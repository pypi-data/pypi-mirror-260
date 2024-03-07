from typing import List

from pydantic.main import BaseModel

from patched_cli.models.enums import Severity


class Report(BaseModel):
    # Vulnerabilities Found (CWEs)
    vulns_found: int = 0
    # Vulnerabilities that are Triaged (CWEs)
    vulns_triaged: int = 0
    # Vulnerabilities in Patches that are generated (CWEs)
    fixes_generated: int = 0
    # Vulnerabilities in Patches that are validated (CWEs)
    fixes_validated: int = 0
    # Vulnerabilities in Patches that are compatible (CWEs)
    fixes_compatible: int = 0
    # Vulnerabilities in Patches that are part of PR (CWEs)
    fixes_triaged: int = 0

    def merge(self, other):
        self.vulns_found += other.vulns_found
        self.vulns_triaged += other.vulns_triaged
        self.fixes_generated += other.fixes_generated
        self.fixes_triaged += other.fixes_triaged


class Cwe(BaseModel):
    id: int
    title: str


class Vuln(BaseModel):
    cwe: Cwe
    severity: Severity
    bug_msg: str
    start: int
    end: int


class VulnFile(BaseModel):
    path: str
    src: str
    vulns: List[Vuln]
    is_obfuscated: bool = False


class PatchMessage(BaseModel):
    title: str
    msg: str
    start_line: int
    end_line: int


class Patch(BaseModel):
    path: str
    patch: str
    msgs: List[PatchMessage] = []


class PatchResponse(BaseModel):
    patches: List[Patch] = []
    report: Report = Report()


class CreatePullRequest(BaseModel):
    repo_slug: str
    path: str
    diff_text: str
    original_branch_name: str
    next_branch_name: str
    applied_patches: List[Patch]
    report: Report | None = None
