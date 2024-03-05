from __future__ import annotations

import json
from pathlib import Path

import requests

from workstream_dbt_core.exception import WorkstreamError
from workstream_dbt_core.http import post_dbt_files
from workstream_dbt_core.result import DbtResult, WorkstreamResult

MANIFEST = "manifest.json"
RUN_RESULTS = "run_results.json"
SOURCE_RESULTS = "sources.json"


def report_invocation(
    target_path: Path,
    client_id: str,
    client_secret: str,
    root_url: str = "https://api.workstream.io/",
) -> WorkstreamResult:
    """
    Reports an invocation of dbt-core to Workstream.

    Args:
        - target_path (pathlib.Path): The path to the `target` directory created by
            an invocation of dbt.
        - client_id (str): The Client ID provided by Workstream for this integration.
        - client_secret (str): The Client Secret provided by Workstream for this
            integration.
        - root_url (str): The root url for the API endpoint provided by Workstream for
            this integration.

    Returns: list[tuple[Path, requests.Response]]: A (file_path,
        Response) pair for each attempted upload of the file at file_path.

    Raises: WorkstreamError if the process does not successfully complete for all files.
    """
    _validate_target_path(target_path)
    project_id, invocation_id = _get_project_and_invocation_id_from_manifest(
        target_path
    )
    files = _get_files_from_invocation(target_path, invocation_id)
    responses = post_dbt_files(
        files, project_id, invocation_id, client_id, client_secret, root_url
    )
    files_uploaded, upload_errors = _validate_responses(responses)
    dbt_result = _compute_dbt_result(files)
    return WorkstreamResult(
        files_uploaded=files_uploaded,
        upload_errors=upload_errors,
        dbt_result=dbt_result,
    )


def _validate_target_path(target_path: Path) -> None:
    """
    Raise a WorkstreamError if target_path does not contain at least a manifest.json and
    one of a run_results.json or sources.json.
    """
    try:
        assert target_path.exists()
        manifest_path = target_path / MANIFEST
        assert manifest_path.exists()
        run_path = target_path / RUN_RESULTS
        source_path = target_path / SOURCE_RESULTS
        assert run_path.exists() or source_path.exists()
    except AssertionError as e:
        raise WorkstreamError(
            e,
            title="Target path does not contain required files.",
            help_text=(
                "target_path must contain at least a manifest.json and one of a "
                "run_results.json or sources.json."
            ),
        ) from e


def _get_project_and_invocation_id_from_manifest(target_path: Path) -> tuple[str, str]:
    """
    Introspect manifest.json to find latest IDs. All dbt commands create/update
    manifest.json, so the invocation_id from that file should be the ID for the
    most recent dbt run.

    Args:
        - target_path (Path)

    Returns: tuple of (project_id, invocation_id)
    """
    manifest_path = target_path / MANIFEST
    try:
        with manifest_path.open("r") as f:
            manifest = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise WorkstreamError(
            e, title="Could not load manifest.json", help_text=str(e)
        ) from e

    try:
        project_id = manifest["metadata"]["project_id"]
        invocation_id = manifest["metadata"]["invocation_id"]
    except KeyError as e:
        raise WorkstreamError(
            e,
            title="manifest.json missing critical metadata",
            help_text=f"Could not find key metadata.{e}",
        ) from e

    return project_id, invocation_id


def _get_files_from_invocation(
    target_path: Path, invocation_id: str
) -> list[tuple[str, Path]]:
    """
    Finds all manifest, sources, and run_results (.json) files in target_path that match
    invocation_id.

    Returns: A list of (file_type, path) pairs for relevant files.
    """
    candidates = [MANIFEST, RUN_RESULTS, SOURCE_RESULTS]
    found_files: list[tuple[str, Path]] = []
    for fn in candidates:
        p = target_path / fn
        try:
            with p.open("r") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue

        try:
            file_invocation_id = data["metadata"]["invocation_id"]
        except KeyError:
            continue
        else:
            if file_invocation_id == invocation_id:
                found_files.append((p.stem, p))

    return found_files


def _validate_responses(
    responses: list[tuple[Path, requests.Response]],
) -> tuple[list[Path], list[WorkstreamError]]:
    """
    Separate responses into successes and errors.

    Args:
        - responses (list[tuple[pathlib.Path, requests.Response]]): A (file_path,
        Response) pair for each attempted upload of the file at file_path.

    Returns: a tuple of lists; first list is successful uploads; second is errors.
    """
    uploads = [p for p, resp in responses if resp.ok]
    errors = [
        WorkstreamError(
            title=f"Encountered an error while uploading {p} to Workstream.",
            help_text=f"{resp.text}",
        )
        for p, resp in responses
        if not resp.ok
    ]
    return uploads, errors


def _compute_dbt_result(files: list[tuple[str, Path]]) -> DbtResult:
    """
    Search run_results or sources for error or failed statuses.

    Args:
        - files: A list of (file_type, path) pairs for relevant files.

    Returns: DbtResult
    """
    results_files = [
        p for file_type, p in files if file_type in ("run_results", "sources")
    ]
    if len(results_files) != 1:
        # run crashed before writing results file
        return DbtResult(exit_code=2, failing_nodes=[])
    try:
        with results_files[0].open("r") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        # dbt wrote an invalid file
        return DbtResult(exit_code=2, failing_nodes=[])
    else:
        failing_nodes: list[str] = []
        for node_result in data["results"]:
            if node_result["status"] in ["fail", "error"]:
                failing_nodes.append(node_result["unique_id"])
        return DbtResult(
            exit_code=1 if failing_nodes else 0, failing_nodes=failing_nodes
        )
