"""
src/agent.py

Orquestrador do JARVIS — implementa o loop de tool calling:

    usuário → agente → LLM
                        ↓ "chame tool X"
              agente → tool X → resultado
                        ↓
              agente → LLM + resultado
                        ↓ resposta final
    usuário ← agente

O loop roda até a LLM devolver uma mensagem de texto sem tool calls,
ou até atingir MAX_ITERACOES (proteção contra loops infinitos).
"""

import json
from loguru import logger

from src.llm.client import get_llm_client
from src.tools import TOOLS, executar_tool

import os
from dotenv import load_dotenv

load_dotenv()

MAX_ITERACOES = 5  # proteção contra loop infinito

SYSTEM_PROMPT = """Você é o JARVIS Acadêmico, um assistente pessoal para estudantes universitários.

Você tem acesso a ferramentas para:
- Consultar e adicionar eventos na agenda
- Gerenciar lista de tarefas (listar, adicionar, concluir)
- Buscar conteúdo nos materiais de estudo indexados (RAG)
- Montar planos de estudo combinando agenda e tarefas

Diretrizes:
- Sempre use as ferramentas disponíveis antes de responder perguntas sobre agenda, tarefas ou materiais.
- Quando o usuário pedir para adicionar algo, use a tool adequada e confirme o que foi feito.
- Para planos de estudo, chame 'planejar_estudos' para obter o contexto e depois elabore o plano.
- Responda sempre em português brasileiro, de forma clara e objetiva.
- Se uma ferramenta retornar erro, explique ao usuário o que aconteceu e sugira uma alternativa.
"""


def processar_mensagem(
    mensagem: str,
    historico: list[dict] = None,
) -> dict:
    """
    Processa uma mensagem do usuário com suporte a tool calling.

    Parâmetros:
        mensagem  : texto enviado pelo usuário
        historico : lista de mensagens anteriores no formato OpenAI
                    [{"role": "user"|"assistant", "content": "..."}]
                    Opcional — se None, começa uma conversa nova.

    Retorna:
        {
            "resposta":   str,          ← texto final para o usuário
            "tool_logs":  list[dict],   ← registro de todas as tools chamadas
            "historico":  list[dict],   ← histórico atualizado (para próxima chamada)
        }
    """
    client = get_llm_client()
    model  = os.getenv("LLM_MODEL_NAME")

    # ── Monta o histórico inicial ─────────────────────────────────────────────
    if historico is None:
        historico = []

    mensagens = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + historico
        + [{"role": "user", "content": mensagem}]
    )

    tool_logs  = []
    iteracoes  = 0

    # ── Loop principal ────────────────────────────────────────────────────────
    while iteracoes < MAX_ITERACOES:
        iteracoes += 1
        logger.info(f"[agente] Iteração {iteracoes} — enviando {len(mensagens)} mensagens")

        try:
            response = client.chat.completions.create(
                model=model,
                messages=mensagens,
                tools=TOOLS,
                # Sem tool_choice — deixa o servidor usar o padrão dele
            )
        except Exception as e:
                logger.warning(f"{e}")
                response = client.chat.completions.create(
                    model=model,
                    messages=mensagens,
                )

        choice  = response.choices[0]
        message = choice.message

        # ── Resposta final (sem tool call) ────────────────────────────────────
        if choice.finish_reason == "stop" or not message.tool_calls:
            resposta = message.content or ""
            logger.info(f"[agente] Resposta final: {len(resposta)} caracteres")

            # Atualiza historico com o par usuário/assistente
            historico_atualizado = (
                historico
                + [{"role": "user",      "content": mensagem}]
                + [{"role": "assistant", "content": resposta}]
            )

            return {
                "resposta":  resposta,
                "tool_logs": tool_logs,
                "historico": historico_atualizado,
            }

        # ── A LLM pediu tool calls ────────────────────────────────────────────
        # Adiciona a mensagem do assistente (com tool_calls) ao contexto
        mensagens.append(message)

        for tc in message.tool_calls:
            nome      = tc.function.name
            args_json = tc.function.arguments

            logger.info(f"[agente] Tool chamada: {nome} | args: {args_json}")

            # Executa a tool
            try:
                resultado = executar_tool(nome, args_json)
                status    = "ok"
            except Exception as e:
                resultado = {"erro": str(e)}
                status    = "erro"
                logger.error(f"[agente] Erro na tool {nome}: {e}")

            # Registra o log
            tool_logs.append({
                "tool":      nome,
                "args":      json.loads(args_json) if isinstance(args_json, str) else args_json,
                "resultado": resultado,
                "status":    status,
            })

            # Devolve resultado para a LLM no próximo turno
            mensagens.append({
                "role":         "tool",
                "tool_call_id": tc.id,
                "content":      json.dumps(resultado, ensure_ascii=False),
            })

    # ── Segurança: limite de iterações atingido ───────────────────────────────
    logger.warning("[agente] Limite de iterações atingido sem resposta final.")
    return {
        "resposta":  "Não consegui processar sua solicitação completamente. Por favor, tente reformular.",
        "tool_logs": tool_logs,
        "historico": historico + [{"role": "user", "content": mensagem}],
    }
