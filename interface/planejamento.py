"""pages/planejamento.py — Planejamento de estudos + melhorias de aprendizado."""

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
    st.markdown("# Planejamento de Estudos")
    st.caption("Combine agenda, tarefas e materiais para gerar planos e exercícios de revisão.")

    tab_plano, tab_recall, tab_exercicios = st.tabs([
        "📋 Gerar plano", "🧠 Active Recall", "✏️ Exercícios"
    ])

    # ── Gerar plano ───────────────────────────────────────────────────────────
    with tab_plano:
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
            prompt = (
                f"Monte um plano de estudos para {data_plano.strftime('%d/%m/%Y')}. "
                f"Foco: {foco or 'geral'}. "
                f"Horas disponíveis: {horas_dia}h. "
                f"Estilo: {estilo}. "
                f"Incluir: {', '.join(incluir)}. "
                f"Tarefas pendentes: {[t['titulo'] for t in tarefas if not t.get('concluida')][:5]}. "
                f"Próximas provas: {[e['titulo'] for e in provas_proximas][:3]}."
            )
            st.session_state.messages.append({"role": "user", "content": prompt})
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

    # ── Active Recall ─────────────────────────────────────────────────────────
    with tab_recall:
        st.markdown("### 🧠 Active Recall — o sistema pergunta, você responde")
        st.caption("Técnica de memorização ativa: responder perguntas consolida o aprendizado.")

        if not st.session_state.docs_loaded:
            st.info("📚 Carregue materiais na aba **Materiais RAG** para gerar perguntas automaticamente.")
        else:
            topico = st.text_input(
                "Tópico para praticar",
                placeholder="Ex: Regressão logística, Redes neurais…",
                key="recall_topico",
            )
            dificuldade = st.select_slider(
                "Dificuldade", ["Básico", "Intermediário", "Avançado"], value="Intermediário"
            )

            if st.button("🎲 Gerar pergunta", use_container_width=False):
                prompt = (
                    f"Gere UMA pergunta de nível {dificuldade.lower()} sobre o tópico '{topico or 'do material carregado'}'. "
                    "Após a pergunta, adicione uma tag <gabarito> com a resposta correta. "
                    "Não mostre o gabarito diretamente, apenas gere a pergunta."
                )
                st.session_state["recall_question"] = f"[Pergunta gerada pelo JARVIS sobre: {topico}]"
                st.session_state["recall_show"] = False

            if st.session_state.get("recall_question"):
                st.markdown(f"""
                <div class="jarvis-card" style="border-left:4px solid #a78bfa;">
                    <div style="color:#a78bfa;font-size:.8rem;margin-bottom:4px;">PERGUNTA</div>
                    <div style="font-size:1rem;">{st.session_state["recall_question"]}</div>
                </div>
                """, unsafe_allow_html=True)

                resposta = st.text_area("Sua resposta", height=100, key="recall_resp")

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Verificar resposta", use_container_width=True):
                        if resposta.strip():
                            prompt_check = (
                                f"Pergunta: {st.session_state['recall_question']}\n"
                                f"Resposta do aluno: {resposta}\n"
                                "Avalie a resposta (correta / parcialmente correta / incorreta) "
                                "e forneça feedback construtivo em português."
                            )
                            st.session_state.messages.append({"role": "user", "content": prompt_check})
                            st.session_state.active_page = "chat"
                            st.rerun()
                        else:
                            st.warning("Digite sua resposta antes de verificar.")
                with col_b:
                    if st.button("👁 Ver gabarito", use_container_width=True):
                        st.session_state["recall_show"] = True

                if st.session_state.get("recall_show"):
                    st.success("💡 Gabarito: [Será exibido após geração pela LLM]")

    # ── Exercícios ─────────────────────────────────────────────────────────────
    with tab_exercicios:
        st.markdown("### ✏️ Geração de exercícios")
        st.caption("Crie exercícios personalizados a partir dos seus materiais.")

        c1, c2 = st.columns(2)
        with c1:
            materia  = st.text_input("Matéria / Tópico", placeholder="Ex: Machine Learning")
            qtd      = st.slider("Quantidade de questões", 1, 10, 5)
        with c2:
            tipo_ex  = st.multiselect(
                "Tipo de exercício",
                ["Múltipla escolha", "Verdadeiro/Falso", "Discursiva", "Complete a lacuna"],
                default=["Múltipla escolha"],
            )
            nivel    = st.select_slider("Nível", ["Básico", "Intermediário", "Avançado"])

        contexto_extra = st.text_area(
            "Contexto adicional (opcional)",
            placeholder="Cole aqui trechos ou instruções específicas…",
            height=80,
        )

        if st.button("🎓 Gerar exercícios", use_container_width=True, type="primary"):
            prompt = (
                f"Gere {qtd} exercício(s) de {nivel.lower()} sobre '{materia}'. "
                f"Tipos: {', '.join(tipo_ex)}. "
                f"{'Contexto extra: ' + contexto_extra if contexto_extra else ''} "
                "Formate cada questão com número, enunciado e gabarito ao final."
            )
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.active_page = "chat"
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Histórico de dificuldades")
        st.caption("Identifica automaticamente tópicos onde você erra mais.")

        dificuldades = st.session_state.get("dificuldades", {
            "Redes Neurais":      3,
            "Backpropagation":    5,
            "Regularização":      2,
            "Embeddings":         1,
        })

        if dificuldades:
            for topico_d, erros in sorted(dificuldades.items(), key=lambda x: -x[1]):
                nivel_d = "Alta" if erros >= 4 else "Média" if erros >= 2 else "Baixa"
                cor_d   = "#f87171" if nivel_d == "Alta" else "#fbbf24" if nivel_d == "Média" else "#34d399"
                barra   = min(erros / 6, 1.0)

                st.markdown(f"""
                <div class="jarvis-card" style="padding:10px 14px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;">{topico_d}</span>
                        <span style="background:{cor_d}22;color:{cor_d};border-radius:6px;padding:1px 8px;font-size:.75rem;">{nivel_d}</span>
                    </div>
                    <div style="background:#1e2330;border-radius:4px;height:6px;margin-top:6px;">
                        <div style="background:{cor_d};height:6px;width:{barra*100:.0f}%;border-radius:4px;transition:width .3s;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Nenhum dado de dificuldade ainda. Pratique com o Active Recall!")
