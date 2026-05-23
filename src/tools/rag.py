"""
src/tools/rag.py — Responses API format.
"""

from src.rag.retriever import responder


BUSCAR_MATERIAL_RAG_DEF = {
    "type": "function",
    "name": "buscar_material_rag",
    "description": (
        "Busca informações nos materiais de estudo do estudante (PDFs, notas, textos). "
        "Use quando o usuário pedir explicação de um conceito, resumo de conteúdo, "
        "ou qualquer pergunta respondível pelos documentos indexados."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "pergunta": {
                "type": "string",
                "description": "A pergunta ou tópico a buscar nos materiais.",
            },
            "metodo": {
                "type": "string",
                "enum": ["hibrido", "semantico", "bm25"],
                "description": "'hibrido' (padrão) combina semântico e lexical.",
            },
            "k": {
                "type": "integer",
                "description": "Número de trechos a recuperar (padrão: 3).",
            },
        },
        "required": ["pergunta"],
    },
}


def buscar_material_rag(pergunta: str, metodo: str = "hibrido", k: int = 3) -> dict:
    try:
        return responder(pergunta=pergunta, metodo=metodo, k=k)
    except FileNotFoundError as e:
        msg = "Os materiais ainda não foram indexados. Faça upload na aba Materiais RAG."
        return {"erro": str(e), "resposta": msg, "chunks": []}
    except Exception as e:
        return {"erro": str(e), "resposta": f"Erro ao buscar nos materiais: {e}", "chunks": []}
