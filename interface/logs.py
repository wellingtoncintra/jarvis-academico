# -*- coding: utf-8 -*-
"""interface/logs.py — Logs de tool calling."""

import streamlit as st
import json
import datetime


def render():
    st.markdown("# 🔧 Tool Call Logs")
    st.caption("Registro de todas as ferramentas acionadas pelo agente nesta sessão.")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑 Limpar logs", use_container_width=True):
            st.session_state.tool_logs = []
            st.rerun()

    logs = st.session_state.get("tool_logs", [])

    if not logs:
        st.markdown(
            '<div style="background:#13161e;border:1px solid #1e2330;border-radius:12px;'
            'padding:40px;text-align:center;color:#64748b;margin-top:16px;">'
            '⚙ Nenhuma ferramenta acionada ainda. Inicie uma conversa no Chat.</div>',
            unsafe_allow_html=True,
        )
        return

    # Métricas
    m1, m2, m3 = st.columns(3)
    m1.metric("Total de chamadas", len(logs))
    m2.metric("✅ Sucesso", sum(1 for l in logs if l.get("status") == "ok"))
    m3.metric("❌ Erro",    sum(1 for l in logs if l.get("status") != "ok"))

    st.markdown("---")

    # Lista de logs
    for log in reversed(logs):
        ok      = log.get("status") == "ok"
        cor     = "#34d399" if ok else "#f87171"
        simbolo = "✓" if ok else "✗"
        ts      = log.get("ts", "")

        with st.expander(f"⚙ `{log['tool']}` — {ts}", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Entrada (args)**")
                st.code(
                    json.dumps(log.get("args", {}), ensure_ascii=False, indent=2),
                    language="json",
                )
            with c2:
                st.markdown("**Saída (resultado)**")
                resultado = log.get("resultado", log.get("result", ""))
                if isinstance(resultado, (dict, list)):
                    st.code(json.dumps(resultado, ensure_ascii=False, indent=2), language="json")
                else:
                    st.code(str(resultado))

            st.markdown(
                f'<span style="background:{cor}22;color:{cor};border-radius:99px;'
                f'padding:2px 12px;font-size:.82rem;font-weight:600;">{simbolo} {log["status"]}</span>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.download_button(
        "⬇ Exportar logs (JSON)",
        data=json.dumps(logs, ensure_ascii=False, indent=2),
        file_name=f"jarvis_logs_{datetime.date.today()}.json",
        mime="application/json",
    )
