import contextlib
import hashlib
import textwrap
from textwrap import indent
from typing import Dict, Generator, List

from git import Head, Repo

from patched_cli.client.patched import PatchedClient
from patched_cli.client.scm import GithubClient, GitlabClient, ScmPlatformClientProtocol
from patched_cli.models.common import Patch, PatchMessage, Report
from patched_cli.models.records import LocalRepository, PrCreationResult
from patched_cli.utils.logging import logger
from patched_cli.utils.noop import noop


def get_slug_from_remote_url(remote_url: str) -> str:
    # TODO: consider using https://github.com/nephila/giturlparse instead
    if remote_url.startswith("git@"):
        # ssh
        _, _, potential_slug = remote_url.partition(":")
    else:
        potential_slug = "/".join(remote_url.split("/")[-2:])

    return potential_slug.removesuffix(".git")


@contextlib.contextmanager
def transitioning_branches(repo: Repo, is_new_branch: bool) -> Generator[tuple[Head, Head], None, None]:
    current_branch = repo.active_branch
    # default noop
    final_func = noop
    next_branch = current_branch
    if is_new_branch:
        next_branch_name = f"patched-{current_branch.name}"
        logger.info(f'Creating new branch "{next_branch_name}".')
        final_func = current_branch.checkout
        next_branch = repo.create_head(next_branch_name, force=True)

    try:
        next_branch.checkout()
        yield current_branch, next_branch
    finally:
        final_func()


class _EphemeralGitConfig:
    _DEFAULT = -2378137912

    def __init__(self, repo: Repo):
        self._repo = repo
        self._keys: set[tuple[str, str]] = set()
        self._original_values: Dict[tuple[str, str], str] = dict()
        self._modified_values: Dict[tuple[str, str], str] = dict()

    def set_value(self, section: str, option: str, value: str):
        self._keys.add((section, option))
        self._modified_values[(section, option)] = value

    @contextlib.contextmanager
    def context(self):
        try:
            self._persist_values_to_be_modified()
            yield
        finally:
            self._undo_modified_values()

    def _persist_values_to_be_modified(self):
        reader = self._repo.config_reader("repository")
        for section, option in self._keys:
            original_value = reader.get_value(section, option, self._DEFAULT)
            if original_value != self._DEFAULT:
                self._original_values[(section, option)] = original_value

        writer = self._repo.config_writer()
        try:
            for section, option in self._keys:
                writer.set_value(section, option, self._modified_values[(section, option)])
        finally:
            writer.release()

    def _undo_modified_values(self):
        writer = self._repo.config_writer()
        try:
            for section, option in self._keys:
                original_value = self._original_values.get((section, option), None)
                if original_value is None:
                    writer.remove_option(section, option)
                else:
                    writer.set_value(section, option, original_value)
        finally:
            writer.release()


def commit_with_msg(repo: Repo, msg: str):
    ephemeral = _EphemeralGitConfig(repo)
    ephemeral.set_value("user", "name", "patched.codes[bot]")
    ephemeral.set_value("user", "email", "298395+patched.codes[bot]@users.noreply.github.com")

    with ephemeral.context():
        repo.git.commit(
            "--author",
            "patched.codes[bot]<298395+patched.codes[bot]@users.noreply.github.com>",
            "-m",
            msg,
        )


def create_branch_and_pr(
    local_repo: LocalRepository,
    applied_patches: List[Patch],
    is_create_pr: bool,
    report: Report | None,
    scm_client: ScmPlatformClientProtocol | None,
    patched_client: PatchedClient | None,
) -> PrCreationResult:
    repo: Repo = local_repo.repo  # type: ignore

    with transitioning_branches(repo, local_repo.is_new_branch) as (current_branch, next_branch):
        # git add
        for applied_patch in applied_patches:
            repo.git.add(applied_patch.path)
            commit_with_msg(repo, f"Patched: \"{applied_patch.path}\"")

        if not is_create_pr or (scm_client is None and patched_client is None):
            return PrCreationResult(
                message=f'Branch created at: "{next_branch.name}"',
                branch_name=next_branch.name,
                pr_url=None,
            )

        tracking_branch = current_branch.tracking_branch()
        if tracking_branch is None:
            msg = f"""\
            Unable to create pull request as base branch does not track a remote branch.
            Branch created at: \"{next_branch.name}\""""
            return PrCreationResult(message=textwrap.dedent(msg), branch_name=next_branch.name, pr_url=None)

        original_remote_name = tracking_branch.remote_name
        original_remote_url = repo.remotes[original_remote_name].url

        logger.info(f'Creating pull request for branch "{next_branch.name}" to merge into "{current_branch.name}".')
        # force push, assume we have control
        repo.git.push("-f", "--set-upstream", original_remote_name, next_branch.name)

        repo_slug = get_slug_from_remote_url(original_remote_url)
        # diff_text = repo.git.diff(current_branch.name)
        diff_text = ""

        if scm_client is not None:
            url = create_pr(
                repo_slug=repo_slug,
                path=str(local_repo.path),
                diff_text=diff_text,
                original_branch_name=current_branch.name,
                next_branch_name=next_branch.name,
                applied_patches=applied_patches,
                report=report,
                scm_client=scm_client,
            )
        elif patched_client is not None:
            url = patched_client.create_pr(
                repo_slug=repo_slug,
                path=str(local_repo.path),
                diff_text=diff_text,
                original_branch=current_branch.name,
                next_branch=next_branch.name,
                patches=applied_patches,
                report=report,
            )
        else:
            raise ValueError("Either scm_client or patched_client must be provided")

        return PrCreationResult(
            message=f'Pull request generated at: "{url}"',
            branch_name=next_branch.name,
            pr_url=url,
        )


def create_pr(
    repo_slug: str,
    path: str,
    diff_text: str,
    original_branch_name: str,
    next_branch_name: str,
    applied_patches: List[Patch],
    report: Report | None,
    scm_client: ScmPlatformClientProtocol,
):
    if report is None:
        body = "This is an automated pull request generated by patched."
    else:
        body = f"This pull request from patched fixes {report.fixes_triaged} issues."

    pr = scm_client.create_pr(
        repo_slug,
        f"Patched results for branch: {original_branch_name}",
        body,
        original_branch_name,
        next_branch_name,
    )

    if isinstance(scm_client, GithubClient):
        file_link_format = "{url}/files#diff-{diff_anchor}"
        chunk_link_format = "{url}/files#diff-{diff_anchor}L{start_line}-L{end_line}"
        anchor_hash = hashlib.sha256
    elif isinstance(scm_client, GitlabClient):
        file_link_format = "{url}/diffs#{diff_anchor}"
        # TODO: deal with gitlab line links
        # chunk_link_format = "{url}/diffs#{diff_anchor}_{start_line}_{end_line}"
        chunk_link_format = "{url}/diffs#{diff_anchor}"
        anchor_hash = hashlib.sha1
    else:
        return pr.url()

    file_comment_parts = []
    for repo_file_path, patch_msgs in create_comments(applied_patches, path):
        diff_anchor = anchor_hash(repo_file_path.encode()).hexdigest()
        file_link = file_link_format.format(url=pr.url(), diff_anchor=diff_anchor)
        file_part = f"File changed: [{repo_file_path}]({file_link})"

        chunk_comment_parts = []
        for patch_msg in patch_msgs:
            chunk_link = chunk_link_format.format(
                url=pr.url(), diff_anchor=diff_anchor, start_line=patch_msg.start_line, end_line=patch_msg.end_line
            )
            expandable = (
                f"<details><summary>[{patch_msg.title}]({chunk_link})</summary>"
                f"{indent(patch_msg.msg, '  ')}</details>"
            )
            chunk_comment_parts.append(expandable)

        msg = f"""\
<div markdown="1">

* {file_part}{''.join(chunk_comment_parts)}

</div>"""
        file_comment_parts.append(msg)

    new_body = "\n\n".join([body, "------", *file_comment_parts])
    pr.set_body(new_body)

    return pr.url()


def create_comments(applied_patches: List[Patch], path: str) -> Generator[tuple[str, list[PatchMessage]], None, None]:
    for applied_patch in applied_patches:
        git_file_path = applied_patch.path.removeprefix(path + "/")
        yield git_file_path, applied_patch.msgs


def wipe_null(obj: dict):
    rv = dict()
    for key, value in obj.items():
        if value is not None:
            rv[key] = value
    return rv
