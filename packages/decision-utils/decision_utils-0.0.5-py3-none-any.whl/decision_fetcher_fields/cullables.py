import re

from bs4 import BeautifulSoup

EXTRA_SIR_MADAM = re.compile(
    r"""Sirs\/Mesdames\:""",
    re.I | re.X,
)

EXTRA_ATTEST = re.compile(
    r"""I\s*attest\s*that\s*the\s*conclusion(s)?\s*in\s*the\s*above\s*(Decision|Resolution)\s*""",
    re.I | re.X,
)

EXTRA_RELEASE = re.compile(
    r"""O\s*r\s*d\s*e\s*r\s*o\s*f\s*R\s*e\s*l\s*e\s*a\s*s\s*e\s*""", re.I | re.X
)

EXTRA_NOTICE = re.compile(
    r"""N\s*o\s*t\s*i\s*c\s*e\s*o\s*f\s*J\s*u\s*d\s*g\s*m\s*e\s*n\s*t\s*""", re.I | re.X
)

EXTRA_TAKE_NOTICE = re.compile(r"""Please\s*take\s*notice\s*that\s*on""", re.I | re.X)


def is_extraneous_fragment(text: str) -> bool:
    short_slice = text[:500]
    long_slice = text[:1000]
    return (
        is_notice(long_slice)
        or is_order_of_release(short_slice)
        or is_attest(long_slice)
        or is_address(long_slice)
    )


def is_notice(text: str) -> bool:
    return (
        is_notice_title(text) or is_notice_please(text) or notice_variant(text)
    ) and no_footnotes_found(text)
    #! although a `notice of judgment` pattern is found, it may be part of a footnote


def no_footnotes_found(text: str) -> bool:
    """
    Is there a footnote found in the raw string?
    """
    notes = BeautifulSoup(text, "lxml")
    return False if len(notes("sup")) else True


def is_notice_title(text: str) -> bool:
    return is_match_in_text(EXTRA_NOTICE, text)


def is_notice_please(text: str) -> bool:
    return is_match_in_text(EXTRA_TAKE_NOTICE, text)


def is_order_of_release(text: str) -> bool:
    return is_match_in_text(EXTRA_RELEASE, text)


def is_attest(text: str) -> bool:
    return is_match_in_text(EXTRA_ATTEST, text)


def is_address(text: str) -> bool:
    return is_match_in_text(EXTRA_SIR_MADAM, text)


def is_match_in_text(pattern: re.Pattern, text: str) -> bool:
    """
    Determine whether the following patterns exist in source text;
    And if they do, if they exist near the top of the source text:
    1. notice of judgment
    2. order of release
    3. attestation clause
    """
    # create html object from text
    html = BeautifulSoup(text, "lxml")
    # find pattern in html object
    if not (tag := html.find(string=pattern)):
        return False
    # convert target html to string since pattern found
    initiator = str(tag)
    # create text variant of html object to serve as base
    base = str(html)
    # get the text position of initiator string from base
    pos = base.index(initiator)
    # if base position is near top of text, it likely is a match
    if pos < 500:
        return True
    return False


def notice_variant(raw: str) -> bool:
    """
    Problems in finding the notice
    """
    html = BeautifulSoup(raw, "lxml")
    try:
        item = str(html.center.text)  # type: ignore
        return is_match_in_text(EXTRA_NOTICE, item)
    except AttributeError:
        try:
            item = str(html.text)
            return is_match_in_text(EXTRA_NOTICE, item)
        except ValueError:
            return False
    except Exception:
        return False
