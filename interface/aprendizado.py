"""interface/aprendizado.py — Melhorias de aprendizado: Active Recall + Exercícios.

Duas funcionalidades de aprendizado exigidas pelo Trabalho 2:
  - Active Recall (interativa): o sistema pergunta, o aluno responde e o sistema avalia.
  - Geração de exercícios (múltipla escolha): gerados a partir dos materiais (RAG)
    e renderizados na própria aba, sem depender do chat.

Ambas as funcionalidades são ancoradas no RAG: as perguntas e os exercícios
nascem dos materiais que o aluno indexou, não do conhecimento geral da LLM.
"""

import streamlit as st

from src.utils import extrair_json as _extrair_json


def _classificar_feedback(feedback: str) -> str:
    """
    Normaliza o texto de feedback da avaliação em uma classificação canônica:
    'correta', 'parcial' ou 'incorreta'.

    A avaliação (AVALIACAO_SYSTEM) instrui o Gemma a iniciar a resposta com
    CORRETA / PARCIALMENTE / INCORRETA. Mapeamos esse prefixo; qualquer outro
    formato cai em 'incorreta' por segurança (sinaliza tentativa não bem-sucedida).
    """
    fb_up = (feedback or "").strip().upper()
    if fb_up.startswith("CORRETA"):
        return "correta"
    if fb_up.startswith("PARCIALMENTE"):
        return "parcial"
    return "incorreta"


# ── Active Recall: geração e avaliação ────────────────────────────────────────

def gerar_pergunta_recall(topico: str, dificuldade: str, k: int = 3) -> dict:
    """
    Gera uma pergunta de Active Recall a partir dos materiais indexados (RAG).

    Fluxo:
        1. Recupera trechos relevantes dos PDFs do aluno via busca híbrida
        2. Pede ao Gemma uma pergunta + gabarito baseados SÓ nesses trechos
        3. Retorna {"pergunta": str, "gabarito": str, "fontes": [str]}

    Em caso de falha de parsing, devolve {"erro": ...}.
    """
    # Import lazy: só carrega o stack de RAG quando o recurso é usado de fato.
    from src.rag.retriever import buscar_hibrido
    from src.llm.client import chat
    from src.prompts import aprendizado as p

    consulta = topico.strip() or "conceitos centrais do material"
    chunks = buscar_hibrido(consulta, k=k)

    if not chunks:
        return {"erro": "Não encontrei trechos relevantes nos materiais para esse tópico."}

    contexto = "\n\n".join(
        f"Trecho {i+1} (fonte: {c['fonte']}):\n{c['texto']}"
        for i, c in enumerate(chunks)
    )
    fontes = sorted({c["fonte"] for c in chunks})

    resposta = chat(p.recall_user(dificuldade, consulta, contexto), system_prompt=p.RECALL_SYSTEM)
    dados = _extrair_json(resposta)

    if not dados or "pergunta" not in dados or "gabarito" not in dados:
        return {"erro": "A LLM não retornou um JSON válido. Tente gerar novamente."}

    return {
        "pergunta": dados["pergunta"].strip(),
        "gabarito": dados["gabarito"].strip(),
        "fontes":   fontes,
    }


def avaliar_resposta_recall(pergunta: str, gabarito: str, resposta_aluno: str) -> str:
    """
    Avalia a resposta do aluno comparando-a ao gabarito, via Gemma.
    Retorna o texto do feedback (com classificação correta/parcial/incorreta).
    """
    from src.llm.client import chat
    from src.prompts import aprendizado as p

    return chat(
        p.avaliacao_user(pergunta, gabarito, resposta_aluno),
        system_prompt=p.AVALIACAO_SYSTEM,
    )


# ── Geração de exercícios (múltipla escolha) ──────────────────────────────────

def gerar_exercicios(topico: str, qtd: int, nivel: str) -> dict:
    """
    Gera exercícios de múltipla escolha a partir dos materiais indexados (RAG).

    A quantidade de chunks recuperados é proporcional ao número de questões
    (mais questões → mais contexto), com teto para não inchar o prompt.

    Retorna {"questoes": [...], "fontes": [...]} ou {"erro": ...}.
    Cada questão: {"enunciado", "alternativas": {"A":..,"B":..,"C":..,"D":..},
                   "correta": "A".."D", "explicacao"}.
    """
    from src.rag.retriever import buscar_hibrido
    from src.llm.client import chat
    from src.prompts import aprendizado as p

    consulta = topico.strip() or "conceitos centrais do material"
    k = min(qtd + 2, 8)  # contexto proporcional ao nº de questões, teto 8
    chunks = buscar_hibrido(consulta, k=k)

    if not chunks:
        return {"erro": "Não encontrei trechos relevantes nos materiais para esse tópico."}

    contexto = "\n\n".join(
        f"Trecho {i+1} (fonte: {c['fonte']}):\n{c['texto']}"
        for i, c in enumerate(chunks)
    )
    fontes = sorted({c["fonte"] for c in chunks})

    resposta = chat(p.exercicios_user(qtd, nivel, consulta, contexto), system_prompt=p.EXERCICIOS_SYSTEM)
    dados = _extrair_json(resposta)

    if not dados or "questoes" not in dados or not isinstance(dados["questoes"], list):
        return {"erro": "A LLM não retornou um JSON válido. Tente gerar novamente."}

    # Filtra questões malformadas (sem alternativas ou sem correta)
    questoes = [
        q for q in dados["questoes"]
        if isinstance(q, dict) and q.get("enunciado")
        and isinstance(q.get("alternativas"), dict) and q.get("correta")
    ]
    if not questoes:
        return {"erro": "Os exercícios vieram em formato inesperado. Tente novamente."}

    return {"questoes": questoes, "fontes": fontes}


# ── Página ────────────────────────────────────────────────────────────────────

def render():
    st.markdown("# 🧠 Melhoria de Aprendizagem")
    st.caption("Pratique com perguntas de recordação ativa e exercícios gerados dos seus materiais.")

    from src.rag.paths import indices_existem

    tab_recall, tab_exercicios = st.tabs(["🧠 Active Recall", "✏️ Exercícios"])

    # ── Active Recall ─────────────────────────────────────────────────────────
    with tab_recall:
        st.markdown("### Active Recall — o sistema pergunta, você responde")
        st.caption("Técnica de memorização ativa: responder perguntas consolida o aprendizado.")

        if not indices_existem():
            st.info("📚 Nenhum material indexado ainda. Faça upload na aba **Materiais RAG** para gerar perguntas.")
        else:
            topico = st.text_input(
                "Tópico para praticar",
                placeholder="Ex: Autômatos finitos, Gramáticas livres de contexto…",
                key="recall_topico",
            )
            dificuldade = st.select_slider(
                "Dificuldade", ["Básico", "Intermediário", "Avançado"], value="Intermediário"
            )

            if st.button("🎲 Gerar pergunta", use_container_width=False):
                with st.spinner("Gerando pergunta a partir dos seus materiais…"):
                    resultado = gerar_pergunta_recall(topico, dificuldade)

                if "erro" in resultado:
                    st.warning(resultado["erro"])
                else:
                    st.session_state["recall_question"] = resultado["pergunta"]
                    st.session_state["recall_gabarito"] = resultado["gabarito"]
                    st.session_state["recall_fontes"]   = resultado.get("fontes", [])
                    st.session_state["recall_show"]      = False
                    st.session_state["recall_feedback"]  = None

            if st.session_state.get("recall_question"):
                fontes = st.session_state.get("recall_fontes", [])
                fontes_html = (
                    f'<div style="color:#64748b;font-size:.72rem;margin-top:8px;">'
                    f'📎 Fontes: {", ".join(fontes)}</div>'
                    if fontes else ""
                )
                st.markdown(f"""
                <div class="jarvis-card" style="border-left:4px solid #a78bfa;">
                    <div style="color:#a78bfa;font-size:.8rem;margin-bottom:4px;">PERGUNTA</div>
                    <div style="font-size:1rem;">{st.session_state["recall_question"]}</div>
                    {fontes_html}
                </div>
                """, unsafe_allow_html=True)

                resposta = st.text_area("Sua resposta", height=100, key="recall_resp")

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Verificar resposta", use_container_width=True):
                        if resposta.strip():
                            with st.spinner("JARVIS está avaliando sua resposta…"):
                                feedback = avaliar_resposta_recall(
                                    st.session_state["recall_question"],
                                    st.session_state.get("recall_gabarito", ""),
                                    resposta,
                                )
                            st.session_state["recall_feedback"] = feedback

                            # Item 12 — registra o desempenho UMA vez, aqui no
                            # handler do clique (não no bloco de render abaixo,
                            # que reexecuta a cada rerun e duplicaria o registro).
                            from src.storage import registrar_tentativa
                            classificacao = _classificar_feedback(feedback)
                            registrar_tentativa(
                                topico=st.session_state.get("recall_topico", ""),
                                classificacao=classificacao,
                            )
                        else:
                            st.warning("Digite sua resposta antes de verificar.")
                with col_b:
                    if st.button("👁 Ver gabarito", use_container_width=True):
                        st.session_state["recall_show"] = True

                # Feedback da avaliação (na própria aba)
                if st.session_state.get("recall_feedback"):
                    fb = st.session_state["recall_feedback"]
                    classificacao = _classificar_feedback(fb)
                    if classificacao == "correta":
                        st.success(f"**Avaliação:** {fb}")
                    elif classificacao == "parcial":
                        st.warning(f"**Avaliação:** {fb}")
                    else:
                        st.error(f"**Avaliação:** {fb}")

                # Gabarito real (sob demanda)
                if st.session_state.get("recall_show"):
                    st.success(f"💡 **Gabarito:** {st.session_state.get('recall_gabarito', '—')}")

        # ── Dificuldades identificadas (histórico persistido) ─────────────────
        # Item 12: lê o desempenho agregado por tópico e destaca os mais difíceis.
        # Renderiza fora do bloco de prática para aparecer mesmo sem índice ativo.
        from src.storage import resumo_por_topico, total_tentativas, limpar_desempenho

        if total_tentativas() > 0:
            st.markdown("---")
            col_h, col_r = st.columns([4, 1])
            with col_h:
                st.markdown("### 📊 Suas dificuldades identificadas")
                st.caption("Aproveitamento por tópico, com base no seu histórico de recordação ativa.")
            with col_r:
                if st.button("🗑 Limpar histórico", use_container_width=True, key="limpar_desempenho"):
                    limpar_desempenho()
                    st.rerun()

            for r in resumo_por_topico():
                aprov = r["aproveitamento"]
                cor = "#34d399" if aprov >= 70 else ("#fbbf24" if aprov >= 40 else "#f87171")
                st.markdown(f"""
                <div class="jarvis-card" style="border-left:4px solid {cor};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="font-size:1rem;font-weight:600;">{r["topico"]}</div>
                        <div style="color:{cor};font-weight:700;">{aprov:.0f}%</div>
                    </div>
                    <div style="color:#64748b;font-size:.78rem;margin-top:4px;">
                        {r["total"]} tentativa(s) · ✅ {r["corretas"]} · ◐ {r["parciais"]} · ✗ {r["incorretas"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Exercícios (múltipla escolha) ─────────────────────────────────────────
    with tab_exercicios:
        st.markdown("### Geração de exercícios")
        st.caption("Exercícios de múltipla escolha criados a partir dos seus materiais.")

        if not indices_existem():
            st.info("📚 Nenhum material indexado ainda. Faça upload na aba **Materiais RAG** para gerar exercícios.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                materia = st.text_input(
                    "Matéria / Tópico",
                    placeholder="Ex: Autômatos finitos",
                    key="ex_topico",
                )
                qtd = st.slider("Quantidade de questões", 1, 8, 3, key="ex_qtd")
            with c2:
                nivel = st.select_slider(
                    "Nível", ["Básico", "Intermediário", "Avançado"],
                    value="Intermediário", key="ex_nivel",
                )

            if st.button("🎓 Gerar exercícios", use_container_width=True, type="primary"):
                with st.spinner("Gerando exercícios a partir dos seus materiais…"):
                    resultado = gerar_exercicios(materia, qtd, nivel)

                if "erro" in resultado:
                    st.warning(resultado["erro"])
                    st.session_state["ex_questoes"] = None
                else:
                    st.session_state["ex_questoes"] = resultado["questoes"]
                    st.session_state["ex_fontes"]   = resultado.get("fontes", [])

            # Renderização das questões na própria aba
            questoes = st.session_state.get("ex_questoes")
            if questoes:
                fontes = st.session_state.get("ex_fontes", [])
                if fontes:
                    st.caption(f"📎 Fontes: {', '.join(fontes)}")

                for idx, q in enumerate(questoes, 1):
                    alternativas = q.get("alternativas", {})
                    alts_html = "".join(
                        f'<div style="margin:4px 0;"><b>{letra})</b> {texto}</div>'
                        for letra, texto in alternativas.items()
                    )
                    st.markdown(f"""
                    <div class="jarvis-card" style="border-left:4px solid #34d399;">
                        <div style="color:#34d399;font-size:.8rem;margin-bottom:6px;">QUESTÃO {idx}</div>
                        <div style="font-size:1rem;margin-bottom:8px;">{q.get("enunciado","")}</div>
                        {alts_html}
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander(f"👁 Ver gabarito da questão {idx}"):
                        correta = q.get("correta", "—")
                        explicacao = q.get("explicacao", "")
                        st.success(f"**Resposta correta: {correta}**")
                        if explicacao:
                            st.markdown(explicacao)
