"""interface/planejamento.py — Planejamento de estudos (item 3.4).

Página de planejamento: exibe o contexto acadêmico (eventos, tarefas, provas
próximas) e dispara a geração do plano no chat, onde a tool `planejar_estudos`
combina agenda + tarefas + materiais (RAG).

As melhorias de aprendizado (Active Recall e Exercícios) ficam na página
separada `interface/aprendizado.py`.
"""

import streamlit as st
import datetime
import json
from pathlib import Path


def _load_tarefas():
    p = Path("data/tarefas.json")
    if p.exists():
        return json.loads(p.read_text())
    return st.session_state.get("tarefas", [])


def _load_agenda():
    p = Path("data/agenda.json")
    if p.exists():
        return json.loads(p.read_text())
    return st.session_state.get("agenda", [])


def render():
    st.markdown("# 📊 Planejamento de Estudos")
    st.caption("Combine agenda, tarefas e materiais para gerar um plano de estudos.")

    st.markdown("### Contexto atual")
    tarefas = _load_tarefas()
    agenda  = _load_agenda()
    hoje    = datetime.date.today()

    c1, c2, c3 = st.columns(3)
    pendentes_hoje  = [t for t in tarefas if not t.get("concluida") and t.get("prazo") == str(hoje)]
    provas_proximas = [
        e for e in agenda
        if e.get("tipo") == "Prova"
        and hoje <= datetime.date.fromisoformat(e["data"]) <= hoje + datetime.timedelta(days=7)
        if e.get("data")
    ]
    eventos_hoje = [e for e in agenda if e.get("data") == str(hoje)]

    c1.metric("📅 Eventos hoje",     len(eventos_hoje))
    c2.metric("✅ Tarefas vencendo", len(pendentes_hoje))
    c3.metric("⚠ Provas em 7 dias", len(provas_proximas))

    st.markdown("---")
    st.markdown("### Gerar plano com JARVIS")

    col_left, col_right = st.columns([1, 1])
    with col_left:
        foco      = st.text_input("Foco principal", placeholder="Ex: Prova de IA na sexta")
        horas_dia = st.slider("Horas disponíveis hoje", 1, 12, 4)
        incluir   = st.multiselect(
            "Incluir no plano",
            ["Tarefas pendentes", "Eventos da agenda", "Materiais RAG", "Revisão espaçada"],
            default=["Tarefas pendentes", "Eventos da agenda"],
        )
    with col_right:
        estilo = st.radio(
            "Estilo do plano",
            ["Blocos de tempo (Pomodoro)", "Por prioridade", "Por matéria"],
            horizontal=False,
        )
        data_plano = st.date_input("Data do plano", value=hoje)

    if st.button("🪄 Gerar plano de estudos", use_container_width=True, type="primary"):
        from src.prompts.planejamento import gerar_plano_mensagem
        prompt = gerar_plano_mensagem(
            data_str=data_plano.strftime('%d/%m/%Y'),
            foco=foco,
            horas=horas_dia,
            estilo=estilo,
            incluir=incluir,
            tarefas_pendentes=[t['titulo'] for t in tarefas if not t.get('concluida')],
            provas_proximas=[e['titulo'] for e in provas_proximas],
        )
        st.session_state.pending_message = prompt
        st.session_state.active_page = "chat"
        st.rerun()

    # Visualização rápida do contexto
    if provas_proximas:
        st.markdown("---")
        st.markdown("**⚠ Provas próximas:**")
        for ev in provas_proximas:
            d = datetime.date.fromisoformat(ev["data"])
            dias_restantes = (d - hoje).days
            st.markdown(f"""
            <div class="jarvis-card" style="border-left:4px solid #f87171;padding:10px 14px;">
                <span style="font-weight:600;">{ev['titulo']}</span>
                <span style="color:#f87171;margin-left:12px;font-size:.85rem;">
                    {d.strftime('%d/%m')} · {dias_restantes} dia(s) restante(s)
                </span>
            </div>
            """, unsafe_allow_html=True)
