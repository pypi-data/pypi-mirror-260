import datetime
import logging
from enum import StrEnum, auto
from http import HTTPStatus
from typing import NamedTuple

import httpx
from bs4 import BeautifulSoup
from citation_utils import Citation
from dateutil.parser import parse
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError, Table

from .config import ELIB


def url_to_content(url: str) -> bytes | None:
    """Get contents of `url`, e.g. html or PDF."""
    res = httpx.get(url, follow_redirects=True, timeout=90.0)
    if res.status_code == HTTPStatus.OK:
        return res.content
    return None


def url_to_soup(url: str) -> BeautifulSoup | None:
    """Creates a soup object from the response of the `url`."""
    content = url_to_content(url=url)
    if content:
        return BeautifulSoup(content, "lxml")
    return None


class Item(NamedTuple):
    """Based on each 'month url', items can be extracted for further processing. Each
    item represents a decision containing fields in this data structure. Paired
    with `citation-utils` (later on), can extract the proper category and number for
    table insertion as a row.
    """

    url: str
    docket: str
    title: str
    date: datetime.date

    def add_to_db(self, db: Database):
        citation = Citation.extract_citation(
            f"{self.docket}, {self.date.strftime('%B %-d, %Y')}"
        )

        if not citation:
            logging.error(f"Could not create citation row, {self.docket=} {self.date=}")
            return None

        if not citation.docket_category:
            logging.error(f"Could not produce docket category {self=}")
            return None

        tbl = db["elib"]
        if not tbl.exists():
            logging.error(f"Missing table to insert record {self=}")
            return None

        if not isinstance(tbl, Table):
            logging.error(f"elib must be a valid table {self=}")
            return None

        id = int(self.url.split("/")[-1])

        cat = citation.docket_category.name.lower()

        if num := citation.docket_serial:
            if "." in num:
                logging.error(f"Citation needs fixing {num=}")
                return None

            num = num.lower()
            if num.endswith("[1"):
                num = num.removesuffix("[1")

            if len(num) < 3:
                logging.error(f"Citation digit too short for elibrary decisions {num=}")
                return None

            if len(num) > 20:
                logging.error(f"Citation digit too long {num=}")
                return None

        date = self.date.isoformat()

        title = self.title.title()
        if len(title) < 20:
            logging.error(f"Title seems too short {title=}")
            return None

        try:
            tbl.get(id)
        except NotFoundError:
            tbl.insert(
                {
                    "id": id,
                    "cat": cat,
                    "num": num,
                    "date": date,
                    "year": self.date.year,
                    "title": title,
                    "path": f"{cat}/{num}/{date}",
                }
            )


class Listing(StrEnum):
    """Contains month names which can pe paired with a year."""

    Jan = auto()
    Feb = auto()
    Mar = auto()
    Apr = auto()
    May = auto()
    Jun = auto()
    Jul = auto()
    Aug = auto()
    Sep = auto()
    Oct = auto()
    Nov = auto()
    Dec = auto()

    @classmethod
    def from_year(cls, year: int, db: Database):
        for member in cls:
            # e-library partial URL to get a list of decisions for a given month
            if soup := url_to_soup(url=f"{ELIB}/docmonth/{member.name}/{year}/1"):
                for tag in soup(id="container_title")[0]("li"):
                    try:
                        item = Item(
                            url=tag("a")[0]["href"].replace(
                                "showdocs",
                                "showdocsfriendly",
                            ),  # get the better formatted url
                            docket=tag("strong")[0].text,
                            title=tag("small")[0].text.strip(),
                            date=parse(
                                tag("a")[0]
                                .find_all(string=True, recursive=False)[-1]
                                .strip()
                            ).date(),
                        )
                        item.add_to_db(db)
                    except Exception as e:
                        logging.error(f"No Decision Item from {tag=}, see {e=}")
