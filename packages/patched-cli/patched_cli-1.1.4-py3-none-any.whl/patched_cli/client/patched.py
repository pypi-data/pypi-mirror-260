import atexit
import os
import pathlib
import socket
import sys
from typing import List

import click
import requests
from git.repo.base import Repo
from requests import Response, Session
from requests.adapters import DEFAULT_POOLBLOCK, HTTPAdapter
from urllib3 import HTTPConnectionPool, HTTPSConnectionPool, PoolManager

from patched_cli.envvars import PATCH_MODEL_ENVVAR, PATCH_TRIAGE_ENVVAR
from patched_cli.models.common import CreatePullRequest, Patch, PatchResponse, VulnFile, Report
from patched_cli.utils.logging import logger


class TCPKeepAliveHTTPSConnectionPool(HTTPSConnectionPool):
    # probe start
    TCP_KEEP_IDLE = 60
    # probe interval
    TCP_KEEPALIVE_INTERVAL = 60
    # probe times
    TCP_KEEP_CNT = 3

    def _validate_conn(self, conn):
        super()._validate_conn(conn)

        if sys.platform == "linux":
            if hasattr(socket, "TCP_KEEPIDLE"):
                conn.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, self.TCP_KEEP_IDLE)
            if hasattr(socket, "TCP_KEEPINTVL"):
                conn.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, self.TCP_KEEPALIVE_INTERVAL)
            if hasattr(socket, "TCP_KEEPCNT"):
                conn.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, self.TCP_KEEP_CNT)
        elif sys.platform == "darwin":
            conn.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            conn.sock.setsockopt(socket.IPPROTO_TCP, 0x10, self.TCP_KEEPALIVE_INTERVAL)
        elif sys.platform == "win32":
            conn.sock.ioctl(
                socket.SIO_KEEPALIVE_VALS, (1, self.TCP_KEEP_IDLE * 1000, self.TCP_KEEPALIVE_INTERVAL * 1000)
            )


class KeepAlivePoolManager(PoolManager):
    def __init__(self, num_pools=10, headers=None, **connection_pool_kw):
        super().__init__(num_pools=num_pools, headers=headers, **connection_pool_kw)
        self.pool_classes_by_scheme = {
            "http": HTTPConnectionPool,
            "https": TCPKeepAliveHTTPSConnectionPool,
        }


class KeepAliveHTTPSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=DEFAULT_POOLBLOCK, **pool_kwargs):
        self.poolmanager = KeepAlivePoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            strict=True,
            **pool_kwargs,
        )


class PatchedClient(click.ParamType):
    TOKEN_URL = "https://app.patched.codes/signin"
    DEFAULT_PATCH_URL = "https://patch-function-ps63srnnsq-de.a.run.app"

    def __init__(self, url: str, access_token: str):
        self.access_token = access_token
        self.url = url
        self._session = Session()
        atexit.register(self._session.close)
        self._edit_tcp_alive()

    def _edit_tcp_alive(self):
        # credits to https://www.finbourne.com/blog/the-mysterious-hanging-client-tcp-keep-alives
        self._session.mount("https://", KeepAliveHTTPSAdapter())

    def _post(self, **kwargs) -> Response | None:
        try:
            response = self._session.post(**kwargs)
        except requests.ConnectionError as e:
            logger.error(f"Unable to establish connection to patched server: {e}")
            return None
        except requests.RequestException as e:
            logger.error(f"Request failed with exception: {e}")
            return None

        return response

    def test_token(self) -> bool:
        response = self._post(
            url=self.url + "/token/test", headers={"Authorization": f"Bearer {self.access_token}"}, json={}
        )

        if response is None:
            return False

        if not response.ok:
            logger.error(f"Access Token failed with status code {response.status_code}")
            return False

        body = response.json()
        if "msg" not in body:
            logger.error("Access Token test failed with unknown response")
            return False

        return body["msg"] == "ok"

    def get_patches(self, path: pathlib.Path, repo: Repo | None, vuln_files: List[VulnFile]) -> PatchResponse:
        branch_name = None
        original_remote_url = path.absolute().as_uri()
        if repo is not None:
            branch = repo.active_branch
            branch_name = branch.name
            tracking_branch = branch.tracking_branch()
            if tracking_branch is not None:
                original_remote_name = tracking_branch.remote_name
                original_remote_url = repo.remotes[original_remote_name].url

        request_obj = {
            "url": original_remote_url,
            "branch": branch_name,
            "vuln_files": [vuln_file.model_dump() for vuln_file in vuln_files],
        }

        model = os.getenv(PATCH_MODEL_ENVVAR)
        apply_triage = os.getenv(PATCH_TRIAGE_ENVVAR)
        if model is not None:
            request_obj["model"] = model
        if apply_triage is not None:
            request_obj["triage"] = not apply_triage.lower() == "false"

        response = self._post(
            url=self.url + "/v2/patch",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json=request_obj,
        )

        if response is None:
            return PatchResponse()

        if not response.ok:
            logger.error(f"Get Patches failed with status code {response.status_code}")
            return PatchResponse()

        try:
            return PatchResponse(**response.json())
        except Exception as e:
            logger.error(f"Get Patches failed with exception: {e}")
            return PatchResponse()

    def create_pr(
        self,
        repo_slug: str,
        path: str,
        diff_text: str,
        original_branch: str,
        next_branch: str,
        patches: List[Patch],
        report: Report,
    ) -> str:
        create_pull_request = CreatePullRequest(
            repo_slug=repo_slug,
            path=path,
            diff_text=diff_text,
            original_branch_name=original_branch,
            next_branch_name=next_branch,
            applied_patches=patches,
            report=report,
        )
        response = self._post(
            url=self.url + "/create_pr",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json=create_pull_request.model_dump(),
        )

        if response is None:
            return ""

        if not response.ok:
            logger.error(f"Create PR failed with status code {response.status_code}")
            return ""

        if "url" not in response.json():
            logger.error("Create PR failed with unknown response")
            return ""

        return response.json()["url"]
