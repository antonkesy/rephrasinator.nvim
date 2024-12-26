from typing import Optional

from langchain.prompts import PromptTemplate


def get_prompt(
    sentence_to_rephrase: str,
    additional_request: Optional[str] = None,
    multiple_responses: bool = False,
) -> PromptTemplate:
    return PromptTemplate.from_template(
        _get_prompt_text(sentence_to_rephrase, additional_request, multiple_responses)
    )


def _get_prompt_text(
    sentence_to_rephrase: str,
    additional_request: Optional[str] = None,
    multiple_responses: bool = False,
) -> str:
    return (
        f"""
            Rephrase the following sentence by only changing some words: {sentence_to_rephrase}.
            """
        + "Give only one possible answer, no other text."
        if not multiple_responses
        else "Number them from 1 to 10 in style: '1. <YOUR ANSWER>'"
        + """
            No extra punctuation or information.
            Don't add any extra information.
            Don't add extra newlines.
            Keep the same meaning.
            """
        + (
            f"And please also: {additional_request}."
            if additional_request is not None
            else ""
        )
    )
