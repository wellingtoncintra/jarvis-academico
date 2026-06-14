"""
interface/avaliacao.py - Painel de avaliação do RAG.

Mostra o artefato obrigatório de avaliação diretamente no Streamlit:
perguntas, chunks recuperados, respostas, classificações e análise de erros.
"""

import json
from collections import Counter
from pathlib import Path

import streamlit as st


EVAL_PATH = Path("data/evaluation/avaliacao_rag.json")


def _carregar_avaliacao() -> dict:
    if not EVAL_PATH.exists():
        return {}
    return json.loads(EVAL_PATH.read_text(encoding="utf-8"))


def _label_classificacao(valor: str) -> str:
    cores = {
        "correta": "#064e3b",
        "parcialmente correta": "#713f12",
        "incorreta": "#7f1d1d",
    }
    cor = cores.get(valor, "#1f2937")
    return (
        f"<span style='background:{cor};color:#f8fafc;"
        f"border-radius:999px;padding:3px 10px;font-size:.78rem;"
        f"font-weight:700;text-transform:uppercase;'>{valor}</span>"
    )


def render():
    st.markdown("# Avaliação e Análise de Erros")
    st.caption("Artefato de entrega: 10 perguntas avaliadas, chunks recuperados e falhas identificadas.")

    dados = _carregar_avaliacao()
    if not dados:
        st.warning("Arquivo de avaliacao nao encontrado em `data/evaluation/avaliacao_rag.json`.")
        return

    perguntas = dados.get("perguntas", [])
    falhas = dados.get("analise_erros", [])
    contagem = Counter(p.get("classificacao", "sem classificacao") for p in perguntas)

    col_total, col_ok, col_parcial, col_inc = st.columns(4)
    col_total.metric("Perguntas", len(perguntas))
    col_ok.metric("Corretas", contagem.get("correta", 0))
    col_parcial.metric("Parciais", contagem.get("parcialmente correta", 0))
    col_inc.metric("Incorretas", contagem.get("incorreta", 0))

    st.markdown(
        f"**Metodo registrado:** `{dados.get('metodo_recuperacao', 'n/a')}` "
        f"com `k={dados.get('k', 'n/a')}` chunks por pergunta."
    )

    tab_perguntas, tab_falhas, tab_exportar = st.tabs(
        ["Perguntas avaliadas", "Análise de erros", "Exportar"]
    )

    with tab_perguntas:
        for item in perguntas:
            titulo = f"{item.get('id')} - {item.get('pergunta')}"
            with st.expander(titulo, expanded=item.get("id") == "Q01"):
                st.markdown(_label_classificacao(item.get("classificacao", "")), unsafe_allow_html=True)
                st.markdown("**Resposta avaliada**")
                st.write(item.get("resposta", ""))

                st.markdown("**Chunks recuperados**")
                for doc in item.get("documentos_recuperados", []):
                    st.markdown(
                        f"- `{doc.get('chunk_id')}` | fonte `{doc.get('fonte')}` | "
                        f"score `{doc.get('score')}`"
                    )
                    st.caption(doc.get("trecho", ""))

                st.markdown("**Justificativa da classificação**")
                st.write(item.get("justificativa", ""))

    with tab_falhas:
        for falha in falhas:
            with st.expander(f"{falha.get('id')} - {falha.get('tipo')}", expanded=True):
                st.markdown("**Falha**")
                st.write(falha.get("falha", ""))
                st.markdown("**Causa**")
                st.write(falha.get("causa", ""))
                st.markdown("**Possível solução**")
                st.write(falha.get("possivel_solucao", ""))

    with tab_exportar:
        st.markdown("O mesmo conteúdo também está documentado em `AVALIACAO_E_ANALISE_ERROS.md`.")
        st.download_button(
            "Baixar JSON da avaliação",
            data=json.dumps(dados, ensure_ascii=False, indent=2),
            file_name="avaliacao_rag.json",
            mime="application/json",
            use_container_width=True,
        )
