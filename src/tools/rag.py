"""
src/tools/rag.py

Tool de busca nos materiais acadêmicos indexados (FAISS + BM25).
Chama src/rag/retriever.py que já faz recuperação + geração.
"""

from src.rag.retriever import responder


# ── Definição (schema para a LLM) ────────────────────────────────────────────

BUSCAR_MATERIAL_RAG = {
    "type": "function",
    "function": {
        "name": "buscar_material_rag",
        "description": (
            "Busca informações nos materiais de estudo do estudante (PDFs). "
            "Use quando o usuário pedir explicação de um conceito, resumo de um conteúdo, "
            "ou qualquer pergunta que possa ser respondida a partir dos documentos indexados."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "pergunta": {
                    "type": "string",
                    "description": (
                        "A pergunta ou tópico a buscar nos materiais. "
                        "Reformule como uma pergunta clara se o usuário fez um pedido vago."
                    ),
                },
                "metodo": {
                    "type": "string",
                    "enum": ["hibrido", "semantico", "bm25"],
                    "description": (
                        "'hibrido' (padrão) = combina busca semântica e lexical, melhor para a maioria dos casos. "
                        "'semantico' = busca por significado, bom para paráfrases. "
                        "'bm25' = busca por palavras exatas, bom para termos técnicos específicos."
                    ),
                },
                "k": {
                    "type": "integer",
                    "description": "Número de trechos a recuperar (padrão: 3, máximo recomendado: 5).",
                },
            },
            "required": ["pergunta"],
        },
    },
}


# ── Implementação ─────────────────────────────────────────────────────────────

def buscar_material_rag(
    pergunta: str,
    metodo: str = "hibrido",
    k: int = 3,
) -> dict:
    """
    Recupera trechos relevantes dos documentos indexados e gera uma resposta.

    Retorna:
        {
            "resposta": str,   ← texto gerado pelo Gemma com base nos chunks
            "chunks":  [...],  ← trechos recuperados (id, texto, fonte, score, metodo)
            "metodo":  str,
        }

    Em caso de erro (ex: índices não existem):
        {
            "erro": str,
            "resposta": str    ← mensagem amigável para repassar ao usuário
        }
    """
    try:
        resultado = responder(pergunta=pergunta, metodo=metodo, k=k)
        return resultado
    except FileNotFoundError as e:
        msg = (
            "Os materiais de estudo ainda não foram indexados. "
            "Acesse a aba 'Materiais RAG' na interface e faça o upload dos documentos."
        )
        return {"erro": str(e), "resposta": msg, "chunks": []}
    except Exception as e:
        msg = f"Erro ao buscar nos materiais: {e}"
        return {"erro": str(e), "resposta": msg, "chunks": []}
