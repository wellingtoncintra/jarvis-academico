# -*- coding: utf-8 -*-
"""interface/agenda.py — Agenda acadêmica usando src/storage/agenda.py."""

import streamlit as st
import datetime

from src.storage.agenda import (
    adicionar_evento,
    listar_eventos_hoje,
    listar_eventos_semana,
    listar_todos_eventos,
    listar_eventos_por_periodo,
    listar_eventos_por_data,
    remover_evento,
)

DIAS_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
TIPOS   = ["aula", "prova", "evento"]
CORES   = {
    "aula":   "#4f8ef7",
    "prova":  "#f87171",
    "evento": "#34d399",
}


def _card_evento(ev, hoje):
    cor    = CORES.get(ev.get("tipo", "evento"), "#64748b")
    data   = ev.get("data", "—")
    hora   = ev.get("hora") or ""
    tipo   = ev.get("tipo", "evento")
    titulo = ev.get("titulo", "Sem título")
    desc   = ev.get("descricao") or ""

    try:
        d          = datetime.date.fromisoformat(data)
        label_data = f"{d.strftime('%d/%m/%Y')} ({DIAS_PT[d.weekday()]})"
        is_today   = d == hoje
    except Exception:
        label_data = data
        is_today   = False

    badge_hoje = ""
    if is_today:
        badge_hoje = ' <span style="background:#1d4ed8;color:#fff;border-radius:99px;font-size:.7rem;padding:2px 8px;">HOJE</span>'

    col_card, col_del = st.columns([0.9, 0.1])
    with col_card:
        st.markdown(
            f'<div style="border-left:4px solid {cor};background:#13161e;'
            f'border-radius:0 10px 10px 0;padding:14px 18px;margin-bottom:8px;'
            f'border:1px solid #1e2330;border-left:4px solid {cor};">'
            f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">'
            f'<span style="color:{cor};font-weight:700;font-size:1rem;">{titulo}</span>'
            f'<span style="background:{cor}22;color:{cor};border-radius:6px;padding:2px 10px;font-size:.75rem;">{tipo}</span>'
            f'{badge_hoje}</div>'
            f'<div style="color:#94a3b8;font-size:.85rem;margin-top:4px;">'
            f'🗓 {label_data}{"&nbsp;&nbsp;⏰ " + hora if hora else ""}</div>'
            + (f'<div style="color:#cbd5e1;font-size:.85rem;margin-top:4px;">{desc}</div>' if desc else "")
            + "</div>",
            unsafe_allow_html=True,
        )
    with col_del:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑", key=f"del_ev_{ev['id']}", help="Remover evento"):
            remover_evento(ev["id"])
            st.rerun()


def render():
    st.markdown("# 📅 Agenda Acadêmica")

    tab_vis, tab_add = st.tabs(["📋 Visualizar", "➕ Adicionar evento"])

    with tab_vis:
        hoje = datetime.date.today()

        filtro = st.selectbox(
            "Filtrar por",
            ["Todos", "Hoje", "Esta semana", "Próximos 7 dias"],
            key="agenda_filtro",
        )

        if filtro == "Hoje":
            eventos = listar_eventos_hoje()
        elif filtro == "Esta semana":
            start = hoje - datetime.timedelta(days=hoje.weekday())
            eventos = listar_eventos_por_periodo(start.isoformat(), (start + datetime.timedelta(days=6)).isoformat())
        elif filtro == "Próximos 7 dias":
            eventos = listar_eventos_por_periodo(hoje.isoformat(), (hoje + datetime.timedelta(days=7)).isoformat())
        else:
            eventos = listar_todos_eventos()

        if not eventos:
            st.info("Nenhum evento encontrado para o filtro selecionado.")
        else:
            for ev in eventos:
                _card_evento(ev, hoje)

        st.markdown("---")
        todos = listar_todos_eventos()
        m1, m2, m3 = st.columns(3)
        m1.metric("Total de eventos", len(todos))
        m2.metric("Hoje", len(listar_eventos_hoje()))
        provas = [e for e in listar_eventos_por_periodo(
            hoje.isoformat(), (hoje + datetime.timedelta(days=7)).isoformat()
        ) if e.get("tipo") == "prova"]
        m3.metric("Provas (7 dias)", len(provas))

    with tab_add:
        with st.form("form_agenda", clear_on_submit=True):
            c1, c2 = st.columns(2)
            titulo    = c1.text_input("Título *", placeholder="Ex: Prova de IA")
            tipo      = c2.selectbox("Tipo", TIPOS)
            data_ev   = c1.date_input("Data *", value=datetime.date.today())
            hora_ev   = c2.text_input("Hora", placeholder="14:00")
            descricao = st.text_area("Descrição", height=80)

            if st.form_submit_button("➕ Adicionar evento", use_container_width=True):
                if not titulo:
                    st.error("Título é obrigatório.")
                else:
                    adicionar_evento(
                        titulo=titulo,
                        data=str(data_ev),
                        hora=hora_ev or None,
                        tipo=tipo,
                        descricao=descricao or None,
                    )
                    st.success(f"✅ Evento '{titulo}' adicionado!")
                    st.rerun()
