import re

VOTELINE_MIN_LENGTH = 15
VOTELINE_MAX_LENGTH = 1000


def is_line_ok(text: str):
    has_proper_length = VOTELINE_MAX_LENGTH > len(text) > VOTELINE_MIN_LENGTH
    has_indicator = re.search(r"(C\.|J\.)?J\.", text)
    not_all_caps = not text.isupper()
    first_char_capital_letter = re.search(r"^[A-Z]", text)
    return all(
        [
            has_proper_length,
            has_indicator,
            not_all_caps,
            first_char_capital_letter,
        ]
    )


def extract_votelines(key_id: str, text: str):
    lines = text.splitlines()
    for counter, line in enumerate(lines, start=1):
        if is_line_ok(line):
            yield dict(
                id=f"{key_id}v{counter}",
                key_id=key_id,
                counter=counter,
                text=line.strip(),
            )
