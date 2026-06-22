"""Gera a recuperação reproduzível das perguntas de avaliação.

Uso básico:
    python src/evaluation/gerar_recuperacao.py

Com reranking:
    python src/evaluation/gerar_recuperacao.py --rerank \
        --saida data/evaluation/recuperacao_rerank.json

Para atualizar os chunks do artefato consumido pela interface:
    python src/evaluation/gerar_recuperacao.py --atualizar-avaliacao
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.rag.retriever import recuperar_documentos


EVAL_PATH = Path("data/evaluation/avaliacao_rag.json")
OUT_PATH = Path("data/evaluation/recuperacao_atual.json")


def _resumo(texto: str, limite: int = 320) -> str:
    texto = " ".join(texto.split())
    if len(texto) <= limite:
        return texto
    return texto[: limite - 3] + "..."


def _serializar_doc(doc: dict) -> dict:
    resultado = {
        "chunk_id": doc["id"],
        "fonte": doc["fonte"],
        "score": round(float(doc["score"]), 6),
        "metodo": doc["metodo"],
        "trecho": _resumo(doc["texto"]),
    }
    if "score_hibrido" in doc:
        resultado["score_hibrido"] = round(float(doc["score_hibrido"]), 6)
    return resultado


def gerar_recuperacao(avaliacao: dict, rerank: bool = False) -> dict:
    k = int(avaliacao.get("k", 3))
    resultados = []

    for item in avaliacao.get("perguntas", []):
        pergunta = item["pergunta"]
        docs = recuperar_documentos(
            pergunta=pergunta,
            metodo="hibrido",
            k=k,
            alpha=0.6,
            rerank=rerank,
        )
        resultados.append(
            {
                "id": item["id"],
                "pergunta": pergunta,
                "k_efetivo": len(docs),
                "documentos_recuperados": [_serializar_doc(doc) for doc in docs],
            }
        )

    return {
        "data_geracao": date.today().isoformat(),
        "metodo_recuperacao": "hibrido+rerank" if rerank else "hibrido",
        "alpha": 0.6,
        "k_base": k,
        "k_comparativo": 6,
        "resultados": resultados,
    }


def atualizar_avaliacao(avaliacao: dict, recuperacao: dict) -> dict:
    """Mescla somente a recuperação, preservando respostas e avaliações manuais."""
    por_id = {item["id"]: item for item in recuperacao["resultados"]}
    for pergunta in avaliacao.get("perguntas", []):
        atual = por_id[pergunta["id"]]
        pergunta["documentos_recuperados"] = atual["documentos_recuperados"]

    avaliacao["data_avaliacao"] = recuperacao["data_geracao"]
    avaliacao["metodo_recuperacao"] = recuperacao["metodo_recuperacao"]
    avaliacao["alpha"] = recuperacao["alpha"]
    avaliacao["k"] = recuperacao["k_base"]
    avaliacao["k_comparativo"] = recuperacao["k_comparativo"]
    return avaliacao


def main() -> None:
    parser = argparse.ArgumentParser(description="Avaliação reproduzível da recuperação RAG")
    parser.add_argument("--rerank", action="store_true", help="Aplica o cross-encoder aos candidatos")
    parser.add_argument("--saida", type=Path, default=OUT_PATH, help="Arquivo JSON de saída")
    parser.add_argument(
        "--atualizar-avaliacao",
        action="store_true",
        help="Atualiza os chunks em data/evaluation/avaliacao_rag.json",
    )
    args = parser.parse_args()

    avaliacao = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    recuperacao = gerar_recuperacao(avaliacao, rerank=args.rerank)

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(
        json.dumps(recuperacao, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if args.atualizar_avaliacao:
        avaliacao = atualizar_avaliacao(avaliacao, recuperacao)
        EVAL_PATH.write_text(
            json.dumps(avaliacao, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    print(f"Recuperação gerada em {args.saida}")
    if args.atualizar_avaliacao:
        print(f"Avaliação atualizada em {EVAL_PATH}")


if __name__ == "__main__":
    main()
