"""
src/tools/__init__.py

Exporta todas as tools prontas para o agente consumir.

Uso no agent.py:
    from src.tools import TOOLS_DEF, executar_tool
"""

from .agenda import CONSULTAR_AGENDA, consultar_agenda
from .agenda import ADICIONAR_AGENDA, adicionar_agenda
from .tarefas import GERENCIAR_TAREFAS, gerenciar_tarefas
from .rag import BUSCAR_MATERIAL_RAG, buscar_material_rag
from .planejamento import PLANEJAR_ESTUDOS, planejar_estudos

import json

# Lista de schemas enviada à LLM no parâmetro `tools`
TOOLS = [
    CONSULTAR_AGENDA,
    ADICIONAR_AGENDA,
    GERENCIAR_TAREFAS,
    BUSCAR_MATERIAL_RAG,
    PLANEJAR_ESTUDOS,
]

# Mapa nome → função Python
_REGISTRY = {
    "consultar_agenda":    consultar_agenda,
    "adicionar_agenda":    adicionar_agenda,
    "gerenciar_tarefas":   gerenciar_tarefas,
    "buscar_material_rag": buscar_material_rag,
    "planejar_estudos":    planejar_estudos,
}


def executar_tool(nome: str, argumentos_json: str) -> dict:
    """
    Recebe o nome da tool e os argumentos como JSON string
    (formato retornado pela OpenAI API) e executa a função correspondente.

    Retorna o resultado como dicionário.
    Levanta ValueError se o nome não for reconhecido.

    Uso:
        resultado = executar_tool("gerenciar_tarefas", '{"acao": "listar_pendentes"}')
    """
    fn = _REGISTRY.get(nome)
    if fn is None:
        raise ValueError(
            f"Tool '{nome}' não encontrada. "
            f"Disponíveis: {list(_REGISTRY.keys())}"
        )

    args = json.loads(argumentos_json) if isinstance(argumentos_json, str) else argumentos_json
    return fn(**args)
