from __future__ import annotations

import re


class IndexedSpans:
    """Spans with various indexes."""

    def __init__(
        self,
        raw_string: str,
        spans: list[str] | None = None,
        span_extractor_fn: callable | None = None,
    ) -> None:
        """Initialize the IndexedSpans object.

        Args:
            raw_string (str): The original raw text string.
            spans (list[str] | None): A list of strings, each representing an important
                span (sentence) from the raw_string. If None, then the span_extractor_fn
                must be provided.
            span_extractor_fn (callable | None): A function that extracts spans from the
                raw string. If None, then the spans must be provided.
        """
        self.raw = raw_string

        if spans:
            self.spans = spans
        elif span_extractor_fn:
            self.spans = span_extractor_fn(raw_string)
        else:
            error_msg = "Either spans or a span_extractor_fn must be provided."
            raise ValueError(error_msg)

        self.string_start, self.string_end = self.index_spans()

    def index_spans(self) -> tuple[list[list[int]], list[list[int]]]:
        """Indexes the spans in the raw string."""
        string_start, string_end = [], []
        for span in self.spans:
            starts, ends = [], []
            for match_ in re.finditer(re.escape(span), self.raw):
                starts.append(match_.start())
                ends.append(match_.end())
            string_start.append(starts)
            string_end.append(ends)

        return string_start, string_end

    def span(self, span_idx: int) -> str | None:
        """Returns the span at the specified index.

        Args:
            span_idx: The index of the span in the list.

        Returns:
            The span at the specified index, or None if not found.
        """
        return self.spans[span_idx] if 0 <= span_idx < len(self.spans) else None

    def get_span_start(self, span_idx: int) -> list[int]:
        """Returns the starting index of the span in the raw string.

        Args:
            span_idx: The index of the span in the list.

        Returns:
            The starting index(es) of the span in the raw string, or an empty list if not found.
        """
        return self.string_start[span_idx] if 0 <= span_idx < len(self.string_start) else []

    def get_span_end(self, span_idx: int) -> list[int]:
        """Returns the ending index of the span in the raw string.

        Args:
            span_idx: The index of the span in the list.

        Returns:
            The ending index(es) of the span in the raw string, or an empty list if not found.
        """
        return self.string_end[span_idx] if 0 <= span_idx < len(self.string_end) else []

    def raw_string(self) -> str:
        """Returns the original raw string"""
        return self.raw

    def num_spans(self) -> int:
        """Returns the number of spans in the raw string."""
        return len(self.spans)

    def inverse_removing(self, spans_to_remove: list[int]) -> str:
        """Returns a string after removing the specified spans.

        Args:
            spans_to_remove: List of span indices (ints) to remove. If the index is out of
                bounds, it is ignored.

        Returns:
            A string with the specified spans removed.
        """
        segments = []
        previous_end = 0
        removed_indices = set(spans_to_remove)

        # Flattening and sorting the ranges to remove in ascending order based on start indices
        all_starts = [
            start for idx, starts in enumerate(self.string_start) if idx in removed_indices for start in starts
        ]
        all_ends = [end for idx, ends in enumerate(self.string_end) if idx in removed_indices for end in ends]
        all_ranges = sorted(zip(all_starts, all_ends), key=lambda x: x[0])

        for start, end in all_ranges:
            if start >= previous_end:
                segments.append(self.raw[previous_end:start])
                previous_end = end
        segments.append(self.raw[previous_end:])

        return "".join(segments)

    def get_span_index(self, span: str) -> int | None:
        """Returns the index of the specified span.

        Args:
            span: The span to search for.

        Returns:
            The index of the specified span, or None if not found.
        """
        return self.spans.index(span) if span in self.spans else None
