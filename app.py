import streamlit as st

st.set_page_config(
    page_title="JARVIS Acadêmico",
    page_icon="img/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600;700&display=swap');

:root {
    --bg:       #0d0f14;
    --surface:  #13161e;
    --border:   #1e2330;
    --accent:   #286bde;
    --accent2:  #a78bfa;
    --success:  #34d399;
    --warning:  #fbbf24;
    --danger:   #f87171;
    --accent-hover: #4f8ef7;
    --accent-active: #075df2;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --mono:     'Space Mono', monospace;
    --sans:     'Sora', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg);
    color: var(--text);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Buttons */
.stButton > button {
    background: var(--accent);
    color: #fff !important;
    border: none;
    border-radius: 8px;
    font-family: var(--sans);
    font-weight: 600;
    transition: background .2s, transform .15s;
}
.stButton > button:hover,
.stButton > button:focus,
.stButton > button:focus-visible {
    background: var(--accent-hover) !important;
    color: #fff !important;
}
.stButton > button:active {
    background: var(--accent-active) !important;
    color: #fff !important;
    transform: translateY(1px);
}
.stButton > button[disabled] {
    opacity: .6;
    cursor: not-allowed;
}

/* Text inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: var(--sans) !important;
}

/* Chat messages */
.chat-bubble-user {
    background: var(--accent);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    margin: 4px 0;
    max-width: 80%;
    margin-left: auto;
    font-size: .95rem;
}
.chat-bubble-ai {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    margin: 4px 0;
    max-width: 85%;
    font-size: .95rem;
}

/* Tool log badge */
.tool-badge {
    display: inline-block;
    background: #1a1f2e;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    border-radius: 6px;
    padding: 6px 10px;
    font-family: var(--mono);
    font-size: .78rem;
    color: var(--accent2);
    margin: 4px 0;
    width: 100%;
}

/* Cards */
.jarvis-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.jarvis-card:hover { border-color: var(--accent); }

/* Status pills */
.pill-ok   { background:#064e3b; color:var(--success); padding:2px 10px; border-radius:99px; font-size:.8rem; font-weight:600; }
.pill-warn { background:#451a03; color:var(--warning); padding:2px 10px; border-radius:99px; font-size:.8rem; font-weight:600; }
.pill-err  { background:#450a0a; color:var(--danger);  padding:2px 10px; border-radius:99px; font-size:.8rem; font-weight:600; }

/* Headings */
h1, h2, h3 { font-family: var(--sans); font-weight: 700; }
h1 { font-size: 1.9rem; }
h2 { font-size: 1.3rem; color: var(--accent); }

/* Metric override */
[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"]  { gap: 8px; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"]       { border-radius: 8px 8px 0 0; color: var(--muted); padding: 8px 18px; font-family: var(--sans); }
.stTabs [aria-selected="true"]     { background: var(--surface) !important; color: var(--accent) !important; border-bottom: 2px solid var(--accent); }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

.e1q5ojhd0 {
    display: flex;
    justify-content: center;
    align-items: center;
}
.et0utro0 {
    display: none;
}
[data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
defaults = {
    "messages":     [],
    "tool_logs":    [],
    "tarefas":      [],
    "agenda":       [],
    "docs_loaded":  [],
    "active_page":  "chat",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <style>
        .st-emotion-cache-7czcpc > img {
            margin-top: -54px;
            margin-bottom: -24px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.image("img/logo.png", width=180)
    st.markdown("---")

    pages = {
        "Chat":          "chat",
        "Agenda":        "agenda",
        "Tarefas":       "tarefas",
        "Materiais RAG": "rag",
        "Planejamento":  "plan",
        "Logs":          "logs",
    }
    for label, key in pages.items():
        active = st.session_state.active_page == key
        style  = "color: #4f8ef7 !important; font-weight: 700;" if active else ""
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.active_page = key
            st.rerun()

    st.markdown("---")
    st.caption(f"Mensagens: {len(st.session_state.messages)}")
    st.caption(f"Docs carregados: {len(st.session_state.docs_loaded)}")
    st.caption(f"Tool calls: {len(st.session_state.tool_logs)}")

# ── Route to page ─────────────────────────────────────────────────────────────
page = st.session_state.active_page

if page == "chat":
    from interface.chat import render
    render()
elif page == "agenda":
    from interface.agenda import render
    render()
elif page == "tarefas":
    from interface.tarefas import render
    render()
elif page == "rag":
    from interface.rag import render
    render()
elif page == "plan":
    from interface.planejamento import render
    render()
elif page == "logs":
    from interface.logs import render
    render()