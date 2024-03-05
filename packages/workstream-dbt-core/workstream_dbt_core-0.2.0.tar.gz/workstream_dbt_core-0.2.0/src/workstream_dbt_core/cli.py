from __future__ import annotations

from pathlib import Path
from typing import Any

import click

from workstream_dbt_core.api import report_invocation


def _validate_root_url(ctx: Any, param: Any, value: str) -> str:
    return value if value.endswith("/") else f"{value}/"


@click.group()
def workstream() -> None:
    pass


@workstream.command()
@click.option(
    "--target-path",
    "-t",
    type=click.Path(
        resolve_path=True,
        path_type=Path,
    ),
    default="./target",
    envvar="WORKSTREAM_DBT_TARGET_PATH",
    help=(
        "The path to the `target` directory created by an invocation of dbt. "
        "Defaults to `./target`"
    ),
)
@click.option(
    "--client-id",
    envvar="WORKSTREAM_DBT_CLIENT_ID",
    help="The Client ID provided by Workstream for this integration.",
)
@click.option(
    "--client-secret",
    envvar="WORKSTREAM_DBT_CLIENT_SECRET",
    help="The Client Secret provided by Workstream for this integration.",
)
@click.option(
    "--root-url",
    envvar="WORKSTREAM_DBT_ROOT_URL",
    default="https://api.workstream.io/",
    help=(
        "The root url for the API endpoint provided by Workstream for this integration."
    ),
    callback=_validate_root_url,
)
@click.option(
    "--exit-nonzero",
    envvar="WORKSTREAM_DBT_EXIT_NONZERO",
    help=(
        "Configure whether this program should exit with a nonzero exit code on "
        "dbt failures (like failed tests or run errors). Defaults to False, "
        "so failures with this program do not interfere with subsequent dbt steps."
    ),
    is_flag=True,
)
@click.pass_context
def report(
    ctx: click.Context,
    target_path: Path,
    client_id: str | None,
    client_secret: str | None,
    root_url: str,
    exit_nonzero: bool,
) -> None:
    """
    Reports an invocation of dbt-core to Workstream.
    """
    if not target_path.exists():
        print(
            "Encountered an error:\n"
            f"Configured target path {target_path} does not exist!\n"
            "Default is a directory named 'target' in the CWD; "
            "you can configure this with the --target-path option."
        )
        ctx.exit(code=0)  # don't block future dbt steps
    elif target_path.is_file():
        print(
            "Encountered an error:\n"
            f"Configured target path {target_path} points to a file, "
            "but this tool expects a directory."
        )
        ctx.exit(code=0)

    if client_id is None or client_secret is None:
        print(
            "Encountered an error:\n"
            "Missing credentials! Must set --client-id and --client-secret "
            "or set the environment variables WORKSTREAM_DBT_CLIENT_ID and "
            "WORKSTREAM_DBT_CLIENT_SECRET"
        )
        ctx.exit(code=0)

    result = report_invocation(
        target_path=target_path,
        client_id=client_id,
        client_secret=client_secret,
        root_url=root_url,
    )
    result.print_report(exit_nonzero=exit_nonzero)
    if exit_nonzero:
        ctx.exit(code=result.dbt_result.exit_code)
    else:
        ctx.exit(code=0)
