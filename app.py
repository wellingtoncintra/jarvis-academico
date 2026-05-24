import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

st.set_page_config(
    page_title="JARVIS Acadêmico",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600;700&display=swap');

:root {
    --bg:      #0d0f14;
    --surface: #13161e;
    --border:  #1e2330;
    --accent:  #4f8ef7;
    --accent2: #a78bfa;
    --success: #34d399;
    --warning: #fbbf24;
    --danger:  #f87171;
    --text:    #e2e8f0;
    --muted:   #64748b;
}

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
    transition: width 0.3s ease;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

.stButton > button {
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 8px;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    transition: opacity .2s;
}
.stButton > button:hover { opacity: .85; }

/* Botão de nav ativo */
.nav-active > button {
    background: #1e3a5f !important;
    border-left: 3px solid var(--accent) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

.chat-bubble-user {
    background: var(--accent);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    margin: 6px 0;
    max-width: 80%;
    margin-left: auto;
    font-size: .95rem;
    word-wrap: break-word;
}

.tool-badge {
    display: block;
    background: #1a1f2e;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    border-radius: 6px;
    padding: 6px 10px;
    font-family: monospace;
    font-size: .78rem;
    color: var(--accent2);
    margin: 4px 0;
}

.jarvis-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.jarvis-card:hover { border-color: var(--accent); }

.pill-ok  { background:#064e3b; color:var(--success); padding:2px 10px; border-radius:99px; font-size:.8rem; font-weight:600; }
.pill-err { background:#450a0a; color:var(--danger);  padding:2px 10px; border-radius:99px; font-size:.8rem; font-weight:600; }

[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
}

.stTabs [data-baseweb="tab-list"]  { gap: 8px; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"]       { border-radius: 8px 8px 0 0; color: var(--muted); padding: 8px 18px; }
.stTabs [aria-selected="true"]     { background: var(--surface) !important; color: var(--accent) !important; border-bottom: 2px solid var(--accent); }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "messages":       [],
    "historico_llm":  [],
    "tool_logs":      [],
    "tarefas":        [],
    "agenda":         [],
    "docs_loaded":    [],
    "active_page":    "chat",
    "sidebar_collapsed": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Cabeçalho com botão de minimizar
    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        if not st.session_state.sidebar_collapsed:
            st.markdown("## 🎓 JARVIS")
    #with col_toggle:
    #    toggle_label = "◀" if not st.session_state.sidebar_collapsed else "▶"
    #    toggle_help  = "Minimizar menu" if not st.session_state.sidebar_collapsed else "Expandir menu"
    #    if st.button(toggle_label, key="toggle_sidebar", help=toggle_help):
    #        st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
    #        st.rerun()

    st.markdown("---")

    pages = {
        "💬": ("chat",   "Chat"),
        "📅": ("agenda", "Agenda"),
        "✅": ("tarefas","Tarefas"),
        "📚": ("rag",    "Materiais RAG"),
        "📊": ("plan",   "Planejamento"),
        "🔧": ("logs",   "Logs"),
    }

    collapsed = st.session_state.sidebar_collapsed

    for icon, (key, label) in pages.items():
        active      = st.session_state.active_page == key
        btn_label   = icon if collapsed else f"{icon} {label}"
        btn_type    = "primary" if active else "secondary"

        if st.button(btn_label, key=f"nav_{key}", use_container_width=True, type=btn_type):
            st.session_state.active_page = key
            st.rerun()

    if not collapsed:
        st.markdown("---")
        st.caption(f"💬 Mensagens: {len(st.session_state.messages)}")
        st.caption(f"📄 Docs: {len(st.session_state.docs_loaded)}")
        st.caption(f"⚙ Tool calls: {len(st.session_state.tool_logs)}")

# ── Roteamento ────────────────────────────────────────────────────────────────
page = st.session_state.active_page

if page == "chat":
    from interface.chat import render
elif page == "agenda":
    from interface.agenda import render
elif page == "tarefas":
    from interface.tarefas import render
elif page == "rag":
    from interface.rag import render
elif page == "plan":
    from interface.planejamento import render
elif page == "logs":
    from interface.logs import render

render()
