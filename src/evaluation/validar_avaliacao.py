"""Valida a consistência entre avaliação, chunks atuais e requisitos mínimos."""

import json
import pickle
from collections import Counter
from pathlib import Path


EVAL_PATH = Path("data/evaluation/avaliacao_rag.json")
CHUNKS_PATH = Path("data/processed/chunks.pkl")
CLASSIFICACOES = {"correta", "parcialmente correta", "incorreta"}
TOKENS_CORROMPIDOS = ("glyph[", "formula-not-decoded")


def _resumo(texto: str, limite: int = 320) -> str:
    texto = " ".join(texto.split())
    return texto if len(texto) <= limite else texto[: limite - 3] + "..."


def validar() -> list[str]:
    dados = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    chunks = pickle.loads(CHUNKS_PATH.read_bytes())
    chunks_por_id = {chunk["id"]: chunk for chunk in chunks}
    erros = []

    perguntas = dados.get("perguntas", [])
    if len(perguntas) < 10:
        erros.append(f"A avaliação possui apenas {len(perguntas)} perguntas.")
    if len(dados.get("analise_erros", [])) < 3:
        erros.append("A análise possui menos de três falhas.")
    if dados.get("metodo_recuperacao") != "hibrido":
        erros.append("O método oficial da avaliação não está como híbrido.")

    contagem = Counter()
    for pergunta in perguntas:
        classificacao = pergunta.get("classificacao")
        if classificacao not in CLASSIFICACOES:
            erros.append(f"{pergunta.get('id')}: classificação inválida.")
        else:
            contagem[classificacao] += 1

        docs = pergunta.get("documentos_recuperados", [])
        if not docs:
            erros.append(f"{pergunta.get('id')}: nenhum chunk recuperado.")

        for doc in docs:
            chunk_id = doc.get("chunk_id")
            chunk = chunks_por_id.get(chunk_id)
            if chunk is None:
                erros.append(f"{pergunta.get('id')}: chunk inexistente {chunk_id}.")
                continue
            if doc.get("fonte") != chunk.get("fonte"):
                erros.append(f"{pergunta.get('id')}: fonte divergente em {chunk_id}.")
            if doc.get("trecho") != _resumo(chunk["texto"]):
                erros.append(f"{pergunta.get('id')}: trecho divergente em {chunk_id}.")
            if not 0.0 <= float(doc.get("score", -1)) <= 1.0:
                erros.append(f"{pergunta.get('id')}: score fora de [0, 1] em {chunk_id}.")

    esperado = {
        "corretas": contagem["correta"],
        "parcialmente_corretas": contagem["parcialmente correta"],
        "incorretas": contagem["incorreta"],
    }
    if dados.get("resultado_resumo") != esperado:
        erros.append("O resumo das classificações não corresponde às perguntas.")

    corpus = "\n".join(chunk["texto"] for chunk in chunks)
    for token in TOKENS_CORROMPIDOS:
        if token in corpus:
            erros.append(f"O corpus ainda contém o token corrompido: {token}")

    return erros


def main() -> None:
    erros = validar()
    if erros:
        print("Avaliação inválida:")
        for erro in erros:
            print(f"- {erro}")
        raise SystemExit(1)
    print("Avaliação válida: perguntas, falhas, scores, fontes e chunks estão consistentes.")


if __name__ == "__main__":
    main()
