"""
Gera a recuperação das perguntas de avaliação usando o índice BM25 atual.

Uso:
    python src/evaluation/gerar_recuperacao.py

Saida:
    data/evaluation/recuperacao_atual.json
"""

import json
import pickle
import re
from pathlib import Path

import numpy as np


EVAL_PATH = Path("data/evaluation/avaliacao_rag.json")
BM25_PATH = Path("data/processed/indice_bm25.pkl")
CHUNKS_PATH = Path("data/processed/chunks.pkl")
OUT_PATH = Path("data/evaluation/recuperacao_atual.json")


def _tokenizar(texto: str) -> list[str]:
    return re.findall(r"\w+", texto.lower())


def _resumo(texto: str, limite: int = 280) -> str:
    texto = " ".join(texto.split())
    if len(texto) <= limite:
        return texto
    return texto[: limite - 3] + "..."


def main() -> None:
    avaliacao = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    chunks = pickle.loads(CHUNKS_PATH.read_bytes())
    dados_bm25 = pickle.loads(BM25_PATH.read_bytes())
    bm25 = dados_bm25["bm25"]
    k = int(avaliacao.get("k", 3))

    resultados = []
    for item in avaliacao.get("perguntas", []):
        pergunta = item["pergunta"]
        scores = bm25.get_scores(_tokenizar(pergunta))
        indices = np.argsort(scores)[::-1][:k]

        docs = []
        for idx in indices:
            chunk = chunks[int(idx)]
            docs.append(
                {
                    "chunk_id": chunk["id"],
                    "fonte": chunk["fonte"],
                    "score": round(float(scores[int(idx)]), 3),
                    "trecho": _resumo(chunk["texto"]),
                }
            )

        resultados.append(
            {
                "id": item["id"],
                "pergunta": pergunta,
                "documentos_recuperados": docs,
            }
        )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(
            {
                "metodo": "bm25",
                "k": k,
                "resultados": resultados,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Recuperação gerada em {OUT_PATH}")


if __name__ == "__main__":
    main()
