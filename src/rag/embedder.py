"""
src/rag/embedder.py

Responsável por:
  1. Gerar embeddings dos chunks com sentence-transformers
  2. Construir o índice FAISS (busca semântica)
  3. Construir o índice BM25 (busca lexical)
  4. Salvar e carregar os índices em disco (data/processed/)

Os dois índices são sempre construídos juntos e salvos juntos,
pois o retriever usa os dois combinados (busca híbrida).
"""

import re
import pickle
import numpy as np
import faiss

from pathlib import Path
from loguru import logger
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

# ── Configurações ──────────────────────────────────────────────────────────────
MODELO_EMBEDDING = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
INDICE_DIR       = Path("data/processed")
FAISS_PATH       = INDICE_DIR / "indice.faiss"
BM25_PATH        = INDICE_DIR / "indice_bm25.pkl"
CHUNKS_PATH      = INDICE_DIR / "chunks.pkl"

# Modelo carregado uma única vez em memória
_modelo: SentenceTransformer | None = None


def _get_modelo() -> SentenceTransformer:
    """Carrega o modelo de embeddings na primeira chamada (lazy loading)."""
    global _modelo
    if _modelo is None:
        logger.info(f"Carregando modelo de embeddings: {MODELO_EMBEDDING}")
        _modelo = SentenceTransformer(MODELO_EMBEDDING)
        logger.info("Modelo carregado.")
    return _modelo


# ── Tokenização para BM25 ──────────────────────────────────────────────────────

def _tokenizar(texto: str) -> list[str]:
    """Tokeniza um texto em lista de palavras para o BM25."""
    return re.findall(r"\w+", texto.lower())


# ── Construção dos índices ─────────────────────────────────────────────────────

def construir_indices(chunks: list[dict]) -> tuple:
    """
    Recebe os chunks e constrói os dois índices.

    Retorna:
        (indice_faiss, indice_bm25, matriz_embeddings)

    Parâmetros:
        chunks: lista de dicts com chaves "id", "texto", "fonte", "arquivo"
    """
    if not chunks:
        raise ValueError("Lista de chunks vazia — nada para indexar.")

    textos = [c["texto"] for c in chunks]
    modelo = _get_modelo()

    # ── Índice semântico (FAISS) ──────────────────────────────────────────────
    logger.info(f"Gerando embeddings para {len(chunks)} chunks...")
    matriz = modelo.encode(
        textos,
        normalize_embeddings=True,   # norma = 1 → produto interno = cosine similarity
        show_progress_bar=True,
        batch_size=32,
    ).astype("float32")

    dim = matriz.shape[1]
    indice_faiss = faiss.IndexFlatIP(dim)   # produto interno (= cosine para vetores normalizados)
    indice_faiss.add(matriz)
    logger.info(f"Índice FAISS criado: {dim} dimensões, {indice_faiss.ntotal} vetores.")

    # ── Índice lexical (BM25) ─────────────────────────────────────────────────
    corpus_tokenizado = [_tokenizar(t) for t in textos]
    indice_bm25 = BM25Okapi(corpus_tokenizado)
    logger.info(f"Índice BM25 criado com {len(chunks)} documentos.")

    return indice_faiss, indice_bm25, matriz


# ── Persistência em disco ──────────────────────────────────────────────────────

def salvar_indices(
    chunks: list[dict],
    indice_faiss,
    indice_bm25,
    matriz: np.ndarray,
) -> None:
    """
    Salva os índices e os chunks em disco para uso posterior.

    Arquivos gerados em data/processed/:
        indice.faiss      — índice vetorial
        indice_bm25.pkl   — índice BM25 serializado
        chunks.pkl        — lista de chunks com metadados
    """
    INDICE_DIR.mkdir(parents=True, exist_ok=True)

    # Salva FAISS
    faiss.write_index(indice_faiss, str(FAISS_PATH))
    logger.info(f"Índice FAISS salvo em: {FAISS_PATH}")

    # Salva BM25 + matriz de embeddings juntos (precisamos da matriz para o híbrido)
    with open(BM25_PATH, "wb") as f:
        pickle.dump({"bm25": indice_bm25, "matriz": matriz}, f)
    logger.info(f"Índice BM25 salvo em: {BM25_PATH}")

    # Salva os chunks (texto + metadados)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    logger.info(f"Chunks salvos em: {CHUNKS_PATH} ({len(chunks)} chunks)")


def carregar_indices() -> tuple:
    """
    Carrega os índices e chunks do disco.

    Retorna:
        (chunks, indice_faiss, indice_bm25, matriz_embeddings)

    Lança FileNotFoundError se os índices não existirem.
    Execute o indexer.py primeiro para gerá-los.
    """
    if not FAISS_PATH.exists() or not BM25_PATH.exists() or not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            "Índices não encontrados. "
            "Execute 'python src/rag/indexer.py' para indexar os documentos."
        )

    logger.info("Carregando índices do disco...")

    indice_faiss = faiss.read_index(str(FAISS_PATH))

    with open(BM25_PATH, "rb") as f:
        dados_bm25 = pickle.load(f)
    indice_bm25 = dados_bm25["bm25"]
    matriz      = dados_bm25["matriz"]

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    logger.info(f"Índices carregados: {len(chunks)} chunks, {indice_faiss.ntotal} vetores.")
    return chunks, indice_faiss, indice_bm25, matriz


def indices_existem() -> bool:
    """Verifica se os índices já foram gerados."""
    return FAISS_PATH.exists() and BM25_PATH.exists() and CHUNKS_PATH.exists()


# ── Indexação incremental ──────────────────────────────────────────────────────

def adicionar_chunks(novos_chunks: list[dict]) -> None:
    """
    Adiciona novos chunks aos índices existentes.
    Útil quando o usuário faz upload de um PDF novo pela interface.

    Se não existirem índices ainda, cria do zero.
    """
    if indices_existem():
        chunks_existentes, indice_faiss, indice_bm25, matriz = carregar_indices()
        todos_chunks = chunks_existentes + novos_chunks
    else:
        todos_chunks = novos_chunks

    # Reconstrói os índices completos
    # (FAISS IndexFlatIP não suporta remoção, então sempre reconstruímos)
    indice_faiss, indice_bm25, matriz = construir_indices(todos_chunks)
    salvar_indices(todos_chunks, indice_faiss, indice_bm25, matriz)

    logger.info(f"Índices atualizados: {len(todos_chunks)} chunks no total.")
