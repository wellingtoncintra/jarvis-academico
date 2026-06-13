"""
src/tools/rag.py — Responses API format.

NOTA DE PERFORMANCE:
    O import de `src.rag.retriever` é feito DENTRO de buscar_material_rag()
    (lazy import), e não no topo do módulo. Isso evita que apenas importar a
    *definição* da tool (BUSCAR_MATERIAL_RAG_DEF) arraste todo o stack de RAG
    (sentence_transformers + torch + faiss) na cadeia:
        interface/chat.py → src.agent → src.tools → tools.rag → retriever
    Com o import no topo, abrir a aba Chat carregava o PyTorch inteiro só para
    desenhar a tela. Com o lazy import, o stack pesado só sobe na primeira
    pergunta de RAG de fato — junto do carregamento dos pesos, que já era lazy.
"""


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
    # Lazy import: só carrega sentence_transformers/faiss quando o RAG é usado.
    from src.rag.retriever import responder
    try:
        return responder(pergunta=pergunta, metodo=metodo, k=k)
    except FileNotFoundError as e:
        msg = "Os materiais ainda não foram indexados. Faça upload na aba Materiais RAG."
        return {"erro": str(e), "resposta": msg, "chunks": []}
    except Exception as e:
        return {"erro": str(e), "resposta": f"Erro ao buscar nos materiais: {e}", "chunks": []}
