from __future__ import annotations

import gzip
import hashlib
import hmac
import os
import tempfile
from pathlib import Path

import requests


def post_dbt_files(
    files: list[tuple[str, Path]],
    project_id: str,
    invocation_id: str,
    client_id: str,
    client_secret: str,
    root_url: str,
) -> list[tuple[Path, requests.Response]]:
    """
    Upload one or more files matching expected types to the Workstream endpoint.

    Args:
        files (list[tuple[str, Path]]): a list of (file_type, path) pairs to
            upload. file_type should be one of manifest, run_results, or
            sources.
        project_id (str): The dbt project ID associated with the files.
        invocation_id (str): The dbt invocation ID associated with the files.
        client_id (str): The Workstream API client ID.
        client_secret (str): The Workstream API client secret.
        root_url (str): The Workstream API root url.

    Returns: a (Path, Response) pair for each attempted upload.
    """
    responses: list[tuple[Path, requests.Response]] = []
    for file_type, p in files:
        if file_type not in ["manifest", "run_results", "sources"]:
            continue

        url = f"{root_url}dbt/{project_id}/files/{file_type}/{invocation_id}"
        responses.append(
            _post_file(
                file_path=p,
                url=url,
                client_id=client_id,
                client_secret=client_secret,
            )
        )
    return responses


def _post_file(
    file_path: Path, url: str, client_id: str, client_secret: str
) -> requests.Response:
    """
    Post a file to an endpoint of the Workstream API.

    Args:
        - file_path (Path): A Path to an uncompressed file to upload.
        - url (str): The full API endpoint URL to post the file to.
        - client_id (str): The Workstream API client ID.
        - client_secret (str): The Workstream API client secret.
    """
    headers = _build_auth_headers(
        client_id=client_id, client_secret=client_secret, url=url
    )
    with file_path.open("rb") as source_file:
        compressed_data = gzip.compress(source_file.read())
        with tempfile.SpooledTemporaryFile() as compressed_file:
            compressed_file.write(compressed_data)
            compressed_file.seek(0)
            compressed_files = [
                (
                    "file",
                    (
                        f"{file_path.name}.gz",
                        compressed_file,
                        "application/octet-stream",
                    ),
                )
            ]
            response = requests.post(url, headers=headers, files=compressed_files)
            if os.getenv("WORKSTREAM_DBT_CLIENT_DEBUG", "False") == "True":
                print(response.request)
                print(response.request.headers)
                print(response.request.url)
            return file_path, response


def _build_auth_headers(client_id: str, client_secret: str, url: str) -> dict[str, str]:
    """
    Construct the authorization header for a Workstream API request.

    Args:
        - file_path (Path): A Path to an uncompressed file to upload.
        - url (str): The full API endpoint URL to post the file to.
        - client_id (str): The Workstream API client ID.
        - client_secret (str): The Workstream API client secret.

    Returns
    """
    computed_hmac = hmac.new(
        client_secret.encode("utf-8"), url.encode("utf-8"), hashlib.sha512
    ).hexdigest()
    headers = {"Authorization": f"{client_id}:{computed_hmac}"}
    return headers
