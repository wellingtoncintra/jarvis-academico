# src/storage/__init__.py
# Exporta tudo do módulo storage de um lugar só.
# Assim o resto do projeto importa assim:
#   from src.storage import adicionar_tarefa, listar_eventos_hoje

from .database import get_connection, get_cursor, criar_tabelas
from .agenda import (
    adicionar_evento,
    buscar_evento_por_id,
    listar_eventos_por_data,
    listar_eventos_por_periodo,
    listar_eventos_hoje,
    listar_eventos_semana,
    listar_todos_eventos,
    atualizar_evento,
    remover_evento,
)
from .tarefas import (
    adicionar_tarefa,
    buscar_tarefa_por_id,
    listar_tarefas_pendentes,
    listar_tarefas_concluidas,
    listar_todas_tarefas,
    concluir_tarefa,
    reabrir_tarefa,
    atualizar_tarefa,
    remover_tarefa,
)
