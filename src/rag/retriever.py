"""
src/rag/retriever.py

Responsável por:
  1. Buscar chunks relevantes para uma pergunta (BM25, semântico ou híbrido)
  2. Montar o prompt com os chunks recuperados
  3. Enviar para o Gemma e retornar a resposta

É o módulo que o agente chama diretamente via tool calling.
"""

import re
import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer

from .embedder import carregar_indices, indices_existem, MODELO_EMBEDDING
from src.llm.client import get_llm_client, get_model_name

# Modelo de embeddings — mesmo usado na indexação
_modelo: SentenceTransformer | None = None

# Índices carregados em memória (lazy loading)
_chunks         = None
_indice_faiss   = None
_indice_bm25    = None
_matriz         = None


def _get_modelo() -> SentenceTransformer:
    global _modelo
    if _modelo is None:
        _modelo = SentenceTransformer(MODELO_EMBEDDING)
    return _modelo


def _carregar_se_necessario() -> None:
    """Carrega os índices do disco na primeira chamada."""
    global _chunks, _indice_faiss, _indice_bm25, _matriz

    if _chunks is None:
        if not indices_existem():
            raise FileNotFoundError(
                "Índices RAG não encontrados. "
                "Execute 'python src/rag/indexer.py' primeiro."
            )
        _chunks, _indice_faiss, _indice_bm25, _matriz = carregar_indices()


def _tokenizar(texto: str) -> list[str]:
    return re.findall(r"\w+", texto.lower())


def _normalizar(v: np.ndarray) -> np.ndarray:
    """Normaliza um vetor para o intervalo [0, 1]."""
    v = np.array(v, dtype="float32")
    delta = float(v.max() - v.min())
    if delta < 1e-9:
        return np.zeros_like(v)
    return (v - v.min()) / delta


# ── Funções de busca ──────────────────────────────────────────────────────────

def buscar_bm25(pergunta: str, k: int = 3) -> list[dict]:
    """
    Busca lexical — pontua chunks pela frequência dos termos da pergunta.
    Bom para perguntas com termos técnicos específicos.
    """
    _carregar_se_necessario()

    scores = _indice_bm25.get_scores(_tokenizar(pergunta))
    idx    = np.argsort(scores)[::-1][:k]

    return [
        {
            "id":     _chunks[i]["id"],
            "texto":  _chunks[i]["texto"],
            "fonte":  _chunks[i]["fonte"],
            "score":  float(scores[i]),
            "metodo": "bm25",
        }
        for i in idx
        if scores[i] > 0   # descarta chunks sem nenhuma palavra em comum
    ]


def buscar_semantico(pergunta: str, k: int = 3) -> list[dict]:
    """
    Busca semântica — encontra chunks com significado similar à pergunta.
    Bom para perguntas com sinônimos ou paráfrases.
    """
    _carregar_se_necessario()

    modelo  = _get_modelo()
    q_vec   = modelo.encode([pergunta], normalize_embeddings=True).astype("float32")
    scores, idx = _indice_faiss.search(q_vec, k)

    return [
        {
            "id":     _chunks[i]["id"],
            "texto":  _chunks[i]["texto"],
            "fonte":  _chunks[i]["fonte"],
            "score":  float(scores[0][j]),
            "metodo": "semantico",
        }
        for j, i in enumerate(idx[0])
        if i >= 0   # FAISS retorna -1 quando k > total de chunks
    ]


def buscar_hibrido(pergunta: str, k: int = 3, alpha: float = 0.6) -> list[dict]:
    """
    Busca híbrida — combina BM25 e semântico com peso alpha.

    alpha = 0.0  → só BM25
    alpha = 1.0  → só semântico
    alpha = 0.6  → 60% semântico + 40% BM25 (padrão)

    Chunks que aparecem bem nos dois métodos sobem no ranking.
    """
    _carregar_se_necessario()

    modelo = _get_modelo()

    # Scores BM25 normalizados
    scores_bm25 = _normalizar(
        _indice_bm25.get_scores(_tokenizar(pergunta))
    )

    # Scores semânticos normalizados
    q_vec        = modelo.encode([pergunta], normalize_embeddings=True).astype("float32")
    scores_dense = _normalizar(np.dot(_matriz, q_vec[0]))

    # Combinação ponderada
    score_final = alpha * scores_dense + (1.0 - alpha) * scores_bm25
    idx         = np.argsort(score_final)[::-1][:k]

    return [
        {
            "id":     _chunks[i]["id"],
            "texto":  _chunks[i]["texto"],
            "fonte":  _chunks[i]["fonte"],
            "score":  float(score_final[i]),
            "metodo": "hibrido",
        }
        for i in idx
    ]


# ── Geração de resposta ───────────────────────────────────────────────────────

def _construir_prompt(pergunta: str, docs: list[dict]) -> str:
    """Monta o prompt com os chunks recuperados."""
    from src.prompts.rag import rag_resposta
    contexto = "\n\n".join(
        f"Trecho {i+1} (fonte: {d['fonte']}):\n{d['texto']}"
        for i, d in enumerate(docs)
    )
    return rag_resposta(pergunta, contexto)


def responder(
    pergunta: str,
    metodo:   str   = "hibrido",
    k:        int   = 3,
    alpha:    float = 0.6,
) -> dict:
    """
    Função principal do RAG — usada pelo agente via tool calling.

    Fluxo:
        1. Recupera os k chunks mais relevantes
        2. Monta o prompt com o contexto
        3. Envia ao Gemma e retorna a resposta

    Retorna dicionário com:
        resposta:  texto gerado pelo Gemma
        chunks:    lista de chunks usados como contexto
        metodo:    método de busca usado

    Exemplo:
        from src.rag.retriever import responder
        resultado = responder("O que é regressão logística?")
        print(resultado["resposta"])
    """
    logger.info(f"RAG query: '{pergunta}' | método={metodo} | k={k}")

    # ── Passo 1: Recuperação ──────────────────────────────────────────────────
    if metodo == "bm25":
        docs = buscar_bm25(pergunta, k=k)
    elif metodo == "semantico":
        docs = buscar_semantico(pergunta, k=k)
    else:
        docs = buscar_hibrido(pergunta, k=k, alpha=alpha)

    if not docs:
        return {
            "resposta": "Não encontrei trechos relevantes nos documentos indexados.",
            "chunks":   [],
            "metodo":   metodo,
        }

    logger.info(f"Chunks recuperados: {[d['id'] for d in docs]}")

    # ── Passo 2: Geração ──────────────────────────────────────────────────────
    prompt  = _construir_prompt(pergunta, docs)
    client  = get_llm_client()

    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )

    resposta = response.choices[0].message.content
    logger.info(f"Resposta gerada: {len(resposta)} caracteres")

    return {
        "resposta": resposta,
        "chunks":   docs,
        "metodo":   metodo,
    }
