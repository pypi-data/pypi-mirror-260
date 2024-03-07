import logging

import click
from rich.progress import track

from .writer import get_opinion_files_by_year, update_markdown_opinion_file


@click.command()
@click.option(
    "--start",
    required=True,
    type=int,
    help="Start year to include in /corpus-decisions",
)
@click.option(
    "--end",
    type=int,
    required=True,
    help="End year, terminal part of the date range, will not be included",
)
def update_files(start: int, end: int):
    """Update files found in the folder based on ModifyDecisionHandler config."""
    if start <= 1900:
        raise ValueError("`start` must be > 1900")
    if end >= 2025:
        raise ValueError("`end` must be <= 2024")
    if start >= end:
        raise ValueError("`start` must be < than `end`.")

    for year in range(start, end):
        files = list(get_opinion_files_by_year(year=year))
        for file in track(files, description=f"Processing {year}"):
            try:
                update_markdown_opinion_file(file=file, timeout=20)
            except Exception as e:
                err = f"Could not process {file=}; see {e=}"
                logging.error(err)
