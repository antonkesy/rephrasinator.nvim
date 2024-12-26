from enum import Enum

from langchain_community.llms import Ollama
from langchain_core.language_models.chat_models import BaseChatModel

# from langchain_openai import ChatOpenAI


# https://platform.openai.com/docs/models/model-endpoint-compatibility
# https://github.com/ollama/ollama?tab=readme-ov-file#model-library
# https://ollama.com/library
class LLMModel(str, Enum):
    # GPT
    # GPTTurbo = "gpt-3.5-turbo"
    # GPT4 = "gpt-4"
    # PHI
    PHI314B = "phi3:14b"
    # LAMA
    LLAMA3_3_70B = "llama3.3:70b"
    LLAMA3_2_1B = "llama3.2:1b"
    LLAMA3_2_3B = "llama3.2:3b"
    # MISTRAL
    MISTRAL_7B = "mistral:7b"
    # GEMMA
    GEMMA_7B = "gemma:7b"


def get_model_by_name(model_name: str) -> LLMModel:
    for model in LLMModel:
        if model_name == model.value:
            return model
    raise ValueError(f"Model {model_name} not found")


def get_langchain_model(model: LLMModel) -> BaseChatModel:
    match model:
        # case LLMModel.GPTTurbo | LLMModel.GPT4:
        #     ai_model = ChatOpenAI(temperature=0, model=model.value)
        case _:
            ai_model = Ollama(model=model.value)
    return ai_model
