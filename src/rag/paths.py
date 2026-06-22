"""
src/rag/paths.py

Caminhos dos índices RAG e checagem de existência.

Este módulo é deliberadamente LEVE: importa apenas pathlib. A separação existe
para que checar se os índices já foram gerados (indices_existem) não exija
importar o embedder, que por sua vez arrasta sentence-transformers / torch /
faiss — um custo de vários segundos.

Telas que só precisam saber se há índices (ex.: a aba de aprendizado decidindo
entre "gere materiais" e o formulário de prática) importam daqui e abrem
instantaneamente. O stack pesado de ML só é carregado quando uma operação que
realmente o usa (gerar embeddings, buscar) é executada.
"""

from pathlib import Path

# Diretório e arquivos dos índices persistidos.
INDICE_DIR  = Path("data/processed")
FAISS_PATH  = INDICE_DIR / "indice.faiss"
BM25_PATH   = INDICE_DIR / "indice_bm25.pkl"
CHUNKS_PATH = INDICE_DIR / "chunks.pkl"


def indices_existem() -> bool:
    """
    Verifica se os três índices já foram gerados em disco.
    Operação trivial de I/O — não carrega nenhuma dependência pesada.
    """
    return FAISS_PATH.exists() and BM25_PATH.exists() and CHUNKS_PATH.exists()
