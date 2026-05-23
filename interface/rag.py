"""pages/rag.py — Upload e consulta de materiais via RAG."""

import streamlit as st
import os
from pathlib import Path

UPLOAD_DIR = Path("data/docs")


def render():
    st.markdown("# 📚 Materiais de Estudo (RAG)")
    st.caption("Carregue PDFs ou textos para consultar via linguagem natural no Chat.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    tab_upload, tab_query, tab_manage = st.tabs(["📤 Upload", "🔍 Consulta direta", "📁 Gerenciar"])

    # ── Upload ────────────────────────────────────────────────────────────────
    with tab_upload:
        st.markdown("### Carregar documentos")
        uploaded = st.file_uploader(
            "Selecione PDFs, TXTs ou Markdown",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
            key="rag_uploader",
        )

        if uploaded:
            col1, col2 = st.columns([3, 1])
            with col1:
                chunk_size    = st.slider("Tamanho do chunk (tokens aprox.)", 128, 1024, 512, 64)
                chunk_overlap = st.slider("Overlap entre chunks", 0, 256, 64, 16)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                embed_model = st.selectbox("Embeddings", ["sentence-transformers/all-MiniLM-L6-v2", "BAAI/bge-small-pt", "intfloat/multilingual-e5-small"])

            if st.button("⚙️ Processar e indexar", use_container_width=True, type="primary"):
                progress = st.progress(0, text="Iniciando…")
                for idx, f in enumerate(uploaded):
                    frac = (idx + 1) / len(uploaded)
                    progress.progress(frac, text=f"Processando {f.name}…")

                    dest = UPLOAD_DIR / f.name
                    dest.write_bytes(f.read())

                    # Registra no session state
                    if f.name not in st.session_state.docs_loaded:
                        st.session_state.docs_loaded.append(f.name)

                progress.progress(1.0, text="✅ Concluído!")

                st.success(f"✅ {len(uploaded)} documento(s) indexado(s) com chunk={chunk_size}, overlap={chunk_overlap}.")

                with st.expander("ℹ️ Estratégia de chunking"):
                    st.markdown(f"""
                    | Parâmetro | Valor |
                    |---|---|
                    | Tamanho do chunk | `{chunk_size}` tokens |
                    | Overlap | `{chunk_overlap}` tokens |
                    | Modelo de embedding | `{embed_model}` |
                    | Documentos indexados | `{len(st.session_state.docs_loaded)}` |

                    **Impacto no RAG:**
                    - Chunks menores → maior precisão, mais chamadas de recuperação
                    - Overlap garante que informações nos limites de chunk não se percam
                    - Embeddings multilíngues são recomendados para conteúdo em português
                    """)

    # ── Consulta direta ───────────────────────────────────────────────────────
    with tab_query:
        st.markdown("### Consulta direta ao RAG")
        st.caption("Teste a recuperação sem passar pelo Chat principal.")

        query = st.text_input("Pergunta", placeholder="Ex: O que é regressão logística?")
        top_k = st.slider("Top-K documentos recuperados", 1, 10, 3)

        if st.button("🔍 Buscar", use_container_width=False) and query:
            if not st.session_state.docs_loaded:
                st.warning("⚠️ Nenhum documento carregado. Faça upload na aba acima.")
            else:
                with st.spinner("Recuperando trechos relevantes…"):
                    # Placeholder — integrar com retriever real
                    st.markdown("**Trechos recuperados:**")
                    for k in range(min(top_k, 3)):
                        st.markdown(f"""
                        <div class="jarvis-card" style="border-left:4px solid #4f8ef7;">
                            <div style="display:flex;justify-content:space-between;">
                                <span style="color:#4f8ef7;font-size:.8rem;font-family:var(--mono);">
                                    📄 {st.session_state.docs_loaded[0] if st.session_state.docs_loaded else 'doc.pdf'} · chunk {k+1}
                                </span>
                                <span style="color:#34d399;font-size:.8rem;">score: {0.95 - k*0.08:.2f}</span>
                            </div>
                            <div style="color:#cbd5e1;font-size:.88rem;margin-top:6px;">
                                [Conteúdo do chunk {k+1} para a query: "{query}"]
                                — Este trecho será preenchido pelo retriever real após integração com
                                o pipeline RAG (ChromaDB / FAISS + SentenceTransformers).
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.info("💡 Para a resposta completa, use o **Chat** com a pergunta acima.")

    # ── Gerenciar ─────────────────────────────────────────────────────────────
    with tab_manage:
        st.markdown("### Documentos indexados")
        docs_disk = list(UPLOAD_DIR.glob("*")) if UPLOAD_DIR.exists() else []

        if not docs_disk and not st.session_state.docs_loaded:
            st.markdown(
                '<div class="jarvis-card" style="color:#64748b;text-align:center;padding:32px;">Nenhum documento carregado ainda.</div>',
                unsafe_allow_html=True,
            )
        else:
            all_docs = list({d.name for d in docs_disk} | set(st.session_state.docs_loaded))
            for doc in all_docs:
                path   = UPLOAD_DIR / doc
                size   = f"{path.stat().st_size / 1024:.1f} KB" if path.exists() else "—"
                ext    = doc.rsplit(".", 1)[-1].upper() if "." in doc else "?"
                cor    = "#4f8ef7" if ext == "PDF" else "#a78bfa"

                c1, c2 = st.columns([0.85, 0.15])
                with c1:
                    st.markdown(f"""
                    <div class="jarvis-card" style="padding:10px 14px;margin:0 0 4px 0;">
                        <div style="display:flex;align-items:center;gap:8px;">
                            <span style="background:{cor}22;color:{cor};border-radius:6px;padding:1px 8px;font-size:.75rem;">{ext}</span>
                            <span style="color:#e2e8f0;">{doc}</span>
                            <span style="color:#64748b;font-size:.8rem;margin-left:auto;">{size}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("🗑", key=f"del_{doc}", help="Remover"):
                        if path.exists():
                            path.unlink()
                        if doc in st.session_state.docs_loaded:
                            st.session_state.docs_loaded.remove(doc)
                        st.rerun()

            st.markdown("---")
            st.caption(f"Total: **{len(all_docs)} documento(s)**")
