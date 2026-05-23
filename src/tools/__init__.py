"""
src/tools/__init__.py

Exporta TOOLS_DEF no formato Responses API e o dispatcher executar_tool.
"""

from .agenda       import CONSULTAR_AGENDA_DEF,    consultar_agenda
from .agenda       import ADICIONAR_AGENDA_DEF,    adicionar_agenda
from .tarefas      import GERENCIAR_TAREFAS_DEF,   gerenciar_tarefas
from .rag          import BUSCAR_MATERIAL_RAG_DEF,  buscar_material_rag
from .planejamento import PLANEJAR_ESTUDOS_DEF,    planejar_estudos

import json

TOOLS_DEF = [
    CONSULTAR_AGENDA_DEF,
    ADICIONAR_AGENDA_DEF,
    GERENCIAR_TAREFAS_DEF,
    BUSCAR_MATERIAL_RAG_DEF,
    PLANEJAR_ESTUDOS_DEF,
]

_REGISTRY = {
    "consultar_agenda":    consultar_agenda,
    "adicionar_agenda":    adicionar_agenda,
    "gerenciar_tarefas":   gerenciar_tarefas,
    "buscar_material_rag": buscar_material_rag,
    "planejar_estudos":    planejar_estudos,
}


def executar_tool(nome: str, argumentos) -> dict:
    """
    Executa a tool pelo nome.
    `argumentos` pode ser dict ou JSON string
    (a Responses API retorna item.arguments como string).
    """
    fn = _REGISTRY.get(nome)
    if fn is None:
        raise ValueError(f"Tool '{nome}' não encontrada. Disponíveis: {list(_REGISTRY.keys())}")
    args = json.loads(argumentos) if isinstance(argumentos, str) else argumentos
    return fn(**args)
