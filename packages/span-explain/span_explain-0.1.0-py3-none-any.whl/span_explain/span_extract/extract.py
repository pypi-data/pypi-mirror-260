"""Extract spans from a given text."""


from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import nltk
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from nltk.tokenize import PunktSentenceTokenizer
from thefuzz import process

from span_explain.config import config
from span_explain.utils import read_prompt_from_file

from .models import ExtractedSpans
from .utils import find_query_in_text


if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel

logger = logging.getLogger(__name__)

PROMPTS = {"span_extraction": config.prompt_dir / "span-extraction.txt"}


class SpanExtractor:
    """Extracts spans from a given text."""

    def __init__(
        self,
        model: BaseChatModel,
        custom_prompt: str | None = None,
        few_shot_examples: list[dict[str, str]] | None = None,
    ) -> None:
        """Initialize the SpanExtractor.

        Args:
            model (BaseChatModel): The chat language model to use from LangChain.
            custom_prompt (str, optional): Custom prompt to use instead of the default one. Defaults to None.
        """
        self._llm = model
        self._custom_prompt = custom_prompt
        self.few_shot_examples = few_shot_examples
        self._parser = PydanticOutputParser(pydantic_object=ExtractedSpans)
        self._prompt = self._prepare_llm_messages()
        self._chain = self._prompt | self._llm | self._parser

    def _prepare_llm_messages(self) -> ChatPromptTemplate:
        messages = []
        system_prompt = (
            self._custom_prompt if self._custom_prompt else read_prompt_from_file(PROMPTS["span_extraction"])
        )
        messages.append(SystemMessagePromptTemplate.from_template(system_prompt))

        if self.few_shot_examples:
            formatted_examples = [
                {"input": ex["input"], "output": json.dumps({"spans": ex["output"]}, ensure_ascii=False)}
                for ex in self.few_shot_examples
            ]
            example_prompt = ChatPromptTemplate.from_messages(
                [("human", "{input}"), ("ai", "{output}")],
            )
            few_shot_prompt = FewShotChatMessagePromptTemplate(
                examples=formatted_examples,
                example_prompt=example_prompt,
            )
            messages.append(few_shot_prompt)

        messages.append(HumanMessagePromptTemplate.from_template("{text}"))

        return ChatPromptTemplate(
            messages=messages,
            input_variables=["text"],
            partial_variables={"format_instructions": self._parser.get_format_instructions()},
        )

    def _find_span_in_text(self, text: str, span: str) -> str | None:
        """Finds the span in the text using fuzzy search."""
        # First we need to make sure the text has newlines
        if "\n" not in text:
            nltk.download("punkt", quiet=True)
            tokenizer = PunktSentenceTokenizer()
            text = "\n".join(tokenizer.tokenize(text))

        start_index, end_index, _ = find_query_in_text(span, text, split_on="\n")
        if start_index != -1:
            return text[start_index:end_index]
        return None

    def _find_span_in_sentence(self, sentence: str, span: str, threshold: int = 85) -> str | None:
        """Refines extracted text span in the sentence using fuzzy search."""
        words = sentence.split()
        refined_span = None

        best_match, best_score = None, 0
        for i in range(len(words)):
            for j in range(i, len(words)):
                candidate_span = " ".join(words[i : j + 1])
                score = process.extractOne(span, [candidate_span])[1]
                if score > best_score:
                    best_match, best_score = candidate_span, score

        if best_score >= threshold:
            refined_span = best_match

        return refined_span

    def _fix_misformatted_spans(self, spans: list[str], text: str) -> list[str]:
        incorrect_spans = [span for span in spans if span not in text]
        logger.debug("Incorrect spans: %s", incorrect_spans)
        fixed_spans = []
        for incorrect_span in incorrect_spans:
            logger.debug("Trying to fix span: '%s'", incorrect_span)

            # First we try to find the sentence where the span is located
            sentence = self._find_span_in_text(text, incorrect_span)
            if not sentence:
                logger.warning("Could not find span in text. Skipping...")
                continue

            # Then we try to refine the span in the sentence
            refined_span = self._find_span_in_sentence(sentence, incorrect_span)
            if refined_span:
                logger.debug("Fixed span: '%s'", refined_span)
                fixed_spans.append(refined_span)
            else:
                logger.warning("Could not refine span in sentence. Skipping...")

        return fixed_spans

    def _validate_spans(self, spans: list[str], text: str) -> list[str]:
        """Validate the extracted spans against the original text."""
        correct_spans = [span for span in spans if span in text]
        if len(correct_spans) != len(spans):
            logger.warning("len(correct_spans)=%d != len(spans)=%d", len(correct_spans), len(spans))
            logger.warning("The extracted spans are not formatted correctly. Trying to fix...")
            fixed_spans = self._fix_misformatted_spans(spans, text)
            correct_spans.extend(fixed_spans)

        return correct_spans

    def extract_spans_from_text(self, text: str) -> list[str]:
        """Extracts spans from a given input text."""
        logger.info("Extracting spans from %s..", text[:20])
        output = self._chain.invoke({"text": text})
        logger.debug("Model output: %s", output)

        return self._validate_spans(output.spans, text)
