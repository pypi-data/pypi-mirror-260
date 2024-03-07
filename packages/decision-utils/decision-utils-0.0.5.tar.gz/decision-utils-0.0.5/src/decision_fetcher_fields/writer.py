import re

from .utils import is_text_possible

upper_curiam = r"(\bCURIAM\b)"
title_curiam = r"(\bCuriam\b)"
curiams = [upper_curiam, title_curiam]
CURIAM_PATTERN = re.compile(rf"({'|'.join(curiams)})")


def is_curiam(text: str):
    if CURIAM_PATTERN.search(text):
        return True
    return False


judge = r"(\,?\s*\bJ\b)"
chief = r"(\,?\s*\bC\.?\s*J\b)"
writer_block = [judge, chief] + curiams
WRITER_PATTERN = re.compile(rf"({'|'.join(writer_block)})")


def get_writer(raw: str) -> str | None:
    if not is_text_possible(raw):
        return None

    def clean_writer(text: str):
        text = text.removesuffix(", J,:")
        text = text.removesuffix(" J.:*")
        text = text.removesuffix("[*]")
        text = text.removesuffix(", J:")
        text = text.removesuffix(", J:")
        text = text.removesuffix(", J.:")
        text = text.removesuffix(", C.J.:")
        text = text.removesuffix(":")
        return text.title()

    return clean_writer(raw) if WRITER_PATTERN.search(raw) else None
