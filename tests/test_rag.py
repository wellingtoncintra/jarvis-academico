"""
Testes do pipeline de chunking (src/rag/chunker.py).

Cobre apenas o chunker, que é Python puro e não depende de FAISS, torch ou do
modelo de embeddings — mantendo a suíte rápida e sem dependências pesadas.
"""

from src.rag.chunker import chunkar_texto_direto, estatisticas


def test_chunks_tem_chaves_esperadas():
    texto = "Parágrafo um com conteúdo suficiente. " * 10
    chunks = chunkar_texto_direto(texto, fonte="doc_teste")
    assert len(chunks) >= 1
    for c in chunks:
        assert set(c.keys()) >= {"id", "texto", "fonte"}
        assert c["fonte"] == "doc_teste"


def test_id_segue_padrao():
    texto = "Conteúdo de teste com tamanho razoável para um chunk. " * 8
    chunks = chunkar_texto_direto(texto, fonte="afd")
    # padrão: {fonte}_chunk_NNNN
    assert chunks[0]["id"].startswith("afd_chunk_")
    assert chunks[0]["id"].split("_")[-1].isdigit()


def test_texto_longo_gera_multiplos_chunks():
    # Texto bem acima do máximo por parágrafo (1500 chars) deve ser dividido.
    paragrafo_gigante = "Esta é uma frase longa e informativa sobre autômatos. " * 80
    chunks = chunkar_texto_direto(paragrafo_gigante, fonte="longo")
    assert len(chunks) > 1, "Texto muito longo deveria gerar mais de um chunk"


def test_texto_curto_gera_um_chunk():
    chunks = chunkar_texto_direto("Texto curto e direto sobre o tema em questão.", fonte="curto")
    assert len(chunks) == 1


def test_estatisticas_coerentes():
    texto = "Frase de teste com conteúdo. " * 30
    chunks = chunkar_texto_direto(texto, fonte="stats")
    stats = estatisticas(chunks)
    assert set(stats.keys()) == {"total", "min", "max", "media", "mediana"}
    assert stats["total"] == len(chunks)
    assert stats["min"] <= stats["max"]
    assert stats["min"] <= stats["media"] <= stats["max"]


def test_lista_vazia_de_texto_vazio():
    chunks = chunkar_texto_direto("", fonte="vazio")
    # Texto vazio não deve quebrar; retorna lista (possivelmente vazia)
    assert isinstance(chunks, list)
