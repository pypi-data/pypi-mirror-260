import re

xao = re.compile(r"\xa0")

xad = re.compile(r"\xad")

cap_start = re.compile(r"^\s+(?=[A-Z\*].+)", re.M)

x_placeholder = r"\s*[x][\sx]+\n{2}"
xxx = "x x x"
xxx_bq_ideal = " " + xxx + "\n"
xxx_bq1 = re.compile(rf"(?<=^>){x_placeholder}", re.M)
xxx_bq2 = re.compile(rf"(?<=^>\s>){x_placeholder}", re.M)
xxx_bq3 = re.compile(rf"(?<=^>\s>\s>){x_placeholder}", re.M)


line_starts_with_space = re.compile(r"^\s+")

two_spaces_then_line = re.compile(r"\s{2}\n")
"""Two spaces plus line break needs an extra space."""

start_bq = re.compile(r"\n{2}(>\n){2}", re.M)
"""Blockquotes that start with double line breaks and followed by double blockquotes"""

end_bq = re.compile(r"(\n[>\s]+){2}\n{2}", re.M)
"""Blockquotes that terminate with double blockquotes and double line breaks"""

lone_bq = re.compile(r"\n{2}[>\s]+\n{2}", re.M)
"""Blockquotes that appear as a lone symbol, surrounded by double link breaks"""

sp_empty_bq = re.compile(r"(?<=^>)\n{2}(?=>)")
"""Blockquote terminating with double line breaks and followed by another blockquote"""

bq_line_next_line_not_bq = re.compile(
    r"""
            ^> # starts with blockquote marker
            .+$ # has content and terminates
            \n # new line
            ^(?!>|\s) # start of new line not another blockquote or a space
            """,
    re.M | re.X,
)
"""Since blockquote + newline + text will result in the blockquote + text, need to add a separate line to create a double breakline `\n\n`"""  # noqa: E501


def clean_text(raw_content: str):
    for old, new in [
        ("`", "'"),
        ("“", '"'),
        ("”", '"'),
        ("‘", "'"),
        ("’", "'"),
        ("\u2018", "'"),
        ("\u2019", "'"),
        ("\u0060", "'"),
        ("*vs*.", "v."),
        ("*vs*", "v."),
        ("*v.*", "v."),
        ("*v*.", "v."),
        ("_vs_.", "v."),
        ("_vs_", "v."),
        ("_v._", "v."),
        ("_v_.", "v."),
        (" vs. ", " v. "),
        (", v. ", " v. "),
        (", vs. ", " v. "),
        ("'' ", '" '),
        (" ''", ' "'),
    ]:
        raw_content = raw_content.replace(old, new)
    return raw_content


italicized_case = re.compile(
    r"""
    \*{3} # marker
    (?P<casename>
        (.+?)
        (\svs?\.\s)
        (.+?)
    )
    \*{3} # marker
    """,
    re.X,
)


def add_extra_line(text: str):
    """Recursively go through the text and examine each matching line, adding a new line to each."""  # noqa: E501
    while True:
        if match := bq_line_next_line_not_bq.search(text):
            line = match.group()
            text = text.replace(line, line + "\n")
        else:
            break
    return text


def format_text(text: str):
    text = two_spaces_then_line.sub("\n\n", text)
    text = line_starts_with_space.sub("", text)
    text = cap_start.sub("\n", text)
    text = text.replace("`", "'h")
    text = xao.sub(" ", text)
    text = xad.sub("", text)
    text = xxx_bq1.sub(xxx_bq_ideal, text)
    text = xxx_bq2.sub(xxx_bq_ideal, text)
    text = xxx_bq3.sub(xxx_bq_ideal, text)
    text = start_bq.sub("\n\n", text)
    text = end_bq.sub("\n\n", text)
    text = lone_bq.sub("\n\n", text)
    text = sp_empty_bq.sub("\n", text)
    text = add_extra_line(text)
    return text
