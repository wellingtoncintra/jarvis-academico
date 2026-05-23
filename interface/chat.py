"""
pages/chat.py
Página principal de chat — integra LLM (Gemma 12B via Ollama/OpenAI-compat),
tool calling e exibe logs de ferramentas em tempo real.
"""

import streamlit as st
from src.agent import processar_mensagem

def render():
    st.markdown("# 💬 Chat com JARVIS")
    st.caption("Faça perguntas sobre seus materiais, agenda, tarefas ou peça um plano de estudos.")


    historico = []

    # ── Layout: chat | tool sidebar ──────────────────────────────────────────
    col_chat, col_tools = st.columns([3, 1], gap="medium")

    # ── Tool sidebar ─────────────────────────────────────────────────────────
    with col_tools:
        st.markdown("### 🔧 Ferramentas")
        st.caption("Chamadas realizadas nesta sessão")

        if not st.session_state.tool_logs:
            st.markdown(
                '<div class="jarvis-card" style="color:#64748b;font-size:.85rem;">Nenhuma ferramenta acionada ainda.</div>',
                unsafe_allow_html=True,
            )
        else:
            for log in reversed(st.session_state.tool_logs[-10:]):
                status_class = "pill-ok" if log.get("status") == "ok" else "pill-err"
                status_text  = "✓ ok" if log.get("status") == "ok" else "✗ erro"
                st.markdown(f"""
                <div class="jarvis-card" style="padding:10px 12px;">
                    <div style="font-family:var(--mono);font-size:.75rem;color:#a78bfa;">⚙ {log['tool']}</div>
                    <div style="font-size:.75rem;color:#64748b;margin:2px 0;">{log['ts']}</div>
                    <span class="{status_class}">{status_text}</span>
                </div>
                """, unsafe_allow_html=True)

        #st.markdown("---")
        #st.markdown("**Ferramentas disponíveis**")
        #for t in TOOLS:
        #    st.markdown(f"<div class='tool-badge'>⚙ {t['function']['name']}</div>", unsafe_allow_html=True)

    # ── Chat area ─────────────────────────────────────────────────────────────
    with col_chat:
        # Message history
        chat_container = st.container(height=520)
        with chat_container:
            if not st.session_state.messages:
                st.markdown("""
                <div style="text-align:center;color:#64748b;margin-top:80px;">
                    <div style="font-size:2.5rem;">🎓</div>
                    <div style="font-size:1.1rem;margin-top:8px;">Olá! Sou o JARVIS.</div>
                    <div style="font-size:.9rem;margin-top:4px;">
                        Pergunte sobre seus materiais, agenda ou tarefas.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        st.markdown(
                            f'<div class="chat-bubble-user">{msg["content"]}</div>',
                            unsafe_allow_html=True,
                        )
                    elif msg["role"] == "assistant":
                        st.markdown(
                            f'<div class="chat-bubble-ai">🤖 {msg["content"]}</div>',
                            unsafe_allow_html=True,
                        )
                    elif msg["role"] == "tool_call":
                        st.markdown(
                            f'<div class="tool-badge">⚙ {msg["content"]}</div>',
                            unsafe_allow_html=True,
                        )

        # ── Input row ─────────────────────────────────────────────────────────
        with st.container():
            inp_col, btn_col, clr_col = st.columns([6, 1, 1])
            with inp_col:
                user_input = st.text_input(
                    "Mensagem",
                    placeholder="Ex: O que tenho amanhã? / Explique regressão logística...",
                    label_visibility="collapsed",
                    key="chat_input",
                )
            with btn_col:
                send = st.button("Enviar", use_container_width=True)
            with clr_col:
                if st.button("Limpar", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()

        # ── Quick-action chips ────────────────────────────────────────────────
        chip_cols = st.columns(4)
        chips = [
            ("📅 Hoje", "O que tenho hoje?"),
            ("✅ Tarefas", "Liste minhas tarefas pendentes"),
            ("📚 Resumir", "Resuma o último material carregado"),
            ("📊 Plano", "Monte um plano de estudos para hoje"),
        ]
        for col, (label, prompt) in zip(chip_cols, chips):
            with col:
                if st.button(label, use_container_width=True, key=f"chip_{label}"):
                    user_input = prompt
                    send = True

        # ── Process send ──────────────────────────────────────────────────────
        if send and user_input and user_input.strip():
            historico = processar_mensagem(user_input.strip(),historico)
            st.rerun()