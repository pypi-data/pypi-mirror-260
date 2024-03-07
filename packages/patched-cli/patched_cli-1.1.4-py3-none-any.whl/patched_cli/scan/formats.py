import json
import os
import pathlib
import sys
from urllib.parse import urlparse

from patched_cli.models.common import Cwe, Vuln, VulnFile
from patched_cli.models.enums import Severity
from patched_cli.utils.logging import logger


class SarifFormat:
    def parse(self, repo_path: pathlib.Path, vuln_file: str | pathlib.Path) -> list[VulnFile]:
        with open(vuln_file, "r", encoding="utf-8-sig") as f:
            sarif_results = json.load(f)

        total_vuln_files = []
        for runs in sarif_results["runs"]:
            locations = []
            for artifact in runs["artifacts"]:
                uri = urlparse(artifact["location"]["uri"])
                path = uri.path.lstrip("/")
                if "/" not in path and "\\" in path and sys.platform != "win32":
                    path = path.replace("\\", "/")
                if "\\" not in path and "/" in path and sys.platform == "win32":
                    path = path.replace("/", "\\")

                location = pathlib.Path(path)
                if not location.is_file():
                    # find by wildcard
                    location = next(pathlib.Path(repo_path).glob(f"**{os.sep}{path}"), None)
                else:
                    location = location.resolve()
                if location is None:
                    # cut the first repo path and try to find the file again
                    path = path.lstrip(repo_path.name)
                    location = next(pathlib.Path(repo_path).glob(f"**{os.sep}{path}"), None)

                if location is None:
                    # cut the first path part and try to find the file again
                    _, _, path = path.partition(os.sep)
                    location = next(pathlib.Path(repo_path).glob(f"**{os.sep}{path}"), None)

                if location is None:
                    logger.warning(f"Unable to find file {path}")
                locations.append(location)

            vuln_files: list[VulnFile | None] = [None for _ in locations]
            for result in runs["results"]:
                for result_location in result["locations"]:
                    try:
                        artifact_index = result_location["physicalLocation"]["artifactLocation"]["index"]
                        start_line = result_location["physicalLocation"]["region"]["startLine"]
                        location = locations[artifact_index]
                        bug_msg = result["message"]["text"]
                    except KeyError as e:
                        logger.warning(f"Unable to find key in result: {result}, error: {e}")
                        continue
                    except IndexError as e:
                        logger.warning(f"Unable to find index in artifacts: {result}, error: {e}")
                        continue

                    severity = None
                    if "properties" in result.keys() and "Severity" in result["properties"].keys():
                        severity = Severity.from_str(result["properties"]["Severity"])

                    if severity is None:
                        severity = Severity.UNKNOWN

                    vuln = Vuln(
                        cwe=Cwe(id=-1, title=bug_msg),
                        severity=severity,
                        bug_msg=bug_msg,
                        start=start_line,
                        end=start_line,
                    )

                    vuln_file = vuln_files[artifact_index]
                    if vuln_file is None:
                        if location is None:
                            continue
                        with open(location) as f:
                            src = f.read()

                        vuln_file = VulnFile(path=str(location), src=src, vulns=[vuln], is_obfuscated=False)
                        vuln_files[artifact_index] = vuln_file
                    else:
                        vuln_file = vuln_files[artifact_index]
                        vuln_file.vulns.append(vuln)
            total_vuln_files.extend(vuln_files)
        return [total_vuln_files for total_vuln_files in total_vuln_files if total_vuln_files is not None]
