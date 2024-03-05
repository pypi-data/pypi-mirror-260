from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from workstream_dbt_core.exception import WorkstreamError


@dataclass
class DbtResult:
    exit_code: int
    failing_nodes: list[str]


@dataclass
class WorkstreamResult:
    files_uploaded: list[Path]
    dbt_result: DbtResult
    upload_errors: list[WorkstreamError] = field(default_factory=list)

    def print_report(self, exit_nonzero: bool) -> None:
        for p in self.files_uploaded:
            print(f"Uploaded {p} successfully to Workstream.")
        for e in self.upload_errors:
            print(f"Encountered an error while uploading {p}:\n{e}")
        print(f"dbt exited with code: {self.dbt_result.exit_code}")
        if exit_nonzero:
            print(f"Exiting with code: {self.dbt_result.exit_code}")
        else:
            print("Exiting with code: 0. To exit nonzero, invoke with `--exit-nonzero`")
