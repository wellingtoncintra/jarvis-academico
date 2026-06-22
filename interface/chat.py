"""
interface/chat.py — Chat principal com histórico persistido no session_state.
"""

import streamlit as st
from src.agent import processar_mensagem


def render():
    st.markdown("# 💬 Chat com JARVIS")
    st.caption("Faça perguntas sobre seus materiais, agenda, tarefas ou peça um plano de estudos.")

    # Garante que o histórico existe no session_state
    if "historico_llm" not in st.session_state:
        st.session_state.historico_llm = []

    # Mensagem pendente injetada por outra aba (ex: Planejamento → "Gerar plano").
    # É consumida UMA única vez e processada como um envio normal do chat.
    pending = st.session_state.pop("pending_message", None)

    col_chat, col_tools = st.columns([3, 1], gap="medium")

    # ── Coluna de ferramentas ─────────────────────────────────────────────────
    with col_tools:
        st.markdown("### 🔧 Ferramentas")
        st.caption("Chamadas nesta sessão")

        if not st.session_state.tool_logs:
            st.markdown(
                '<div class="jarvis-card" style="color:#64748b;font-size:.85rem;">'
                "Nenhuma ferramenta acionada ainda.</div>",
                unsafe_allow_html=True,
            )
        else:
            for log in reversed(st.session_state.tool_logs[-10:]):
                status_class = "pill-ok" if log.get("status") == "ok" else "pill-err"
                status_text  = "✓ ok"    if log.get("status") == "ok" else "✗ erro"
                ts = log.get("timestamp", "")
                if "T" in ts:
                    ts = ts.split("T")[1]  # só o horário (HH:MM:SS)
                st.markdown(
                    f'<div class="jarvis-card" style="padding:10px 12px;">'
                    f'<div style="font-family:monospace;font-size:.75rem;color:#a78bfa;">⚙ {log["tool"]}</div>'
                    f'<div style="font-size:.75rem;color:#64748b;margin:2px 0;">{ts}</div>'
                    f'<span class="{status_class}">{status_text}</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # ── Área de chat ──────────────────────────────────────────────────────────
    with col_chat:
        chat_container = st.container(height=520)
        with chat_container:
            if not st.session_state.messages:
                st.markdown(
                    '<div style="text-align:center;color:#64748b;margin-top:80px;">'
                    '<div style="font-size:2.5rem;">🎓</div>'
                    '<div style="font-size:1.1rem;margin-top:8px;">Olá! Sou o JARVIS.</div>'
                    '<div style="font-size:.9rem;margin-top:4px;">'
                    "Pergunte sobre seus materiais, agenda ou tarefas.</div></div>",
                    unsafe_allow_html=True,
                )
            else:
                for msg in st.session_state.messages:
                    role    = msg["role"]
                    content = msg["content"]

                    if role == "user":
                        st.markdown(
                            f'<div class="chat-bubble-user">{content}</div>',
                            unsafe_allow_html=True,
                        )
                    elif role == "assistant":
                        # Usa st.chat_message para renderizar markdown corretamente
                        with st.chat_message("assistant", avatar="🤖"):
                            st.markdown(content)
                    elif role == "tool_call":
                        st.markdown(
                            f'<div class="tool-badge">⚙ {content}</div>',
                            unsafe_allow_html=True,
                        )

        # ── Input ─────────────────────────────────────────────────────────────
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
                st.session_state.messages        = []
                st.session_state.historico_llm   = []
                st.session_state.tool_logs       = []
                st.rerun()

        # ── Chips de ação rápida ──────────────────────────────────────────────
        chip_cols = st.columns(4)
        chips = [
            ("📅 Hoje",    "O que tenho hoje?"),
            ("✅ Tarefas", "Liste minhas tarefas pendentes"),
            ("📚 Resumir", "Resuma o último material carregado"),
            ("📊 Plano",   "Monte um plano de estudos para hoje"),
        ]
        for col, (label, prompt) in zip(chip_cols, chips):
            with col:
                if st.button(label, use_container_width=True, key=f"chip_{label}"):
                    user_input = prompt
                    send       = True

        # ── Processar envio ───────────────────────────────────────────────────
        # Origem do texto: pendência de outra aba tem prioridade sobre o input.
        if pending and pending.strip():
            texto = pending.strip()
        elif send and user_input and user_input.strip():
            texto = user_input.strip()
        else:
            texto = None

        if texto:
            # Adiciona mensagem do usuário imediatamente na tela
            st.session_state.messages.append({"role": "user", "content": texto})

            with st.spinner("JARVIS está pensando..."):
                resultado = processar_mensagem(
                    mensagem=texto,
                    historico=st.session_state.historico_llm,
                )

            # Atualiza histórico LLM para manter contexto entre mensagens
            st.session_state.historico_llm = resultado["historico"]

            # Os logs já vêm com timestamp ISO real (gerado no agente, no
            # momento da chamada). Apenas empilha na sessão, sem sobrescrever.
            for log in resultado["tool_logs"]:
                st.session_state.tool_logs.append(log)

            # Adiciona resposta do assistente
            st.session_state.messages.append({
                "role":    "assistant",
                "content": resultado["resposta"],
            })

            st.rerun()
