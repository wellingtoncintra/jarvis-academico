"""pages/logs.py — Logs de tool calling + avaliação do sistema."""

import streamlit as st
import json
import datetime


def render():
    st.markdown("# Logs & Avaliação")

    tab_logs, tab_eval, tab_erros = st.tabs([
        "📋 Tool Call Logs", "📊 Avaliação (10 perguntas)", "🐛 Análise de Erros"
    ])

    # ── Tool Call Logs ────────────────────────────────────────────────────────
    with tab_logs:
        st.markdown("### Registro de chamadas de ferramentas")

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑 Limpar logs", use_container_width=True):
                st.session_state.tool_logs = []
                st.rerun()

        logs = st.session_state.get("tool_logs", [])

        if not logs:
            st.markdown(
                '<div class="jarvis-card" style="color:#64748b;text-align:center;padding:40px;">Nenhuma ferramenta acionada ainda. Inicie uma conversa no Chat.</div>',
                unsafe_allow_html=True,
            )
        else:
            # Métricas
            m1, m2, m3 = st.columns(3)
            m1.metric("Total de chamadas", len(logs))
            m2.metric("Sucesso", sum(1 for l in logs if l.get("status") == "ok"))
            m3.metric("Erro",    sum(1 for l in logs if l.get("status") != "ok"))

            st.markdown("---")

            for log in reversed(logs):
                status_class = "pill-ok" if log.get("status") == "ok" else "pill-err"
                status_text  = "✓ sucesso" if log.get("status") == "ok" else "✗ erro"

                with st.expander(f"⚙ `{log['tool']}` — {log.get('ts','')}", expanded=False):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Entrada (args)**")
                        st.code(json.dumps(log.get("args", {}), ensure_ascii=False, indent=2), language="json")
                    with c2:
                        st.markdown("**Saída (result)**")
                        result = log.get("result", "")
                        if isinstance(result, (dict, list)):
                            st.code(json.dumps(result, ensure_ascii=False, indent=2), language="json")
                        else:
                            st.code(str(result))
                    st.markdown(f'<span class="{status_class}">{status_text}</span>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("**Exportar logs**")
            logs_json = json.dumps(logs, ensure_ascii=False, indent=2)
            st.download_button(
                "⬇ Baixar logs (JSON)",
                data=logs_json,
                file_name=f"jarvis_logs_{datetime.date.today()}.json",
                mime="application/json",
            )

    # ── Avaliação ─────────────────────────────────────────────────────────────
    with tab_eval:
        st.markdown("### Avaliação do sistema — 10 perguntas")
        st.caption("Registre as perguntas feitas, documentos recuperados, respostas e classificação.")

        if "avaliacoes" not in st.session_state:
            st.session_state.avaliacoes = []

        with st.form("form_avaliacao", clear_on_submit=True):
            pergunta   = st.text_area("Pergunta",          height=60)
            docs_rec   = st.text_area("Documentos recuperados (separe por vírgula)", height=50)
            resposta   = st.text_area("Resposta da LLM",   height=80)
            classif    = st.selectbox("Classificação", ["Correta", "Parcialmente correta", "Incorreta"])
            obs        = st.text_input("Observação / nota")

            if st.form_submit_button("➕ Registrar avaliação", use_container_width=True):
                if pergunta:
                    st.session_state.avaliacoes.append({
                        "n":         len(st.session_state.avaliacoes) + 1,
                        "pergunta":  pergunta,
                        "docs":      docs_rec,
                        "resposta":  resposta,
                        "classif":   classif,
                        "obs":       obs,
                        "ts":        str(datetime.datetime.now()),
                    })
                    st.rerun()

        avs = st.session_state.avaliacoes
        if avs:
            corretas   = sum(1 for a in avs if a["classif"] == "Correta")
            parciais   = sum(1 for a in avs if a["classif"] == "Parcialmente correta")
            incorretas = sum(1 for a in avs if a["classif"] == "Incorreta")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Registradas",    len(avs))
            m2.metric("✅ Corretas",    corretas)
            m3.metric("⚠ Parciais",    parciais)
            m4.metric("❌ Incorretas",  incorretas)

            if len(avs) > 0:
                pct = corretas / len(avs) * 100
                st.progress(pct / 100, text=f"Precisão: {pct:.0f}%")

            st.markdown("---")
            for av in avs:
                cor_c = {"Correta": "#34d399", "Parcialmente correta": "#fbbf24", "Incorreta": "#f87171"}
                cor   = cor_c.get(av["classif"], "#64748b")
                with st.expander(f"#{av['n']} — {av['pergunta'][:60]}…", expanded=False):
                    st.markdown(f"**Pergunta:** {av['pergunta']}")
                    st.markdown(f"**Docs recuperados:** {av['docs'] or '—'}")
                    st.markdown(f"**Resposta:** {av['resposta'] or '—'}")
                    st.markdown(f'<span style="background:{cor}22;color:{cor};border-radius:6px;padding:2px 10px;font-size:.85rem;">{av["classif"]}</span>', unsafe_allow_html=True)
                    if av["obs"]:
                        st.caption(f"Obs: {av['obs']}")

            st.download_button(
                "⬇ Exportar avaliações (JSON)",
                data=json.dumps(avs, ensure_ascii=False, indent=2),
                file_name=f"jarvis_avaliacao_{datetime.date.today()}.json",
                mime="application/json",
            )
        else:
            st.info("Nenhuma avaliação registrada. Use o formulário acima.")

    # ── Análise de erros ──────────────────────────────────────────────────────
    with tab_erros:
        st.markdown("### Análise de falhas do sistema")
        st.caption("Identifique e documente pelo menos 3 falhas observadas.")

        TIPOS_ERRO = ["Recuperação (RAG)", "Geração (LLM)", "Ambiguidade", "Tool Calling", "Outro"]

        if "erros_doc" not in st.session_state:
            st.session_state.erros_doc = []

        with st.form("form_erro", clear_on_submit=True):
            c1, c2 = st.columns(2)
            tipo_e  = c1.selectbox("Tipo de falha", TIPOS_ERRO)
            causa   = c2.text_input("Causa identificada")
            descr   = st.text_area("Descrição da falha",     height=60)
            solucao = st.text_area("Possível solução",        height=60)
            exemplo = st.text_area("Exemplo / evidência",     height=50)

            if st.form_submit_button("➕ Registrar falha", use_container_width=True):
                if descr:
                    st.session_state.erros_doc.append({
                        "n":       len(st.session_state.erros_doc) + 1,
                        "tipo":    tipo_e,
                        "causa":   causa,
                        "descr":   descr,
                        "solucao": solucao,
                        "exemplo": exemplo,
                    })
                    st.rerun()

        erros = st.session_state.erros_doc
        CORES_ERRO = {
            "Recuperação (RAG)":  "#4f8ef7",
            "Geração (LLM)":      "#f87171",
            "Ambiguidade":        "#fbbf24",
            "Tool Calling":       "#a78bfa",
            "Outro":              "#64748b",
        }

        if erros:
            for e in erros:
                cor = CORES_ERRO.get(e["tipo"], "#64748b")
                st.markdown(f"""
                <div class="jarvis-card" style="border-left:4px solid {cor};">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                        <span style="color:#e2e8f0;font-weight:600;">Falha #{e['n']}</span>
                        <span style="background:{cor}22;color:{cor};border-radius:6px;padding:1px 8px;font-size:.75rem;">{e['tipo']}</span>
                    </div>
                    <div style="font-size:.88rem;color:#cbd5e1;"><b>Causa:</b> {e['causa'] or '—'}</div>
                    <div style="font-size:.88rem;color:#cbd5e1;margin-top:2px;"><b>Descrição:</b> {e['descr']}</div>
                    <div style="font-size:.88rem;color:#34d399;margin-top:2px;"><b>Solução:</b> {e['solucao'] or '—'}</div>
                    {"<div style='font-size:.82rem;color:#64748b;margin-top:2px;font-style:italic;'>"+e['exemplo']+"</div>" if e.get('exemplo') else ""}
                </div>
                """, unsafe_allow_html=True)

            remaining = max(0, 3 - len(erros))
            if remaining > 0:
                st.warning(f"⚠️ Mínimo exigido: 3 falhas. Faltam **{remaining}** para atingir o requisito.")
            else:
                st.success(f"✅ Requisito mínimo atingido: {len(erros)} falha(s) documentada(s).")
        else:
            st.info("Nenhuma falha registrada. O mínimo exigido pelo trabalho é 3.")
