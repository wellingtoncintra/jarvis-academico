"""Normalização do Markdown extraído dos PDFs acadêmicos."""

import re
import unicodedata


SUBSTITUICOES = {
    "glyph[epsilon1]": "ε",
    "glyph[negationslash]": "≠",
    "glyph[turnstileleft]": "⊢",
}

ACENTOS_SEPARADOS = {
    "t˜ em": "têm",
    "´ a": "á",
    "´ e": "é",
    "´ i": "í",
    "´ ı": "í",
    "´ o": "ó",
    "´ u": "ú",
    "ˆ a": "â",
    "ˆ e": "ê",
    "ˆ i": "î",
    "ˆ ı": "î",
    "ˆ o": "ô",
    "ˆ u": "û",
    "˜ a": "ã",
    "˜ o": "õ",
    "¸ c": "ç",
    "` a": "à",
    "´ A": "Á",
    "´ E": "É",
    "´ I": "Í",
    "´ O": "Ó",
    "´ U": "Ú",
    "ˆ A": "Â",
    "ˆ E": "Ê",
    "ˆ I": "Î",
    "ˆ O": "Ô",
    "ˆ U": "Û",
    "˜ A": "Ã",
    "˜ O": "Õ",
    "¸ C": "Ç",
    "` A": "À",
}

FORMULA_NAO_DECODIFICADA = re.compile(
    r"<!--\s*formula-not-decoded\s*-->|formula-not-decoded",
    flags=re.IGNORECASE,
)


def normalizar_markdown(markdown: str) -> str:
    """Remove marcadores sem conteúdo e restaura símbolos conhecidos.

    A função não tenta reconstruir fórmulas perdidas. Ela apenas remove o
    marcador gerado pelo conversor e preserva a estrutura de linhas do
    Markdown para não alterar títulos, listas ou parágrafos.
    """
    if not markdown:
        return ""

    texto = markdown
    for token, simbolo in SUBSTITUICOES.items():
        texto = texto.replace(token, simbolo)
    for sequencia, caractere in ACENTOS_SEPARADOS.items():
        texto = texto.replace(sequencia, caractere)

    texto = FORMULA_NAO_DECODIFICADA.sub("", texto)
    texto = unicodedata.normalize("NFC", texto)

    linhas = [re.sub(r"[ \t]{2,}", " ", linha).rstrip() for linha in texto.splitlines()]
    texto = "\n".join(linhas)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()
