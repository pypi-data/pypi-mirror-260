from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pathlib import Path

    from span_explain.lime.explanation import Explanation


def read_prompt_from_file(path_to_prompt_file: Path) -> str:
    """Opens and reads a prompt from a file."""
    with path_to_prompt_file.open("r") as f:
        return f.read()


def mask_text_with_spans(exp: Explanation, spans_to_mask: list[str] | str) -> str:
    """Masks the spans and generates a prediction using the classifier."""
    spans_to_mask = [spans_to_mask] if isinstance(spans_to_mask, str) else spans_to_mask

    ids_to_mask = [
        exp.domain_mapper.indexed_spans.get_span_index(span)
        for span in spans_to_mask
        if exp.domain_mapper.indexed_spans.get_span_index(span) is not None
    ]

    return exp.domain_mapper.indexed_spans.inverse_removing(ids_to_mask)


def remove_words(text: str, words_to_remove: list[str]) -> str:
    """
    Remove specific words from a given text string.

    Args:
        text (str): The input text string.
        words_to_remove (list): A list of words to be removed from the text.

    Returns:
        str: The modified text string with the specified words removed.
    """
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    return " ".join(filtered_words)
