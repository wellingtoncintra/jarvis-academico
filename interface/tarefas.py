# -*- coding: utf-8 -*-
"""interface/tarefas.py — Tarefas usando src/storage/tarefas.py."""

import streamlit as st
import datetime

from src.storage.tarefas import (
    adicionar_tarefa,
    listar_tarefas_pendentes,
    listar_tarefas_concluidas,
    listar_todas_tarefas,
    concluir_tarefa,
    reabrir_tarefa,
    remover_tarefa,
)

PRIORIDADES = ["alta", "media", "baixa"]
CORES_PRIO  = {"alta": "#f87171", "media": "#fbbf24", "baixa": "#34d399"}
LABEL_PRIO  = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}


def _card_tarefa(t):
    prio    = t.get("prioridade", "media")
    cor     = CORES_PRIO.get(prio, "#64748b")
    prazo   = t.get("prazo") or ""
    desc    = t.get("descricao", "")
    vencida = False

    if prazo:
        try:
            vencida = datetime.date.fromisoformat(prazo) < datetime.date.today()
        except Exception:
            pass

    borda = "#f87171" if vencida else cor

    badge_vencida = ""
    if vencida:
        badge_vencida = '<span style="background:#7f1d1d;color:#f87171;border-radius:6px;padding:1px 8px;font-size:.75rem;">⏰ VENCIDA</span>'
    badge_prazo = f'<span style="color:#94a3b8;font-size:.8rem;">📅 {prazo}</span>' if prazo else ""

    col_card, col_done, col_del = st.columns([0.75, 0.13, 0.12])

    with col_card:
        st.markdown(
            f'<div style="border-left:4px solid {borda};background:#13161e;'
            f'border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:6px;'
            f'border:1px solid #1e2330;border-left:4px solid {borda};">'
            f'<span style="font-weight:600;color:#e2e8f0;">{desc}</span>'
            f'<div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap;">'
            f'<span style="background:{cor}22;color:{cor};border-radius:6px;padding:1px 8px;font-size:.75rem;">{LABEL_PRIO.get(prio, prio)}</span>'
            f'{badge_vencida}{badge_prazo}'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    with col_done:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✔", key=f"done_{t['id']}", help="Concluir", use_container_width=True):
            concluir_tarefa(t["id"])
            st.rerun()

    with col_del:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑", key=f"del_{t['id']}", help="Remover", use_container_width=True):
            remover_tarefa(t["id"])
            st.rerun()


def render():
    st.markdown("# ✅ Lista de Tarefas")

    pendentes  = listar_tarefas_pendentes()
    concluidas = listar_tarefas_concluidas()
    todas      = listar_todas_tarefas()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total",      len(todas))
    m2.metric("Pendentes",  len(pendentes))
    m3.metric("Concluídas", len(concluidas))
    m4.metric("⚠ Alta",     sum(1 for t in pendentes if t.get("prioridade") == "alta"))

    tab_pend, tab_done, tab_add = st.tabs(["📋 Pendentes", "✔ Concluídas", "➕ Nova tarefa"])

    with tab_pend:
        if not pendentes:
            st.success("🎉 Nenhuma tarefa pendente!")
        else:
            filtro = st.selectbox("Filtrar por prioridade", ["Todas", "Alta", "Média", "Baixa"], key="filtro_prio")
            mapa   = {"Alta": "alta", "Média": "media", "Baixa": "baixa"}
            for t in pendentes:
                if filtro != "Todas" and t.get("prioridade") != mapa.get(filtro):
                    continue
                _card_tarefa(t)

    with tab_done:
        if not concluidas:
            st.caption("Nenhuma tarefa concluída ainda.")
        else:
            for t in concluidas:
                col_card, col_reopen = st.columns([0.85, 0.15])
                with col_card:
                    concluido_em = t.get("concluido_em", "—")
                    st.markdown(
                        f'<div style="opacity:.6;border-left:4px solid #34d399;background:#13161e;'
                        f'border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:6px;'
                        f'border:1px solid #1e2330;border-left:4px solid #34d399;">'
                        f'<div style="text-decoration:line-through;color:#94a3b8;">{t["descricao"]}</div>'
                        f'<div style="font-size:.8rem;color:#64748b;">✔ {concluido_em}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                with col_reopen:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("↩", key=f"reopen_{t['id']}", help="Reabrir", use_container_width=True):
                        reabrir_tarefa(t["id"])
                        st.rerun()

    with tab_add:
        with st.form("form_tarefa", clear_on_submit=True):
            descricao  = st.text_input("Tarefa *", placeholder="Ex: Estudar capítulo 3 de IA")
            c1, c2     = st.columns(2)
            prioridade = c1.selectbox("Prioridade", PRIORIDADES, index=1,
                                      format_func=lambda x: LABEL_PRIO.get(x, x))
            prazo      = c2.date_input("Prazo", value=None)

            if st.form_submit_button("➕ Adicionar tarefa", use_container_width=True):
                if not descricao:
                    st.error("Descrição é obrigatória.")
                else:
                    adicionar_tarefa(
                        descricao=descricao,
                        prazo=str(prazo) if prazo else None,
                        prioridade=prioridade,
                    )
                    st.success(f"✅ Tarefa adicionada!")
                    st.rerun()
