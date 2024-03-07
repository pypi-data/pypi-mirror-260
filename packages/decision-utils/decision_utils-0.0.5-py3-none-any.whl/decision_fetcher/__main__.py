from pathlib import Path

import click
from sqlite_utils import Database

from .config import create_elib_source, create_justices, db_file
from .draft import KeyDraft
from .items import Listing


@click.group()
def cli():
    """Wrapper of commands to fetch from the e-library."""
    pass


@cli.command()
def init_db():
    log = Path(__file__).parent.joinpath("app.log")
    if log.exists():
        log.unlink()
    Path(__file__).parent.parent.parent.joinpath("decision_files.db").unlink(
        missing_ok=True
    )
    db = Database(filename_or_conn=db_file, use_counts_table=True)
    db.enable_wal()
    create_justices(db)
    create_elib_source(db)
    db.index_foreign_keys()


@cli.command()
@click.option(
    "--start",
    required=True,
    type=int,
    help="Start year to include from the e-library",
)
@click.option(
    "--end",
    type=int,
    required=True,
    help="End year, terminal part of the date range, will not be included",
)
def list_urls(start: int, end: int):
    db = Database(filename_or_conn=db_file, use_counts_table=True)
    for year in range(start, end):  # takes about 3 minutes for all decisions
        Listing.from_year(year=year, db=db)


@cli.command()
@click.option(
    "--start",
    required=True,
    type=int,
    help="Start year to include from the the database",
)
def draft_files(start: int):
    db = Database(filename_or_conn=db_file, use_counts_table=True)
    for row in db["elib"].rows_where("date >= ?", (f"{start}-01-01",)):
        try:
            draft = KeyDraft(key=row["id"])
            draft.add_files(db=db)
        except Exception:
            continue


if __name__ == "__main__":
    cli()
