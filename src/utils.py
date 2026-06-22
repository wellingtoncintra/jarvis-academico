"""
src/utils.py

Utilitários compartilhados do JARVIS Acadêmico.

Centraliza lógica usada em mais de um módulo para evitar duplicação.
Atualmente: extração robusta de JSON de respostas da LLM.
"""

import json
import re


def extrair_json(texto: str) -> dict | None:
    """
    Extrai o primeiro objeto JSON de uma resposta da LLM, de forma tolerante.

    O Gemma às vezes responde com JSON puro, às vezes embrulha em cercas de
    código markdown (```json ... ```), e às vezes mistura o JSON com texto ao
    redor. Esta função cobre os três casos, na ordem:

        1. Remove cercas de código markdown, se houver.
        2. Tenta parsear o texto inteiro como JSON.
        3. Como fallback, procura o primeiro bloco {...} embutido e tenta parseá-lo.

    Retorna o dict parseado, ou None se nada de JSON válido for encontrado.

    Esta é a base de parsing usada tanto pelo agente (que depois valida as
    chaves específicas de um tool call) quanto pelas funcionalidades de
    aprendizado (que esperam um objeto genérico).
    """
    if not texto:
        return None

    texto = texto.strip()

    # Passo 1 — remove cercas de código markdown (```json ... ``` ou ``` ... ```)
    texto = re.sub(r"^```(?:json)?|```$", "", texto, flags=re.MULTILINE).strip()

    # Passo 2 — texto inteiro é JSON puro
    try:
        parsed = json.loads(texto)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Passo 3 — fallback: primeiro bloco {...} embutido no texto
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return None

    return None
