"""pages/tarefas.py — Lista de tarefas acadêmicas."""

import streamlit as st
import datetime
import json
from pathlib import Path

DATA_FILE  = Path("data/tarefas.json")
PRIORIDADES = ["Alta", "Média", "Baixa"]
CORES_PRIO  = {"Alta": "#f87171", "Média": "#fbbf24", "Baixa": "#34d399"}


def _load() -> list:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return st.session_state.get("tarefas", [])


def _save(data: list):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    st.session_state.tarefas = data


def render():
    st.markdown("# Lista de Tarefas")
    tarefas = _load()

    pendentes  = [t for t in tarefas if not t.get("concluida")]
    concluidas = [t for t in tarefas if t.get("concluida")]

    # ── Métricas ──────────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total",      len(tarefas))
    m2.metric("Pendentes",  len(pendentes))
    m3.metric("Concluídas", len(concluidas))
    alta = sum(1 for t in pendentes if t.get("prioridade") == "Alta")
    m4.metric("⚠ Alta prioridade", alta)

    tab_pend, tab_done, tab_add = st.tabs(["📋 Pendentes", "✔ Concluídas", "➕ Nova tarefa"])

    # ── Pendentes ─────────────────────────────────────────────────────────────
    with tab_pend:
        if not pendentes:
            st.markdown(
                '<div class="jarvis-card" style="color:#34d399;text-align:center;padding:32px;">🎉 Nenhuma tarefa pendente!</div>',
                unsafe_allow_html=True,
            )
        else:
            filtro_prio = st.pills(
                "Filtrar por prioridade",
                ["Todas", "Alta", "Média", "Baixa"],
                default="Todas",
                key="filtro_prio",
            )

            for i, t in enumerate(tarefas):
                if t.get("concluida"):
                    continue
                prio = t.get("prioridade", "Média")
                if filtro_prio != "Todas" and prio != filtro_prio:
                    continue

                cor      = CORES_PRIO.get(prio, "#64748b")
                prazo    = t.get("prazo", "")
                materia  = t.get("materia", "")
                vencida  = False
                if prazo:
                    try:
                        vencida = datetime.date.fromisoformat(prazo) < datetime.date.today()
                    except Exception:
                        pass

                borda = "#f87171" if vencida else cor

                cols = st.columns([0.05, 0.75, 0.2])
                with cols[0]:
                    check = st.checkbox("", key=f"ck_{i}", value=False)
                with cols[1]:
                    st.markdown(f"""
                    <div class="jarvis-card" style="border-left:4px solid {borda};padding:10px 14px;margin:0;">
                        <div style="font-weight:600;color:#e2e8f0;">{t['titulo']}</div>
                        <div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap;">
                            <span style="background:{cor}22;color:{cor};border-radius:6px;padding:1px 8px;font-size:.75rem;">{prio}</span>
                            {"<span style='background:#7f1d1d;color:#f87171;border-radius:6px;padding:1px 8px;font-size:.75rem;'>⏰ VENCIDA</span>" if vencida else ""}
                            {"<span style='color:#94a3b8;font-size:.8rem;'>📅 "+prazo+"</span>" if prazo else ""}
                            {"<span style='color:#a78bfa;font-size:.8rem;'>📖 "+materia+"</span>" if materia else ""}
                        </div>
                        {"<div style='color:#cbd5e1;font-size:.82rem;margin-top:4px;'>"+t.get('descricao','')+"</div>" if t.get('descricao') else ""}
                    </div>
                    """, unsafe_allow_html=True)
                with cols[2]:
                    if st.button("Concluir", key=f"done_{i}", use_container_width=True):
                        tarefas[i]["concluida"]     = True
                        tarefas[i]["data_conclusao"] = str(datetime.date.today())
                        _save(tarefas)
                        st.rerun()

                if check:
                    tarefas[i]["concluida"]     = True
                    tarefas[i]["data_conclusao"] = str(datetime.date.today())
                    _save(tarefas)
                    st.rerun()

    # ── Concluídas ────────────────────────────────────────────────────────────
    with tab_done:
        if not concluidas:
            st.caption("Nenhuma tarefa concluída ainda.")
        else:
            for i, t in enumerate(tarefas):
                if not t.get("concluida"):
                    continue
                cols2 = st.columns([0.85, 0.15])
                with cols2[0]:
                    st.markdown(f"""
                    <div class="jarvis-card" style="opacity:.6;border-left:4px solid #34d399;padding:10px 14px;margin:0;">
                        <div style="text-decoration:line-through;color:#94a3b8;">{t['titulo']}</div>
                        <div style="font-size:.8rem;color:#64748b;">✔ {t.get('data_conclusao','—')} {"| 📖 "+t.get('materia','') if t.get('materia') else ''}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with cols2[1]:
                    if st.button("↩ Reabrir", key=f"reopen_{i}", use_container_width=True):
                        tarefas[i]["concluida"] = False
                        tarefas[i].pop("data_conclusao", None)
                        _save(tarefas)
                        st.rerun()

            st.markdown("---")
            if st.button("🗑 Limpar concluídas", use_container_width=False):
                tarefas = [t for t in tarefas if not t.get("concluida")]
                _save(tarefas)
                st.rerun()

    # ── Nova tarefa ───────────────────────────────────────────────────────────
    with tab_add:
        with st.form("form_tarefa", clear_on_submit=True):
            c1, c2 = st.columns(2)
            titulo    = c1.text_input("Título *", placeholder="Ex: Estudar capítulo 3")
            materia   = c2.text_input("Matéria", placeholder="Ex: IA, Cálculo…")
            prioridade = c1.selectbox("Prioridade", PRIORIDADES, index=1)
            prazo      = c2.date_input("Prazo", value=None)
            descricao  = st.text_area("Descrição", height=70)

            submit = st.form_submit_button("➕ Adicionar tarefa", use_container_width=True)
            if submit:
                if not titulo:
                    st.error("Título é obrigatório.")
                else:
                    tarefas.append({
                        "titulo":     titulo,
                        "materia":    materia,
                        "prioridade": prioridade,
                        "prazo":      str(prazo) if prazo else "",
                        "descricao":  descricao,
                        "concluida":  False,
                        "criada_em":  str(datetime.date.today()),
                    })
                    _save(tarefas)
                    st.success(f"✅ Tarefa '{titulo}' adicionada!")
                    st.rerun()
