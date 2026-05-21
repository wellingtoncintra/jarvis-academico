# Documentação do Dataset

## Visão Geral

| # | Arquivo | Origem | Tipo | Limitações |
|---|---------|--------|------|-----------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |

---

## Estratégia de Chunking

- **Tamanho do chunk:** 500 tokens
- **Overlap:** 50 tokens
- **Método:** RecursiveCharacterTextSplitter (LangChain)

### Por que esses valores?

Chunks de 500 tokens preservam contexto suficiente para respostas coerentes sem
ultrapassar o limite de contexto da LLM. O overlap de 50 tokens evita que conceitos
que aparecem na fronteira entre dois chunks sejam perdidos na recuperação.

### Impacto no RAG

- Chunks menores (< 200 tokens): maior precisão na recuperação, mas respostas
  sem contexto suficiente.
- Chunks maiores (> 1000 tokens): respostas mais completas, mas recuperação menos
  precisa — trechos irrelevantes contaminam o contexto enviado à LLM.
- **Nossa escolha (500 tokens):** equilíbrio entre precisão e completude.

---

## Fontes dos Dados

(Descrever aqui a origem de cada documento, ex: apostila da disciplina X,
artigo do arXiv, slides do professor Y, etc.)
