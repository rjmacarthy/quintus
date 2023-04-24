from var.constants import DOC_MAX_LENGTH
import re
from typing import List


def split_text(text: str, max_length=DOC_MAX_LENGTH) -> List[str]:
    text: str = text.strip()

    if len(text) <= max_length:
        return [text]

    chunks: List[str] = []
    chunk_start: int = 0

    for match in re.finditer(r"\W", text):
        if match.start() - chunk_start + 1 > max_length:
            chunk_end = match.start()
            chunks.append(text[chunk_start:chunk_end].strip())
            chunk_start = chunk_end + 1
            if len(text) - chunk_start <= max_length * 1.5:
                chunks.append(text[chunk_start:].strip())
                break
        elif match.start() == len(text) - 1:
            chunks.append(text[chunk_start:].strip())
            break

    return chunks
