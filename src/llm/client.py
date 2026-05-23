"""
Nota: A documentação oficial indica chat.completions, porém esse endpoint
não aceita tool calling. A Responses API (responses.create)
funciona com tools no servidor disponibilizado e foi adotada por isso.
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
    """
    Envia mensagem simples sem tools — usado pelo módulo RAG para geração.
    """
    client     = get_llm_client()
    input_list = []

    if system_prompt:
        input_list.append({"role": "user", "content": system_prompt})

    input_list.append({"role": "user", "content": mensagem})

    response = client.responses.create(
        model=get_model_name(),
        input=input_list,
    )
    return response.output_text
