def is_text_possible(text: str, max_len: int = 30) -> bool:
    if text := text.strip():  # not empty string
        if len(text) <= max_len:
            return True
    return False
