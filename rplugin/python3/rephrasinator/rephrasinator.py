from typing import List, Optional

from langchain.chains import LLMChain

from rephrasinator.model import LLMModel, get_langchain_model
from rephrasinator.prompt import get_prompt


def get_rephrased_sentence(
    sentence_to_rephrase: str,
    additional_request: Optional[str] = None,
    model=LLMModel.PHI314B,
) -> Optional[str]:
    prompt = get_prompt(sentence_to_rephrase, additional_request)
    chain = LLMChain(
        llm=get_langchain_model(model),
        prompt=prompt,
    )
    try:
        response = chain.invoke({input: prompt})["text"]
        return response.strip()
    except Exception:
        return None


def get_rephrased_sentences(
    sentence_to_rephrase: str,
    additional_request: Optional[str] = None,
    model=LLMModel.PHI314B,
) -> List[str]:
    prompt = get_prompt(sentence_to_rephrase, additional_request, True)
    chain = LLMChain(
        llm=get_langchain_model(model),
        prompt=prompt,
    )
    # TODO: Stream the responses instead of waiting for all of them
    response = chain.invoke({input: prompt})["text"]
    return _filter_multiple_responses(response)


def _filter_multiple_responses(response: str) -> List[str]:
    lines = response.split("\n")
    stripped_lines = [line.split(". ", 1)[1].strip() for line in lines if line]
    return [line for line in stripped_lines if line]
