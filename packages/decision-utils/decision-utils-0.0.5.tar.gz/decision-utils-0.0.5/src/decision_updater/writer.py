import datetime
import logging
import multiprocessing
import warnings
from collections import Counter
from collections.abc import Iterator
from pathlib import Path

import frontmatter
import spacy
from citation_title import cite_title
from citation_utils import CountedCitation
from environs import Env
from statute_utils import CountedStatute, setup_local_statute_db

from .dumper import SafeDumper
from .md import clear_markdown

nlp = spacy.load("en_artifacts")

warnings.filterwarnings("ignore")
env = Env()
env.read_env()

DECISIONS = Path().home().joinpath(env.str("DECISIONS_DIR"))
STATUTES = Path().home().joinpath(env.str("STATUTES_DIR"))

logging.debug("Setup statutes database for statute_utils matching")
setup_local_statute_db(STATUTES)


def create_phrase_list(content: str):
    doc = nlp(clear_markdown(content))
    spans = (
        (s.text, s.label_) for s in doc.spans["sc"] if s.label_ not in ("date", "unit")
    )
    return ["__".join([k[0], k[1], str(v)]) for k, v in Counter(spans).items()]


def get_opinion_files_by_year(year: int) -> Iterator[Path]:
    return DECISIONS.glob(f"**/{str(year)}-*/**/*.md")


def get_date_string(file: Path) -> str:
    # get date string based on the path
    _, _, date_str, _ = file.parts[-4:]
    if "/opinion/" in str(file):
        _, _, date_str, _, _ = file.parts[-5:]
    return date_str


def update_opinion(file: Path):
    from decision_updater import format_text

    try:
        # only applicable for looping
        marker = str(file.relative_to(DECISIONS))
        logging.info(f"Updating opinion: {marker}")
    except ValueError:
        marker = None

    # convert text from file to frontmatter
    try:
        post = frontmatter.load(str(file))
    except Exception as e:
        logging.error(f"Loading frontmatter from {file=} failed.; {e=}")

    content = format_text(post.content)
    doc_date = datetime.date.fromisoformat(get_date_string(file))
    statute_list = CountedStatute.from_source(
        text=content,
        document_date=doc_date,
        context=marker,
    )
    citation_list = CountedCitation.from_source(content)
    phrase_list = create_phrase_list(content)

    # prepare data dictionary, remove fields (if they exist) that will be updated
    data = {k: post[k] for k in post.keys() if k not in ("statutes", "citations")}

    # if title key exists (separate opinions won't have them), create a short title
    if "short" not in data:
        if title := data.get("title"):
            data["short"] = cite_title(title) or title[:20]  # type: ignore

    # generate a statute string, if statutes found
    if statutes := "; ".join(
        [f"{c.cat.value.lower()} {c.num.lower()}: {c.mentions}" for c in statute_list]
    ):
        data["statutes"] = statutes

    # generate a citation string, if citations found
    if citations := "; ".join([repr(c) for c in citation_list]):
        data["citations"] = citations

    # add artifact phrases
    if phrase_list:
        data["phrases"] = phrase_list

    # clean content
    post = frontmatter.Post(content, **data)  # type: ignore

    # save file with updated statutes and citations
    frontmatter.dump(post=post, fd=str(file))

    # frontmatter.dump does not include a trailing new line which is
    # a standard for markdown files, a hack is simply to add a new line manually
    # see https://github.com/eyeseast/python-frontmatter/issues/87
    # file.write_text(data=file.read_text() + "\n")


def update_markdown_opinion_file(file: Path, timeout: float = 5):
    """Time-based wrapper around `update_file()` to ensure that it doesn't exceed
    5 seconds in processing the file. If the process is still running at the 5-second
    mark, will terminate.

    Args:
        file (Path): File to update
        timeout (float, optional): Number of seconds before timeout. Defaults to 5.
    """
    process = multiprocessing.Process(target=update_opinion, args=(file,))
    process.start()
    process.join(timeout=timeout)
    if process.is_alive():
        logging.error(f"Took too long: {file=}")
        process.terminate()
        process.join()
