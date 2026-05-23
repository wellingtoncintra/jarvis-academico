"""
src/rag/loader.py

Responsável por carregar PDFs da pasta data/raw/ e converter
para Markdown estruturado usando o Docling.

O Docling analisa a estrutura visual do PDF (títulos, parágrafos,
tabelas, listas) e gera um Markdown limpo — muito superior à
extração de texto bruto do pypdf.
"""

from pathlib import Path
from loguru import logger
from docling.document_converter import DocumentConverter


# Instancia o conversor uma única vez (é pesado para inicializar)
_converter = None


def _get_converter() -> DocumentConverter:
    """Retorna o conversor Docling, inicializando na primeira chamada."""
    global _converter
    if _converter is None:
        logger.info("Inicializando Docling DocumentConverter...")
        _converter = DocumentConverter()
    return _converter


def pdf_para_markdown(caminho_pdf: str | Path) -> str:
    """
    Converte um arquivo PDF para Markdown estruturado.

    Parâmetros:
        caminho_pdf: caminho para o arquivo .pdf

    Retorna:
        string com o conteúdo em Markdown

    Exemplo:
        md = pdf_para_markdown("data/raw/apostila_ia.pdf")
        print(md[:500])
    """
    caminho = Path(caminho_pdf)

    if not caminho.exists():
        raise FileNotFoundError(f"PDF não encontrado: {caminho}")

    if caminho.suffix.lower() != ".pdf":
        raise ValueError(f"Arquivo não é um PDF: {caminho}")

    logger.info(f"Convertendo PDF: {caminho.name}")

    converter = _get_converter()
    resultado = converter.convert(str(caminho))
    markdown = resultado.document.export_to_markdown()

    logger.info(f"Conversão concluída: {len(markdown):,} caracteres")
    return markdown


def carregar_todos_pdfs(pasta: str | Path = "data/raw") -> list[dict]:
    """
    Carrega e converte todos os PDFs de uma pasta.

    Retorna uma lista de dicionários com:
        - nome:     nome do arquivo (sem extensão)
        - arquivo:  caminho completo
        - markdown: conteúdo convertido

    Exemplo:
        documentos = carregar_todos_pdfs("data/raw")
        for doc in documentos:
            print(doc["nome"], len(doc["markdown"]))
    """
    pasta = Path(pasta)

    if not pasta.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")

    pdfs = sorted(pasta.glob("*.pdf"))

    if not pdfs:
        logger.warning(f"Nenhum PDF encontrado em: {pasta}")
        return []

    logger.info(f"Encontrados {len(pdfs)} PDFs em '{pasta}'")

    documentos = []
    for pdf in pdfs:
        try:
            markdown = pdf_para_markdown(pdf)
            documentos.append({
                "nome":     pdf.stem,        # nome sem extensão
                "arquivo":  str(pdf),
                "markdown": markdown,
            })
        except Exception as e:
            logger.error(f"Erro ao converter '{pdf.name}': {e}")

    logger.info(f"Carregados {len(documentos)}/{len(pdfs)} documentos")
    return documentos


def salvar_markdown(markdown: str, caminho_pdf: str | Path) -> Path:
    """
    Salva o Markdown gerado em data/processed/ para inspeção.
    Útil para verificar a qualidade da extração antes de chunkar.

    Retorna o caminho do arquivo .md salvo.
    """
    origem = Path(caminho_pdf)
    destino = Path("data/processed") / origem.with_suffix(".md").name

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(markdown, encoding="utf-8")

    logger.info(f"Markdown salvo em: {destino}")
    return destino
