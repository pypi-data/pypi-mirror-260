from bs4 import BeautifulSoup
from citation_utils import Citation

from .utils import is_text_possible


def get_header_citation(soup: BeautifulSoup):
    """Initial text at the header of e-library decisions. Often found before
    the first <br> tag and after the E-library header."""
    breaks = soup("br")
    if not breaks:
        return None

    for counter, el in enumerate(breaks, start=1):
        el["id"] = f"mark-{counter}"

    first_br = breaks[0]
    body = str(soup)
    marker = str(first_br)
    index = body.find(marker) + len(marker)
    candidate = body[:index]
    if not is_text_possible(candidate, max_len=150):
        return None

    soup = BeautifulSoup(candidate, "lxml")
    texts = soup(string=True)
    for text in texts:
        check_text = text.lower().strip()
        if "e-library" in check_text:
            continue
        if citation := Citation.extract_citation(check_text):
            return citation
    return None
