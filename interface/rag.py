# -*- coding: utf-8 -*-
"""
interface/rag.py — Materiais RAG.

Upload salva em data/raw/ e dispara indexação via src/rag/.
Remoção apaga o arquivo e reindexa tudo sem o documento removido.
"""

import streamlit as st
from pathlib import Path

RAW_DIR = Path("data/raw")


def _indexar_tudo():
    """Reindexa todos os PDFs em data/raw/ do zero."""
    from src.rag.loader   import carregar_todos_pdfs, salvar_markdown
    from src.rag.chunker  import chunkar_documento
    from src.rag.embedder import construir_indices, salvar_indices

    documentos = carregar_todos_pdfs(str(RAW_DIR))
    if not documentos:
        return 0

    for doc in documentos:
        salvar_markdown(doc["markdown"], doc["arquivo"])

    todos_chunks = []
    for doc in documentos:
        todos_chunks.extend(chunkar_documento(doc))

    indice_faiss, indice_bm25, matriz = construir_indices(todos_chunks)
    salvar_indices(todos_chunks, indice_faiss, indice_bm25, matriz)
    return len(todos_chunks)


def _indexar_pdf(caminho: Path):
    """Adiciona um único PDF aos índices existentes."""
    from src.rag.loader   import pdf_para_markdown, salvar_markdown
    from src.rag.chunker  import chunkar_documento
    from src.rag.embedder import adicionar_chunks

    markdown = pdf_para_markdown(caminho)
    salvar_markdown(markdown, caminho)
    doc    = {"nome": caminho.stem, "arquivo": str(caminho), "markdown": markdown}
    chunks = chunkar_documento(doc)
    adicionar_chunks(chunks)
    return len(chunks)


def render():
    st.markdown("# 📚 Materiais de Estudo (RAG)")
    st.caption("Documentos indexados ficam em `data/raw/`. Upload processa e indexa automaticamente.")

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    tab_upload, tab_gerenciar = st.tabs(["📤 Upload", "📁 Gerenciar documentos"])

    # ── Upload ────────────────────────────────────────────────────────────────
    with tab_upload:
        uploaded = st.file_uploader(
            "Selecione PDFs para adicionar ao acervo",
            type=["pdf"],
            accept_multiple_files=True,
            key="rag_uploader",
        )

        if uploaded:
            if st.button("⚙️ Salvar e indexar", use_container_width=True, type="primary"):
                progress = st.progress(0, text="Salvando arquivos...")
                total_chunks = 0

                for idx, f in enumerate(uploaded):
                    dest = RAW_DIR / f.name
                    dest.write_bytes(f.read())
                    progress.progress((idx + 1) / len(uploaded), text=f"Indexando {f.name}…")

                    try:
                        chunks = _indexar_pdf(dest)
                        total_chunks += chunks
                    except Exception as e:
                        st.warning(f"⚠️ Erro ao indexar {f.name}: {e}")

                progress.progress(1.0, text="✅ Concluído!")
                st.success(f"✅ {len(uploaded)} arquivo(s) indexado(s) — {total_chunks} chunks gerados.")
                st.rerun()

    # ── Gerenciar ─────────────────────────────────────────────────────────────
    with tab_gerenciar:
        from src.rag.paths import indices_existem

        pdfs = sorted(RAW_DIR.glob("*.pdf"))

        if not pdfs:
            st.info("Nenhum documento em `data/raw/`. Faça upload na aba acima.")
        else:
            st.markdown(f"**{len(pdfs)} documento(s) no acervo**")

            for pdf in pdfs:
                size = f"{pdf.stat().st_size / 1024:.1f} KB"
                col_nome, col_size, col_del = st.columns([0.6, 0.2, 0.2])

                with col_nome:
                    st.markdown(
                        f'<div style="background:#13161e;border:1px solid #1e2330;'
                        f'border-radius:8px;padding:8px 14px;margin-bottom:4px;">'
                        f'<span style="color:#4f8ef7;font-size:.8rem;">PDF</span> '
                        f'<span style="color:#e2e8f0;">{pdf.name}</span></div>',
                        unsafe_allow_html=True,
                    )
                with col_size:
                    st.markdown(f"<br><span style='color:#64748b;font-size:.85rem;'>{size}</span>",
                                unsafe_allow_html=True)
                with col_del:
                    if st.button("🗑 Remover", key=f"del_pdf_{pdf.name}", use_container_width=True):
                        pdf.unlink()
                        # Reindexar tudo sem o arquivo removido
                        with st.spinner(f"Removendo {pdf.name} e reindexando..."):
                            try:
                                n = _indexar_tudo()
                                st.success(f"✅ Removido. Índices reconstruídos com {n} chunks.")
                            except Exception as e:
                                st.warning(f"Arquivo removido, mas erro ao reindexar: {e}")
                        st.rerun()

        st.markdown("---")
        col_re, col_status = st.columns(2)

        with col_re:
            if st.button("🔄 Reindexar tudo", use_container_width=True):
                with st.spinner("Reindexando todos os documentos..."):
                    try:
                        n = _indexar_tudo()
                        st.success(f"✅ Reindexação completa — {n} chunks gerados.")
                    except Exception as e:
                        st.error(f"Erro: {e}")

        with col_status:
            status = "✅ Índices existem" if indices_existem() else "⚠️ Índices não gerados"
            st.markdown(f"<br><span style='font-size:.9rem;'>{status}</span>", unsafe_allow_html=True)
