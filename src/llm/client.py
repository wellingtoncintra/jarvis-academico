"""
src/llm/client.py

Cliente OpenAI usando chat.completions — endpoint estável no servidor do professor.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_llm_client() -> OpenAI:
    api_key  = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    if not api_key:
        raise ValueError("LLM_API_KEY não encontrada no .env.")
    if not base_url:
        raise ValueError("LLM_BASE_URL não encontrada no .env.")
    return OpenAI(api_key=api_key, base_url=base_url)


def get_model_name() -> str:
    return os.getenv("LLM_MODEL_NAME")


def chat(mensagem: str, system_prompt: str = None) -> str:
    """Chamada simples sem tools — usada pelo módulo RAG para geração."""
    client   = get_llm_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": mensagem})

    response = client.chat.completions.create(
        model=get_model_name(),
        messages=messages,
    )
    return response.choices[0].message.content