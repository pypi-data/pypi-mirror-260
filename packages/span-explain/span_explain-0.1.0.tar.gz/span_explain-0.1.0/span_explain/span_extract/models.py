from __future__ import annotations

from langchain_core.pydantic_v1 import BaseModel, Field, validator


class ExtractedSpans(BaseModel):
    """The extracted spans/utterances from the text describing the core intent or issue of the customer's query.

    Note: preserving the original text is crucial for accurate location mapping in the transcript.
    """

    spans: list[str] = Field(..., description="The extracted spans/utterances from the text.")

    @validator("spans", each_item=True)
    @classmethod
    def _lowercase_spans(cls, value: str) -> str:
        return value.lower()
