import logging
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Deque

import frontmatter
from bs4 import BeautifulSoup, Tag
from corpus_judge import CandidateJustice
from decision_fetcher_fields import (
    MD_FOOTNOTE_ANNEX_CLEAN,
    MD_FOOTNOTE_ANNEX_SPACE,
    MD_FOOTNOTE_LEFT,
    MD_FOOTNOTE_RIGHT,
    clean_category,
    clean_composition,
    get_header_citation,
    get_writer,
    is_curiam,
    is_extraneous_fragment,
    is_opinion_label,
)
from decision_updater import SafeDumper, update_markdown_opinion_file
from decision_utils import update_content
from markdownify import markdownify
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError

from .config import DECISIONS, ELIB
from .dissect import dissect
from .items import url_to_soup
from .sanitize import case_sanitizer


def convert_path_to_record(path: Path) -> dict[str, str | int | bool]:
    record: dict[str, str | int | bool] = {}
    prefix = path.parts[-4:]
    category = prefix[0]
    number = prefix[1]
    date = prefix[2]
    year = date.split("-")[0]  # first digit
    record = {"cat": category, "num": number, "date": date, "year": year}
    main_file = prefix[3].removesuffix(".md")
    main_file_bits = main_file.split("-")

    if len(main_file_bits) > 1:
        if main_file_bits[1] == "pc":
            record |= {"pc": True}
        elif main_file_bits[1].isdigit():
            record |= {"justice_id": int(main_file_bits[1])}
    return record


@dataclass
class Draft:
    date: str
    title: str
    counter: int
    id: str
    origin: str
    body: str
    annex: str
    dir: str | None = None
    label: str | None = None
    writer: str | None = None
    metadata: dict | None = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"{self.id}: {self.is_valid()=}"  # noqa: E501

    def __post_init__(self):
        # Make html uniform, e.g. <b> tags converted to <strong>, etc.
        self.body = case_sanitizer.sanitize(self.body)

        # Validate body with footnote number
        self.body_html = BeautifulSoup(self.body, "lxml")
        self.body_fns = self.body_html("sup")

        # Validate annex with footnote number
        self.annex = case_sanitizer.sanitize(self.annex)
        self.annex_html = BeautifulSoup(self.annex, "lxml")
        self.annex_fns = self.annex_html("sup")

        # Create variables to match footnote digits via `@is_valid`
        self.body_start_digit: int | None = self.get_digit(self.body_fns)
        self.body_end_digit: int | None = self.get_digit(self.body_fns, True)
        self.annex_start_digit: int | None = self.get_digit(self.annex_fns)
        self.annex_end_digit: int | None = self.get_digit(self.annex_fns, True)

        # Validate and add metadata
        if self.is_valid():
            if self.counter == 1:
                self.add_ponencia_metadata()
            else:
                self.add_opinion_metadata()

    def add_ponencia_metadata(self):
        self.label = "Ponencia"
        meta = dict()
        meta["category"] = clean_category(self.body_html)
        meta["composition"] = clean_composition(self.body_html)
        if citation := get_header_citation(self.body_html):
            if citation.phil:
                meta["phil"] = citation.phil
            elif citation.scra:
                meta["scra"] = citation.scra
            elif citation.offg:
                meta["offg"] = citation.offg

        if strong_tags := self.body_html("strong"):
            writer_tag = strong_tags[0]
            if first_strong_text := writer_tag.text.strip():
                self.writer = get_writer(first_strong_text)
                writer_tag["id"] = "writer-marker"
                if self.writer:
                    meta["is_curiam"] = is_curiam(self.writer)

        self.metadata = meta | dissect(self.body)  # will also produce voting lines

    def add_opinion_metadata(self):
        if center_tags := self.body_html("center"):
            if center_text := center_tags[0].text.strip():
                if is_opinion_label(center_text):
                    self.label = center_text.title()
                    try:
                        writer_tag = self.body_html("strong")[0]
                        if writer_text := writer_tag.text.strip():
                            self.writer = get_writer(writer_text)
                            writer_tag["id"] = "writer-marker"
                    except Exception as e:
                        logging.warning(
                            f"No writer tag (post-center): {self.id=}; {e=}"
                        )

        if not self.label:
            if strong_tags := self.body_html("strong"):
                if first_strong_text := strong_tags[0].text.strip():
                    if is_opinion_label(first_strong_text):
                        self.label = first_strong_text.title()
                        try:
                            writer_tag = strong_tags[1]
                            writer_text = writer_tag.text.strip() or None
                            if writer_text:
                                self.writer = get_writer(writer_text)
                                writer_tag["id"] = "writer-marker"
                        except Exception as e:
                            logging.warning(
                                f"No writer tag (post-strong): {self.id=}; {e=}"
                            )

    @property
    def is_body_ok(self) -> bool:
        return all([self.body_start_digit, self.body_end_digit])

    @property
    def is_annex_ok(self) -> bool:
        return all([self.body_start_digit, self.body_end_digit])

    def is_valid(self) -> bool:
        parts_found = self.is_body_ok and self.is_annex_ok and self.body != self.annex
        if not parts_found:
            logging.warning(
                f"Problematic body/annex: {self.id=}; {self.is_body_ok=}; {self.is_annex_ok=}"  # noqa: E501
            )
            return False

        match_start = self.body_start_digit == self.annex_start_digit
        if not match_start:
            logging.warning(
                f"Start footnotes unmatched: {self.id=}, {self.body_start_digit=} {self.annex_start_digit=}"  # noqa: E501
            )
            return False

        match_end = self.body_end_digit == self.annex_end_digit
        if not match_end:
            logging.warning(
                f"End footnotes unmatched: {self.id=} {self.body_end_digit=} {self.annex_end_digit=}"  # noqa: E501
            )
            return False
        return True

    @property
    def body_md(self):
        """There are 2 types of find operations involved:

        1. BeautifulSoup detects tag element previously marked;
        2. Python string find index of the tag element.
        """
        html = str(self.body_html)
        if tag := self.body_html.find(id="writer-marker"):
            html = html[html.find(str(tag)) + len(str(tag)) :]
        return self.md_footnoted(text=html, is_annex=False).strip()

    @property
    def annex_md(self):
        return self.md_footnoted(text=self.annex.strip(), is_annex=True).strip()

    @property
    def content(self):
        return "\n".join([self.body_md, self.annex_md])

    def create_target_file(self, db: Database) -> Path:
        """Create a target file for the opinion based on the opinion writer."""
        judge = CandidateJustice(
            db=db, text=self.writer, date_str=self.date, tablename="justices"
        )
        if self.counter == 1:  # ponencia
            if judge.per_curiam:
                return Path(f"{self.dir}/main-pc.md")
            elif judge.id:
                return Path(f"{self.dir}/main-{judge.id}.md")
            return Path(f"{self.dir}/main.md")
        elif judge.id:  # non-ponencia, separate opinion
            return Path(f"{self.dir}/opinion/{judge.id}.md")
        return Path(f"{self.dir}/opinion/a{self.counter}.md")

    def write_to_target_file(self, db: Database):
        data = {}
        inclusions = ("title", "category", "composition", "phil", "scra", "offg")
        if self.writer:
            data["writer"] = self.writer

        if self.counter == 1:
            data["origin"] = self.origin
            if self.metadata:
                for k, v in self.metadata.items():
                    if k in inclusions:
                        data[k] = v

                if votes := self.metadata.get("voting"):
                    if isinstance(votes, str):
                        lines = []
                        for line in votes.splitlines():
                            line = line.strip()
                            if line and len(line) > 7:
                                lines.append(line)
                        if lines:
                            data["votelines"] = lines
        else:
            data["label"] = self.label

        target_file = self.create_target_file(db)
        if target_file.exists():
            raise Exception(f"{target_file} must not be overriden.")

        try:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            frontmatter.dump(
                post=frontmatter.Post(self.content, **data),
                fd=str(target_file),
                Dumper=SafeDumper,
            )
        except FileExistsError:
            raise Exception("The file must not be overriden.")

    def get_digit(self, footnotes: list[Tag], start_with_last: bool = False):
        """Gets first matching digit from `footnotes` passed. In some situations,
        asterisks are used so this needs to be ignored / skipped."""
        if footnotes:
            fns = footnotes
            if start_with_last:
                fns = reversed(footnotes)
            for fn in fns:
                num = fn.text.strip("[]* ")
                if num and num.isdigit():
                    return int(num)
        return None

    def md_footnoted(self, text: str, is_annex: bool = False):
        """Accepts html markup as `text` and returns a markdown version
        with footnotes cleaned."""

        # Convert all <sup> tags to ^[]^ style
        raw = markdownify(
            text,
            sup_symbol="^",  # preliminary footnote pattern to use
            escape_asterisks=False,
            escape_underscores=False,
        ).strip()

        # Convert ^[digit]^ to markdown friendly: [^digit]
        partial = MD_FOOTNOTE_LEFT.sub("[^", raw)
        result = MD_FOOTNOTE_RIGHT.sub("]", partial)
        if is_annex:
            # Converts the space after '[^digit]<SPACE>' to '[^digit]:<SPACE>'
            result = MD_FOOTNOTE_ANNEX_SPACE.sub(": ", result)
            result = MD_FOOTNOTE_ANNEX_CLEAN.sub("\n\n", result)
        return result


@dataclass
class KeyDraft:
    """Using an elibrary key integer, generate a URL, request it and then
    convert the response into a collection of `Draft`s. Each Draft is a
    body / annex pair for each opinion found in a decision `Item`."""

    key: int
    title: str | None = None
    text: str | None = None
    parts: Deque | None = None
    date: str | None = None
    path: str | None = None

    def __repr__(self) -> str:
        return f"{self.key}, {self.date=}"

    def setup_opinions(self, db: Database):
        try:
            row = db["elib"].get(self.key)  # type: ignore
            self.title = row["title"]
            self.date = row["date"]
            self.path = f"{DECISIONS}/{row['path']}"
        except NotFoundError:
            raise Exception("Missing key from elib table.")

        markdown_files = list(Path(self.path).glob("**/*.md"))
        if markdown_files:
            raise Exception("Path already pre-existing.")

        url = f"{ELIB}/showdocsfriendly/1/{str(self.key)}"
        soup = url_to_soup(url)
        if not soup:
            raise Exception(f"Timeout; check {url=}")

        # mark the <hr> tags
        divisions = soup("hr")
        for counter, division in enumerate(divisions, start=1):
            division["id"] = f"part-{counter}"

        self.text = str(soup)
        self.parts = deque([str(d) for d in divisions])

        if not self.text:
            raise Exception("Missing text.")

        if not self.parts:
            raise Exception("Missing parts.")

        if not self.date:
            raise Exception("Missing date.")

        if not self.title:
            raise Exception("Missing title.")

        if not self.path:
            raise Exception("Missing path.")

        # initialize variables for slicing
        rows = []
        starter = 0
        counter = 1

        # slice text until marked <hr> tags consumed
        body_stack = []
        while True:
            try:
                marker = self.parts.popleft()
            except IndexError:
                break

            # slice text based on unique marker indicators
            index = self.text.find(marker) + len(marker)
            text_to_evaluate = self.text[starter:index]

            # add to stack, proceed to next slice via a new starter
            if not body_stack:
                body_stack.append(text_to_evaluate)
                starter = index
                continue

            # occassionally, fragments need to be discarded, proceed to next slice
            if is_extraneous_fragment(text_to_evaluate):
                starter = index
                continue

            # create document
            pairing = Draft(
                date=self.date,
                title=self.title,
                counter=counter,
                id=f"{self.key}-{counter}",
                origin=str(self.key),
                body=body_stack.pop(),
                annex=text_to_evaluate,
                dir=self.path,
            )

            # check if body footnotes and the annex footnotes match
            if pairing.is_valid:
                yield pairing
                counter += 1
                starter = index

            else:
                logging.error(f"Unmatched {pairing=}; skipping rest.")
                break
        return rows

    def add_files(self, db: Database):
        if rows := self.setup_opinions(db):
            for row in rows:
                target_file = row.create_target_file(db)
                if target_file.exists():
                    logging.debug(f"{target_file=} pre-existing; skip.")
                    continue

                logging.info(f"Creating {target_file=}.")
                row.write_to_target_file(db)

                # clean the file
                update_content(target_file)

                # add statutes / citations / short title (if appropriate)
                update_markdown_opinion_file(target_file)
                if row.counter == 1:  # ponencia
                    record = convert_path_to_record(target_file)
                    db["decisions"].insert(record=record)  # type: ignore
