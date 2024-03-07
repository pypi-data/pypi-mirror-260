from dataclasses import dataclass
from typing import Match

from bs4 import BeautifulSoup, NavigableString, Tag

from decision_fetcher_fields.tags import non_lowered_tagged_text_short

from .ordered import ordered_pattern
from .wherefore import wherefore_pattern


@dataclass
class Phrase:
    """
    Class for determining WHEREFORE and ORDERED clauses

    1. String matching pattern is contained inside a tag
    2. String matching pattern is found after a tag
    3. String matching pattern is behind a tag

    The return is a stringified HTML e.g. "<b>WHEREFORE</b>"
    """

    mode: str  # Mode determines what pattern to use
    text: str  # Context to search the pattern

    @property
    def pattern(self):
        if self.mode == "WHEREFORE":
            return wherefore_pattern
        elif self.mode == "ORDERED":
            return ordered_pattern

    @property
    def get_clause(self) -> str | None:
        html = BeautifulSoup(self.text, "lxml")
        return self.within_tag(html) or self.succeed_tag(html) or self.precede_tag(html)

    def last(self, html: BeautifulSoup, t: Tag) -> Tag | None:
        """Does target exist in html? If yes, return last tag"""
        return match[-1] if (match := html(t)) else None

    def within_tag(self, html: BeautifulSoup) -> str | None:
        """e.g. <b> SO ORDERED. </b>"""
        return str(res) if (res := self.last(html, self.inside_tag)) else None

    def succeed_tag(self, html: BeautifulSoup) -> str | None:
        """e.g. <br>"So Ordered." """
        match = self.last(html, self.tag_then_text)
        return str(match.next_element) if match else None

    def precede_tag(self, html: BeautifulSoup) -> str | None:
        """e.g. "So Ordered <br>"""
        match = self.last(html, self.pattern_precedes_tag)
        return str(match.previous_element) if match else None

    def inside_tag(self, t: Tag):
        return (
            t.string
            and self.pattern.search(t.get_text())
            and non_lowered_tagged_text_short(t)
        )

    def tag_then_text(self, t: Tag):
        if isinstance(t.next_element, NavigableString):
            return self.pattern.search(t.next_element)
        return None

    def pattern_precedes_tag(self, t: Tag) -> Match | None:
        # the previous element of a tag is a string which contains an ordered clause
        if isinstance(t.previous_element, NavigableString):
            return self.pattern.search(t.previous_element)
        return None
