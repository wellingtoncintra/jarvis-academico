"""
src/logging_config.py

Configuração central de logging do JARVIS Acadêmico.

Dois fluxos distintos, com propósitos diferentes:

  1. Log de aplicação (loguru → logs/jarvis.log)
     Diagnóstico técnico: fluxo do agente, pipeline RAG, erros.
     Todas as chamadas logger.* já espalhadas pelo projeto passam a
     gravar aqui automaticamente assim que setup_logging() roda — sem
     precisar tocar em nenhuma delas.

  2. Log de tool calling (JSONL → logs/tool_calls.jsonl)
     Registro estruturado exigido pela especificação (ferramenta,
     entrada, saída, status). Uma linha JSON por chamada, fácil de
     reprocessar posteriormente (ex.: análise de erros).

O diretório logs/ é criado em runtime (está no .gitignore, não é versionado).
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from loguru import logger

# ── Caminhos ──────────────────────────────────────────────────────────────────
LOG_DIR        = Path("logs")
APP_LOG_PATH   = LOG_DIR / "jarvis.log"
TOOL_LOG_PATH  = LOG_DIR / "tool_calls.jsonl"

# Guarda para tornar setup_logging() idempotente (Streamlit reexecuta o módulo).
_configurado = False


def setup_logging() -> None:
    """
    Configura o sink de arquivo do loguru. Idempotente: chamadas repetidas
    (Streamlit reroda o script a cada interação) não duplicam sinks.

    Mantém o sink de console (stderr) que já existia e acrescenta o arquivo
    rotacionado em logs/jarvis.log.
    """
    global _configurado
    if _configurado:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Remove o sink default e reconstrói: console + arquivo.
    logger.remove()

    # Console (mantém o comportamento anterior).
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    )

    # Arquivo de aplicação, com rotação e retenção.
    logger.add(
        APP_LOG_PATH,
        level="DEBUG",
        rotation="5 MB",
        retention="7 days",
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    )

    _configurado = True
    logger.info("Logging configurado: console + arquivo (logs/jarvis.log).")


def registrar_tool_log(tool: str, args: dict, resultado, status: str) -> dict:
    """
    Persiste um registro estruturado de tool calling em logs/tool_calls.jsonl
    e retorna o registro (com timestamp ISO) para uso na UI.

    Uma linha JSON por chamada:
        {"timestamp": "...", "tool": "...", "args": {...},
         "resultado": ..., "status": "ok"|"erro"}

    A falha ao gravar o log nunca interrompe o fluxo do agente — apenas
    emite um warning pelo loguru.
    """
    registro = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "tool":      tool,
        "args":      args,
        "resultado": resultado,
        "status":    status,
    }

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOOL_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.warning(f"Falha ao persistir tool log em {TOOL_LOG_PATH}: {e}")

    return registro
