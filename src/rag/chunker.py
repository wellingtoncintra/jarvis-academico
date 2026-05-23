"""
src/rag/chunker.py

Divide o Markdown em chunks para indexação no RAG.

Estratégia híbrida:
  1. Divide o texto pelos parágrafos naturais do Markdown (\\n\\n)
  2. Parágrafos muito curtos  (< MIN_CHARS)  → agrupados com o próximo
  3. Parágrafos normais       (< MAX_CHARS)  → viram um chunk diretamente
  4. Parágrafos muito longos  (>= MAX_CHARS) → janela deslizante como fallback

Nenhum conteúdo é descartado — parágrafos curtos são agrupados para
preservar informações pontuais como "Frequência mínima: 75%".
"""

from loguru import logger

# ── Configurações padrão ───────────────────────────────────────────────────────
MIN_CHARS  = 150    # parágrafos menores que isso são agrupados com o próximo
MAX_CHARS  = 1500   # parágrafos maiores que isso são quebrados com janela
TAMANHO    = 1000   # tamanho da janela deslizante (em caracteres)
OVERLAP    = 150    # sobreposição entre janelas


# ── Estratégias individuais ────────────────────────────────────────────────────

def _janela_deslizante(texto: str, tamanho: int = TAMANHO, overlap: int = OVERLAP) -> list[str]:
    """
    Divide um texto longo em chunks com sobreposição.
    Usado como fallback para parágrafos muito longos.
    """
    if overlap >= tamanho:
        raise ValueError(f"overlap ({overlap}) deve ser menor que tamanho ({tamanho})")

    chunks = []
    passo  = tamanho - overlap
    inicio = 0

    while inicio < len(texto):
        fim = inicio + tamanho
        chunks.append(texto[inicio:fim])
        inicio += passo

    return chunks


def _por_paragrafo(markdown: str) -> list[str]:
    """
    Divide o Markdown pelos separadores naturais (\\n\\n).
    Retorna parágrafos brutos, sem filtro de tamanho.
    """
    return [p.strip() for p in markdown.split("\n\n")]


# ── Estratégia principal ───────────────────────────────────────────────────────

def _agrupar_curtos(paragrafos: list[str], min_chars: int) -> list[str]:
    """
    Agrupa parágrafos curtos com o seguinte até atingir min_chars.

    Nenhum conteúdo é perdido — parágrafos curtos como
    "Frequência mínima: 75%" são preservados junto ao contexto vizinho.

    Exemplo:
        ["Freq: 75%", "Média: 6,0", "Alunos reprovados por falta perdem o vínculo."]
        → ["Freq: 75%\nMédia: 6,0\nAlunos reprovados por falta perdem o vínculo."]
    """
    agrupados = []
    acumulado = ""

    for p in paragrafos:
        if not p:
            continue

        if acumulado:
            acumulado = acumulado + "\n" + p
        else:
            acumulado = p

        # Quando o acumulado atingir o tamanho mínimo, fecha o grupo
        if len(acumulado) >= min_chars:
            agrupados.append(acumulado)
            acumulado = ""

    # Flush — se sobrou algo no acumulador, adiciona como último chunk
    if acumulado:
        agrupados.append(acumulado)

    return agrupados


def chunkar(
    markdown: str,
    min_chars: int = MIN_CHARS,
    max_chars: int = MAX_CHARS,
    tamanho: int   = TAMANHO,
    overlap: int   = OVERLAP,
) -> list[str]:
    """
    Aplica a estratégia híbrida de chunking sem descartar nenhum conteúdo.

    Fluxo:
        1. Divide por parágrafos (\\n\\n)
        2. Agrupa parágrafos curtos (< min_chars) com o próximo
        3. Parágrafos normais (< max_chars) → chunk direto
        4. Parágrafos longos (>= max_chars)  → janela deslizante

    Retorna lista de strings (chunks limpos, sem vazios).
    """
    if not markdown.strip():
        return []

    paragrafos = _por_paragrafo(markdown)

    # Passo 1 — agrupa os curtos, nada é descartado
    paragrafos = _agrupar_curtos(paragrafos, min_chars)

    chunks_finais = []
    diretos       = 0
    por_janela    = 0

    for p in paragrafos:
        if not p:
            continue

        if len(p) < max_chars:
            # Tamanho ideal — usa diretamente
            chunks_finais.append(p)
            diretos += 1
        else:
            # Muito longo — aplica janela deslizante
            sub_chunks = _janela_deslizante(p, tamanho=tamanho, overlap=overlap)
            chunks_finais.extend(sub_chunks)
            por_janela += len(sub_chunks)

    logger.info(
        f"Chunking concluído: {len(chunks_finais)} chunks | "
        f"{diretos} diretos, {por_janela} por janela deslizante"
    )

    return chunks_finais


def chunkar_documento(documento: dict, **kwargs) -> list[dict]:
    """
    Recebe um documento do loader e retorna lista de chunks com metadados.

    Cada chunk é um dicionário:
        id:       identificador único (ex: "apostila_ia_chunk_0003")
        texto:    conteúdo do chunk
        fonte:    nome do documento de origem
        arquivo:  caminho do PDF original

    Parâmetros:
        documento: dict com chaves "nome", "arquivo", "markdown"
        **kwargs:  parâmetros repassados para chunkar()

    Exemplo:
        from src.rag.loader import carregar_todos_pdfs
        from src.rag.chunker import chunkar_documento

        docs = carregar_todos_pdfs()
        for doc in docs:
            chunks = chunkar_documento(doc)
            print(f"{doc['nome']}: {len(chunks)} chunks")
    """
    nome     = documento["nome"]
    arquivo  = documento["arquivo"]
    markdown = documento["markdown"]

    textos = chunkar(markdown, **kwargs)

    chunks = [
        {
            "id":      f"{nome}_chunk_{i:04d}",
            "texto":   texto,
            "fonte":   nome,
            "arquivo": arquivo,
        }
        for i, texto in enumerate(textos)
    ]

    logger.info(f"Documento '{nome}': {len(chunks)} chunks gerados")
    return chunks


def chunkar_texto_direto(texto: str, fonte: str = "upload", **kwargs) -> list[dict]:
    """
    Chunka um texto avulso (ex: PDF enviado pelo usuário na interface).
    Usa a mesma estratégia híbrida.

    Parâmetros:
        texto:  texto em Markdown ou texto puro
        fonte:  nome identificador da origem
    """
    textos = chunkar(texto, **kwargs)

    return [
        {
            "id":      f"{fonte}_chunk_{i:04d}",
            "texto":   t,
            "fonte":   fonte,
            "arquivo": None,
        }
        for i, t in enumerate(textos)
    ]


def estatisticas(chunks: list[dict]) -> dict:
    """
    Retorna estatísticas dos chunks para análise de qualidade.
    Útil para ajustar os parâmetros de chunking.

    Exemplo:
        stats = estatisticas(chunks)
        print(stats)
        # {'total': 87, 'min': 102, 'max': 1498, 'media': 634, 'mediana': 601}
    """
    import statistics
    tamanhos = [len(c["texto"]) for c in chunks]

    return {
        "total":   len(chunks),
        "min":     min(tamanhos),
        "max":     max(tamanhos),
        "media":   round(statistics.mean(tamanhos)),
        "mediana": round(statistics.median(tamanhos)),
    }
