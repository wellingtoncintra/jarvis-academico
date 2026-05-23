"""
src/rag/indexer.py

Script orquestrador do pipeline RAG.
Roda uma vez para processar todos os PDFs e gerar os índices.
Deve ser reexecutado sempre que novos documentos forem adicionados.

Uso (com venv ativado, na raiz do projeto):
    python src/rag/indexer.py
    python src/rag/indexer.py --pasta data/raw
    python src/rag/indexer.py --pdf data/raw/apostila_ia.pdf
"""

import argparse
from pathlib import Path
from loguru import logger

#from .loader  import carregar_todos_pdfs, pdf_para_markdown, salvar_markdown
from loader import carregar_todos_pdfs, pdf_para_markdown, salvar_markdown
from chunker import chunkar_documento, estatisticas
from embedder import construir_indices, salvar_indices, adicionar_chunks


def indexar_pasta(pasta: str = "data/raw") -> None:
    """
    Processa todos os PDFs de uma pasta e (re)constrói os índices do zero.
    Use este modo quando quiser reindexar tudo.
    """
    logger.info(f"=== Iniciando indexação completa da pasta: {pasta} ===")

    # ── Etapa 1: Carregar e converter PDFs ───────────────────────────────────
    documentos = carregar_todos_pdfs(pasta)

    if not documentos:
        logger.error("Nenhum documento carregado. Abortando.")
        return

    # Salva os Markdowns gerados para inspeção
    for doc in documentos:
        salvar_markdown(doc["markdown"], doc["arquivo"])

    # ── Etapa 2: Chunking ─────────────────────────────────────────────────────
    todos_chunks = []
    for doc in documentos:
        chunks = chunkar_documento(doc)
        todos_chunks.extend(chunks)

    if not todos_chunks:
        logger.error("Nenhum chunk gerado. Verifique os PDFs.")
        return

    stats = estatisticas(todos_chunks)
    logger.info(
        f"Estatísticas dos chunks:\n"
        f"  Total:   {stats['total']}\n"
        f"  Mínimo:  {stats['min']} chars\n"
        f"  Máximo:  {stats['max']} chars\n"
        f"  Média:   {stats['media']} chars\n"
        f"  Mediana: {stats['mediana']} chars"
    )

    # ── Etapa 3: Embeddings e índices ─────────────────────────────────────────
    indice_faiss, indice_bm25, matriz = construir_indices(todos_chunks)

    # ── Etapa 4: Salvar ───────────────────────────────────────────────────────
    salvar_indices(todos_chunks, indice_faiss, indice_bm25, matriz)

    logger.info("=== Indexação concluída com sucesso! ===")
    logger.info(f"Total de chunks indexados: {len(todos_chunks)}")
    logger.info("Agora você pode fazer perguntas ao JARVIS sobre esses documentos.")


def indexar_pdf(caminho_pdf: str) -> None:
    """
    Processa um único PDF e adiciona aos índices existentes.
    Use este modo quando quiser adicionar um documento sem reindexar tudo.
    """
    logger.info(f"=== Adicionando PDF aos índices: {caminho_pdf} ===")

    pdf = Path(caminho_pdf)
    if not pdf.exists():
        logger.error(f"Arquivo não encontrado: {caminho_pdf}")
        return

    # Converte e salva Markdown
    markdown = pdf_para_markdown(pdf)
    salvar_markdown(markdown, pdf)

    # Chunka o documento
    documento = {
        "nome":     pdf.stem,
        "arquivo":  str(pdf),
        "markdown": markdown,
    }
    chunks = chunkar_documento(documento)

    # Adiciona aos índices existentes (ou cria do zero)
    adicionar_chunks(chunks)

    logger.info(f"=== PDF adicionado: {len(chunks)} novos chunks indexados ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexador RAG do JARVIS Acadêmico")
    grupo  = parser.add_mutually_exclusive_group()

    grupo.add_argument(
        "--pasta",
        type=str,
        default="data/raw",
        help="Pasta com PDFs para indexar (padrão: data/raw)",
    )
    grupo.add_argument(
        "--pdf",
        type=str,
        help="Caminho de um PDF específico para adicionar aos índices",
    )

    args = parser.parse_args()

    if args.pdf:
        indexar_pdf(args.pdf)
    else:
        indexar_pasta(args.pasta)
