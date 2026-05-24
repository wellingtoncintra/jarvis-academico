"""
src/agent.py

Orquestrador do JARVIS — tool calling via prompt engineering com chat.completions.

Contexto da decisão:
    A Responses API (responses.create) apresentou comportamento inconsistente
    do Gemma 12B: o modelo ora usava tool_code, ora descrevia a intenção em
    texto livre, sem formato estruturado previsível.
    
    O endpoint chat.completions sem o parâmetro `tools` se mostrou o mais
    estável: com o system prompt descrevendo as tools e pedindo JSON puro,
    o Gemma responde consistentemente com:
        {"tool": "<nome>", "args": {<argumentos>}}

    Vantagens sobre os outros approaches:
    - Sem hacks de parsing (regex, ast, inferência por palavras-chave)
    - Adicionar nova tool = só atualizar TOOLS_PROMPT, sem tocar no loop
    - Funciona em qualquer servidor OpenAI-compat sem flags extras
    - Comportamento previsível e testável

Loop:
    1. System prompt descreve as tools e o formato JSON esperado
    2. LLM responde com JSON → {"tool": "nome", "args": {...}}
    3. Agente detecta, executa a tool e injeta o resultado no contexto
    4. Repete até a LLM responder em texto puro (sem JSON de tool)
    5. Retorna resposta final ao usuário
"""

import json
import re
import os
from loguru import logger
from dotenv import load_dotenv

from src.llm.client import get_llm_client, get_model_name
from src.tools import executar_tool, TOOLS_DEF

load_dotenv()

MAX_ITERACOES = 5


def _construir_tools_prompt() -> str:
    """
    Gera dinamicamente a descrição das tools a partir de TOOLS_DEF.
    Adicionar uma nova tool em src/tools/ automaticamente aparece aqui.
    """
    linhas = [
        "Você tem acesso às ferramentas abaixo. Use-as sempre que a pergunta envolver",
        "agenda, tarefas, materiais de estudo ou planejamento.",
        "",
        "Para chamar uma ferramenta, responda APENAS com JSON neste formato:",
        '{"tool": "<nome_da_ferramenta>", "args": {<argumentos>}}',
        "",
        "Não coloque texto antes ou depois do JSON ao chamar uma ferramenta.",
        "Após receber o resultado, elabore a resposta final em texto normal.",
        "",
        "FERRAMENTAS DISPONÍVEIS",
        "=" * 54,
    ]

    for i, tool_def in enumerate(TOOLS_DEF, 1):
        # Suporta tanto formato Chat Completions (com wrapper) quanto flat
        fn       = tool_def.get("function", tool_def)
        nome     = fn["name"]
        desc     = fn["description"]
        params   = fn.get("parameters", {}).get("properties", {})
        required = fn.get("parameters", {}).get("required", [])

        linhas.append(f"\n{i}. {nome}")
        linhas.append(f"   {desc}")

        if params:
            linhas.append("   Argumentos:")
            for param_nome, param_info in params.items():
                tipo      = param_info.get("type", "string")
                param_desc = param_info.get("description", "")
                enum      = param_info.get("enum")
                obrig     = " (obrigatório)" if param_nome in required else " (opcional)"
                enum_str  = f" — valores: {enum}" if enum else ""
                linhas.append(f"     - {param_nome} ({tipo}{obrig}): {param_desc}{enum_str}")

        # Monta exemplo com o primeiro campo required ou o primeiro param
        exemplo_args = {}
        for param_nome, param_info in params.items():
            if param_nome in required:
                enum = param_info.get("enum")
                exemplo_args[param_nome] = enum[0] if enum else f"<{param_nome}>"
        if exemplo_args:
            linhas.append(f'   Exemplo: {{"tool": "{nome}", "args": {json.dumps(exemplo_args, ensure_ascii=False)}}}')

    linhas.append("\n" + "=" * 54)
    return "\n".join(linhas)


SYSTEM_PROMPT = f"""\
Você é o JARVIS Acadêmico, um assistente pessoal para estudantes universitários.

{_construir_tools_prompt()}

Diretrizes gerais:
- Sempre consulte as ferramentas antes de responder sobre agenda, tarefas ou materiais.
- Quando adicionar algo, confirme ao usuário o que foi cadastrado.
- Para planos de estudo, chame planejar_estudos primeiro e use o contexto retornado.
- Responda sempre em português brasileiro, de forma clara e objetiva.
- Se uma ferramenta retornar erro, explique o problema e sugira alternativa.
"""

# ── Detector de tool call na resposta ────────────────────────────────────────

_TOOL_RE = re.compile(
    r'\{\s*"tool"\s*:\s*"([^"]+)"\s*,\s*"args"\s*:\s*(\{.*?\})\s*\}',
    re.DOTALL,
)


def _extrair_tool_call(texto: str) -> dict | None:
    """
    Extrai {"tool": str, "args": dict} do texto da LLM.
    Retorna None se o texto não for um tool call.
    """
    texto = texto.strip()

    # Tentativa 1: texto inteiro é JSON puro
    try:
        parsed = json.loads(texto)
        if isinstance(parsed, dict) and "tool" in parsed and "args" in parsed:
            return parsed
    except json.JSONDecodeError:
        pass

    # Tentativa 2: JSON embutido no texto
    match = _TOOL_RE.search(texto)
    if match:
        try:
            parsed = json.loads(match.group(0))
            if "tool" in parsed and "args" in parsed:
                return parsed
        except json.JSONDecodeError:
            pass

    return None


# ── Orquestrador ──────────────────────────────────────────────────────────────

def processar_mensagem(
    mensagem: str,
    historico: list[dict] = None,
) -> dict:
    """
    Processa uma mensagem com tool calling via prompt engineering.

    Parâmetros:
        mensagem  : texto do usuário
        historico : [{"role": "user"|"assistant", "content": str}]
                    Se None, inicia conversa nova.

    Retorna:
        {
            "resposta":   str,
            "tool_logs":  list[dict],
            "historico":  list[dict],
        }
    """
    client = get_llm_client()
    model  = get_model_name()

    if historico is None:
        historico = []

    mensagens = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + historico
        + [{"role": "user", "content": mensagem}]
    )

    tool_logs = []
    iteracoes = 0

    while iteracoes < MAX_ITERACOES:
        iteracoes += 1
        logger.info(f"[agente] Iteração {iteracoes} — {len(mensagens)} mensagens")

        response = client.chat.completions.create(
            model=model,
            messages=mensagens,
        )

        texto = (response.choices[0].message.content or "").strip()
        logger.debug(f"[agente] Resposta bruta: {texto[:300]}")

        tool_call = _extrair_tool_call(texto)

        # ── Resposta final ────────────────────────────────────────────────────
        if tool_call is None:
            logger.info(f"[agente] Resposta final: {len(texto)} caracteres")

            historico_atualizado = historico + [
                {"role": "user",      "content": mensagem},
                {"role": "assistant", "content": texto},
            ]
            return {
                "resposta":  texto,
                "tool_logs": tool_logs,
                "historico": historico_atualizado,
            }

        # ── Executa tool call ─────────────────────────────────────────────────
        nome = tool_call["tool"]
        args = tool_call["args"]
        logger.info(f"[agente] Tool: {nome} | args: {json.dumps(args, ensure_ascii=False)}")

        try:
            resultado = executar_tool(nome, args)
            #logger.log(resultado)
            status    = "ok"
        except Exception as e:
            resultado = {"erro": str(e)}
            status    = "erro"
            logger.error(f"[agente] Erro na tool '{nome}': {e}")

        tool_logs.append({"tool": nome, "args": args, "resultado": resultado, "status": status})

        # Injeta resultado no contexto usando apenas roles user/assistant
        mensagens.append({"role": "assistant", "content": texto})
        mensagens.append({
            "role": "user",
            "content": (
                f"[Resultado da ferramenta '{nome}']\n"
                + json.dumps(resultado, ensure_ascii=False, indent=2)
                + "\n\nAgora responda ao usuário em português com base nesse resultado."
            ),
        })

    # ── Proteção ──────────────────────────────────────────────────────────────
    logger.warning("[agente] Limite de iterações atingido.")
    return {
        "resposta":  "Não consegui processar completamente. Tente reformular a pergunta.",
        "tool_logs": tool_logs,
        "historico": historico + [{"role": "user", "content": mensagem}],
    }