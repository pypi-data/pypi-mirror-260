from __future__ import annotations

from thefuzz import fuzz


def find_query_in_text(query: str, text: str, split_on: str = "\n") -> tuple[int, int, int]:
    """Find the best match for a query in a text."""
    segments = text.split(split_on)
    best_match = None
    best_score = 0
    best_index = -1

    for index, segment in enumerate(segments):
        score = fuzz.partial_ratio(query, segment)
        if score > best_score:
            best_score = score
            best_match = segment
            best_index = index

    if best_index != -1:
        start_index = text.find(best_match)
        end_index = start_index + len(best_match)
        return start_index, end_index, best_score

    return -1, -1, 0
