"""
src/agent.py

Orquestrador do JARVIS usando a Responses API.

Nota: A documentação do professor indica chat.completions, porém esse endpoint
não aceita tool calling no vLLM sem --enable-auto-tool-choice e
--tool-call-parser. A Responses API suporta tools nativamente no servidor
disponibilizado e foi adotada por isso.

Loop:
    1. Envia input_list + tools para client.responses.create
    2. Itera response.output buscando itens type="function_call"
    3. Executa cada tool e devolve como "function_call_output"
    4. Repete até não haver function_calls
    5. Retorna response.output_text ao usuário
"""

import json
import os
from loguru import logger
from dotenv import load_dotenv

from src.llm.client import get_llm_client, get_model_name
from src.tools import TOOLS_DEF, executar_tool

load_dotenv()

MAX_ITERACOES = 5

SYSTEM_PROMPT = """\
Você é o JARVIS Acadêmico, um assistente pessoal para estudantes universitários.

Você tem acesso a ferramentas para:
- Consultar e adicionar eventos na agenda acadêmica
- Gerenciar lista de tarefas (listar, adicionar, concluir)
- Buscar conteúdo nos materiais de estudo indexados (RAG)
- Montar planos de estudo combinando agenda, tarefas e materiais

Diretrizes:
- Sempre use as ferramentas antes de responder sobre agenda, tarefas ou materiais.
- Quando adicionar algo, confirme ao usuário o que foi cadastrado.
- Para planos de estudo, chame planejar_estudos primeiro e elabore o plano com o contexto.
- Responda sempre em português brasileiro, de forma clara e objetiva.
- Se uma ferramenta retornar erro, explique e sugira alternativa.
"""


def processar_mensagem(
    mensagem: str,
    historico: list[dict] = None,
) -> dict:
    """
    Processa uma mensagem do usuário com tool calling via Responses API.

    Parâmetros:
        mensagem  : texto do usuário
        historico : mensagens anteriores [{"role": "user"|"assistant", "content": str}]
                    Se None, inicia conversa nova.

    Retorna:
        {
            "resposta":   str,         — texto final para o usuário
            "tool_logs":  list[dict],  — cada tool chamada com args, resultado e status
            "historico":  list[dict],  — histórico atualizado para a próxima chamada
        }
    """
    client = get_llm_client()
    model  = get_model_name()

    if historico is None:
        historico = []

    # input_list acumula tudo entre iterações: histórico + mensagem + outputs de tools
    input_list = historico + [{"role": "user", "content": mensagem}]

    tool_logs = []
    iteracoes = 0

    while iteracoes < MAX_ITERACOES:
        iteracoes += 1
        logger.info(f"[agente] Iteração {iteracoes} — {len(input_list)} itens no input")

        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            tools=TOOLS_DEF,
            input=input_list,
        )

        # Acumula os outputs desta rodada para a próxima iteração
        input_list += response.output

        function_calls = [item for item in response.output if item.type == "function_call"]

        # ── Sem tool calls → resposta final ──────────────────────────────────
        if not function_calls:
            resposta = response.output_text
            logger.info(f"[agente] Resposta final: {len(resposta)} caracteres")

            historico_atualizado = historico + [
                {"role": "user",      "content": mensagem},
                {"role": "assistant", "content": resposta},
            ]

            return {
                "resposta":  resposta,
                "tool_logs": tool_logs,
                "historico": historico_atualizado,
            }

        # ── Executa cada tool call ────────────────────────────────────────────
        for item in function_calls:
            nome = item.name
            args = item.arguments  # string JSON

            logger.info(f"[agente] Tool: {nome} | args: {args}")

            try:
                resultado = executar_tool(nome, args)
                status    = "ok"
            except Exception as e:
                resultado = {"erro": str(e)}
                status    = "erro"
                logger.error(f"[agente] Erro na tool '{nome}': {e}")

            tool_logs.append({
                "tool":      nome,
                "args":      json.loads(args) if isinstance(args, str) else args,
                "resultado": resultado,
                "status":    status,
            })

            # Devolve resultado no formato da Responses API
            input_list.append({
                "type":    "function_call_output",
                "call_id": item.call_id,
                "output":  json.dumps(resultado, ensure_ascii=False),
            })

    # ── Proteção: limite atingido ─────────────────────────────────────────────
    logger.warning("[agente] Limite de iterações atingido.")
    return {
        "resposta":  "Não consegui processar completamente. Tente reformular a pergunta.",
        "tool_logs": tool_logs,
        "historico": historico + [{"role": "user", "content": mensagem}],
    }
