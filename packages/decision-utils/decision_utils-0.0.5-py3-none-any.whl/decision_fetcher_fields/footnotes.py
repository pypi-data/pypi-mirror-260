import re

MD_FOOTNOTE_LEFT = re.compile(
    r"""
    \^\[ # start with ^[ enclosing digits ending in ], targets the "^["
    (?=\d+\])
    """,
    re.X,
)

MD_FOOTNOTE_RIGHT = re.compile(
    r"""
    (?<=\^\d)(\]\^)| # single digit between ^ and ]^ targets the "]^"
    (?<=\^\d{2})(\]\^)| # double digit between ^ and ]^ targets the "]^"
    (?<=\^\d{3})(\]\^) # triple digit between ^ and ]^ targets the "]^"
    """,
    re.X,
)

MD_FOOTNOTE_ANNEX_SPACE = re.compile(
    r"""
    (?<=\^\d\])\s| # single digit between ^[ and ], targets the space \s after
    (?<=\^\d{2}\])\s| # double digit between ^[ and ], targets the space \s after
    (?<=\^\d{3}\])\s # triple digit between ^[ and ], targets the space \s after
    """,
    re.X,
)

MD_FOOTNOTE_ANNEX_CLEAN = re.compile(
    r"""
    \s+
    (?=
        \[
        \^
        \d+
        \]
        :
    )
    """,
    re.X,
)
