"""pages/agenda.py — Agenda acadêmica visual."""

import streamlit as st
import datetime
import json
from pathlib import Path

DATA_FILE = Path("data/agenda.json")

DIAS_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
TIPOS   = ["Aula", "Prova", "Trabalho", "Seminário", "Reunião", "Outro"]
CORES   = {
    "Aula":       "#4f8ef7",
    "Prova":      "#f87171",
    "Trabalho":   "#fbbf24",
    "Seminário":  "#a78bfa",
    "Reunião":    "#34d399",
    "Outro":      "#64748b",
}


def _load() -> list:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return st.session_state.get("agenda", [])


def _save(data: list):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    st.session_state.agenda = data


def render():
    st.markdown("# Agenda Acadêmica")
    agenda = _load()

    tab_vis, tab_add = st.tabs(["📋 Visualizar", "➕ Adicionar evento"])

    # ── Visualizar ────────────────────────────────────────────────────────────
    with tab_vis:
        hoje = datetime.date.today()

        filtro = st.selectbox(
            "Filtrar por",
            ["Todos", "Hoje", "Esta semana", "Próximos 7 dias"],
            key="agenda_filtro",
        )

        def _in_range(ev):
            try:
                d = datetime.date.fromisoformat(ev["data"])
            except Exception:
                return True
            if filtro == "Hoje":
                return d == hoje
            if filtro == "Esta semana":
                start = hoje - datetime.timedelta(days=hoje.weekday())
                return start <= d <= start + datetime.timedelta(days=6)
            if filtro == "Próximos 7 dias":
                return hoje <= d <= hoje + datetime.timedelta(days=7)
            return True

        eventos = [e for e in agenda if _in_range(e)]
        eventos.sort(key=lambda x: (x.get("data", ""), x.get("hora", "")))

        if not eventos:
            st.markdown(
                '<div class="jarvis-card" style="color:#64748b;text-align:center;padding:40px;">Nenhum evento encontrado.</div>',
                unsafe_allow_html=True,
            )
        else:
            for ev in eventos:
                cor   = CORES.get(ev.get("tipo", "Outro"), "#64748b")
                data  = ev.get("data", "—")
                hora  = ev.get("hora", "")
                tipo  = ev.get("tipo", "Outro")
                titulo = ev.get("titulo", "Sem título")
                desc  = ev.get("descricao", "")

                try:
                    d = datetime.date.fromisoformat(data)
                    label_data = f"{d.strftime('%d/%m')} ({DIAS_PT[d.weekday()]})"
                except Exception:
                    label_data = data

                is_today = data == str(hoje)
                badge = ' <span style="background:#4f8ef7;color:#fff;border-radius:99px;font-size:.7rem;padding:1px 8px;">HOJE</span>' if is_today else ""

                st.markdown(f"""
                <div class="jarvis-card" style="border-left:4px solid {cor};">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span style="color:{cor};font-weight:700;font-size:1rem;">{titulo}</span>
                        <span style="background:{cor}22;color:{cor};border-radius:6px;padding:1px 8px;font-size:.75rem;">{tipo}</span>
                        {badge}
                    </div>
                    <div style="color:#94a3b8;font-size:.85rem;margin-top:4px;">
                        🗓 {label_data} {"&nbsp;⏰ " + hora if hora else ""}
                    </div>
                    {"<div style='color:#cbd5e1;font-size:.85rem;margin-top:6px;'>"+desc+"</div>" if desc else ""}
                </div>
                """, unsafe_allow_html=True)

        # Métricas rápidas
        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        provas_semana = sum(
            1 for e in agenda
            if e.get("tipo") == "Prova"
            and e.get("data", "") >= str(hoje)
            and e.get("data", "") <= str(hoje + datetime.timedelta(days=7))
        )
        m1.metric("Total de eventos", len(agenda))
        m2.metric("Hoje", sum(1 for e in agenda if e.get("data") == str(hoje)))
        m3.metric("Provas (7 dias)", provas_semana)
        m4.metric("Esta semana",
                  sum(1 for e in _load()
                      if _in_range_week(e, hoje)))

    # ── Adicionar ─────────────────────────────────────────────────────────────
    with tab_add:
        with st.form("form_agenda", clear_on_submit=True):
            c1, c2 = st.columns(2)
            titulo    = c1.text_input("Título *", placeholder="Ex: Prova de IA")
            tipo      = c2.selectbox("Tipo", TIPOS)
            data_ev   = c1.date_input("Data *", value=datetime.date.today())
            hora_ev   = c2.text_input("Hora", placeholder="14:00")
            descricao = st.text_area("Descrição", height=80)
            local     = st.text_input("Local / Sala")

            submit = st.form_submit_button("➕ Adicionar evento", use_container_width=True)
            if submit:
                if not titulo:
                    st.error("Título é obrigatório.")
                else:
                    agenda.append({
                        "titulo":    titulo,
                        "tipo":      tipo,
                        "data":      str(data_ev),
                        "hora":      hora_ev,
                        "descricao": descricao,
                        "local":     local,
                    })
                    _save(agenda)
                    st.success(f"✅ Evento '{titulo}' adicionado!")
                    st.rerun()

        st.markdown("---")
        st.markdown("**🗑 Remover evento**")
        if agenda:
            opts = {f"{e.get('data','?')} — {e.get('titulo','?')}": i for i, e in enumerate(agenda)}
            sel  = st.selectbox("Selecione para remover", list(opts.keys()), key="rm_ev")
            if st.button("Remover", key="btn_rm_ev"):
                agenda.pop(opts[sel])
                _save(agenda)
                st.rerun()
        else:
            st.caption("Nenhum evento cadastrado.")


def _in_range_week(ev, hoje):
    try:
        d     = datetime.date.fromisoformat(ev["data"])
        start = hoje - datetime.timedelta(days=hoje.weekday())
        return start <= d <= start + datetime.timedelta(days=6)
    except Exception:
        return False
