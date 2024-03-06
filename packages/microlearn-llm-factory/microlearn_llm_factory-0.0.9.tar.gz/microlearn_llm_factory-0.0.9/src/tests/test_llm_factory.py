"""
Test LLMFactory

Usage:
    pytest src/tests/test_llm_factory.py -v --log-cli-level INFO
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_factory.llm_factory import LLMFactory
from langchain_openai import ChatOpenAI
import pytest
from dotenv import load_dotenv


load_dotenv(override=True)


@pytest.fixture
def llm_factory():
    return LLMFactory()


def test_build_llm(llm_factory: LLMFactory):
    llm = llm_factory.build_llm(
        LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="model_name",
        temperature=0.5,
        max_tokens=10,
    )
    assert isinstance(llm, ChatOpenAI)

def test_build_llm_w_api_key(llm_factory: LLMFactory):
    llm = llm_factory.build_llm(
        LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="model_name",
        temperature=0.5,
        max_tokens=10,
        api_key="1234",
    )
    assert isinstance(llm, ChatOpenAI)

def test_build_llm_w_pl_tags(llm_factory: LLMFactory):
    llm = llm_factory.build_llm(
        LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="model_name",
        temperature=0.5,
        max_tokens=10,
        pl_tags=["test"],
    )
    assert isinstance(llm, ChatOpenAI)


def test_build_llm_default(llm_factory: LLMFactory):
    llm = llm_factory.build_llm_default()
    assert isinstance(llm, ChatOpenAI)
