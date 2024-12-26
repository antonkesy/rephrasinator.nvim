"""Top-level package for Rephrasinator."""

__author__ = """Anton Kesy"""
__email__ = "antonkesy@gmail.com"
__version__ = "0.1.0"

from rephrasinator.model import LLMModel, get_model_by_name
from rephrasinator.rephrasinator import get_rephrased_sentence
