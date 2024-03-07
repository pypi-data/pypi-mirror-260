import datetime
import logging
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml
from corpus_judge import JUSTICE_FILE
from environs import Env
from sqlite_utils.db import Database, Table

env = Env()
env.read_env()

ELIB = env.str("ELIB")
DECISIONS = Path().home().joinpath(env.str("DECISIONS_DIR"))
NOW = datetime.datetime.now().astimezone(tz=ZoneInfo("Asia/Manila"))


db_file = Path(__file__).parent.parent.parent / "decision_files.db"
"""Name of the database file that will be created/used"""


def create_justices(db: Database) -> Table:
    tbl = db["justices"]
    if not isinstance(tbl, Table):
        raise Exception("justices should be a Table")
    if not tbl.exists():
        rows = yaml.safe_load(JUSTICE_FILE.read_bytes())
        tbl.insert_all(rows)  # type: ignore
    return tbl


def index_dockets(tbl: Table, prefix: str):
    tbl.create_index(  # type: ignore
        columns=["cat", "num", "date"],
        index_name=f"{prefix}_docket_category_num_date",
        if_not_exists=True,
    )
    tbl.create_index(  # type: ignore
        columns=["cat", "num"],
        index_name=f"{prefix}_docket_category_num",
        if_not_exists=True,
    )
    tbl.create_index(  # type: ignore
        columns=["cat"],
        index_name=f"{prefix}_docket_category",
        if_not_exists=True,
    )
    tbl.create_index(  # type: ignore
        columns=["num"],
        index_name=f"{prefix}_docket_num",
        if_not_exists=True,
    )
    tbl.create_index(  # type: ignore
        columns=["date"],
        index_name=f"{prefix}_docket_date",
        if_not_exists=True,
    )
    tbl.create_index(  # type: ignore
        columns=["date"],
        index_name=f"{prefix}_docket_year",
        if_not_exists=True,
    )


def create_elib_source(db: Database) -> Table:
    """See https://elibrary.judiciary.gov.ph/thebookshelf/1"""
    tbl = db["elib"]
    tbl.create(  # type: ignore
        columns={
            "id": int,
            "cat": str,
            "num": str,
            "date": str,
            "year": int,
            "title": str,
            "path": str,  # relative path where file ought to be stored locally
        },
        pk="id",
        not_null=("cat", "num", "date", "year", "title", "path"),
        if_not_exists=True,
    )
    if not isinstance(tbl, Table):
        raise Exception("Invalid object.")
    index_dockets(tbl, "elib")
    return tbl


def get_decision_paths(target_year: int | None = None):
    return DECISIONS.glob(f"*/*/{target_year or ''}*/*.md")
