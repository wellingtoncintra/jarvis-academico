"""Gera o relatório Markdown a partir do JSON consumido pela interface."""

import json
from pathlib import Path


EVAL_PATH = Path("data/evaluation/avaliacao_rag.json")
OUT_PATH = Path("AVALIACAO_E_ANALISE_ERROS.md")


def gerar_relatorio(dados: dict) -> str:
    resumo = dados["resultado_resumo"]
    linhas = [
        "# Avaliação do Sistema e Análise de Erros - JARVIS Acadêmico",
        "",
        "## Contexto da avaliação",
        "",
        dados["observacao"],
        "",
        f"- Data: {dados['data_avaliacao']}",
        f"- Método: `{dados['metodo_recuperacao']}`",
        f"- Alpha: `{dados.get('alpha', 0.6)}`",
        f"- K base: `{dados['k']}`",
        f"- K comparativo: `{dados.get('k_comparativo', dados['k'])}`",
        "- Arquivo estruturado: `data/evaluation/avaliacao_rag.json`",
        "- Regeneração: `python src/evaluation/gerar_recuperacao.py --atualizar-avaliacao`",
        "- Validação: `python src/evaluation/validar_avaliacao.py`",
        "",
        "## Resultado geral",
        "",
        "| Classificação | Quantidade |",
        "|---|---:|",
        f"| Correta | {resumo['corretas']} |",
        f"| Parcialmente correta | {resumo['parcialmente_corretas']} |",
        f"| Incorreta | {resumo['incorretas']} |",
        "",
        "## Perguntas avaliadas",
    ]

    for item in dados["perguntas"]:
        linhas.extend(
            [
                "",
                f"### {item['id']} - {item['pergunta']}",
                "",
                "**Chunks recuperados:**",
                "",
                "| Chunk | Fonte | Score | Método |",
                "|---|---|---:|---|",
            ]
        )
        for doc in item["documentos_recuperados"]:
            linhas.append(
                f"| `{doc['chunk_id']}` | `{doc['fonte']}` | "
                f"{doc['score']:.6f} | `{doc.get('metodo', dados['metodo_recuperacao'])}` |"
            )
        linhas.extend(
            [
                "",
                f"**Resposta:** {item['resposta']}",
                "",
                f"**Classificação:** {item['classificacao']}.",
                "",
                f"**Justificativa:** {item['justificativa']}",
            ]
        )

    linhas.extend(["", "## Análise de erros"])
    for erro in dados["analise_erros"]:
        linhas.extend(
            [
                "",
                f"### {erro['id']} - {erro['tipo'].capitalize()}",
                "",
                f"**Falha:** {erro['falha']}",
                "",
                f"**Causa:** {erro['causa']}",
                "",
                f"**Possível solução:** {erro['possivel_solucao']}",
            ]
        )

    linhas.extend(
        [
            "",
            "## Melhorias verificadas",
            "",
            *[f"- {item}" for item in dados.get("melhorias_verificadas", [])],
            "",
            "A comparação experimental do cross-encoder está em "
            "`data/evaluation/COMPARACAO_RERANKING.md`.",
            "",
        ]
    )
    return "\n".join(linhas)


def main() -> None:
    dados = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    OUT_PATH.write_text(gerar_relatorio(dados), encoding="utf-8")
    print(f"Relatório gerado em {OUT_PATH}")


if __name__ == "__main__":
    main()
