from openai import OpenAI
import os
from dotenv import load_dotenv
 
load_dotenv()

def get_llm_client() -> OpenAI:
    """
    Retorna um cliente configurado com as credenciais do .env.
    Levanta um erro claro se alguma variável estiver faltando.
    """
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
 
    if not api_key:
        raise ValueError(
            "LLM_API_KEY não encontrada. "
            "Verifique se o .env existe e está preenchido."
        )
    if not base_url:
        raise ValueError(
            "LLM_BASE_URL não encontrada. "
            "Verifique se o .env existe e está preenchido."
        )
 
    return OpenAI(api_key=api_key, base_url=base_url)

def chat(mensagem: str, system_prompt: str = None) -> str:
    """
    Envia uma mensagem para o Gemma e retorna a resposta como string.
 
    Exemplo de uso:
        from src.llm.client import chat
        resposta = chat("Explique o que é RAG.")
        print(resposta)
    """
    client = get_llm_client()
 
    messages = []
 
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
 
    messages.append({"role": "user", "content": mensagem})
 
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=messages,
        max_tokens=1000,
    )
 
    return response.choices[0].message.content

def get_model_name() -> str:
    return os.getenv("LLM_MODEL_NAME")