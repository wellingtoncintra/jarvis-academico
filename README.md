# Estudantes
Wellington Cintra
Cézar Dias

# Video de Apresentação
Link do Drive: https://drive.google.com/file/d/1WdtwzQcWwUIv2ee02kNfm5m2oOrNGnsn/view?usp=sharing
# 🎓 JARVIS Acadêmico

Assistente pessoal inteligente para estudantes universitários, construído com **Streamlit**, **RAG híbrido (FAISS + BM25)**, **Tool Calling via prompt engineering** e o modelo de linguagem **Gemma 3 12B**.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Executando o Projeto](#executando-o-projeto)
- [Executando os Testes](#executando-os-testes)
- [Dataset](#dataset)
- [Decisões Técnicas](#decisões-técnicas)
- [IAs Utilizadas](#ias-utilizadas)

---

## Visão Geral

O JARVIS integra três componentes principais:

| Componente | Tecnologia | Função |
|---|---|---|
| **LLM** | Gemma 3 12B (servidor do professor) | Geração de respostas e decisão de tool calling |
| **RAG** | FAISS + BM25 + SentenceTransformers | Consulta a materiais de estudo indexados |
| **Tool Calling** | Prompt engineering + `chat.completions` | Execução de ferramentas via JSON estruturado |
| **Storage** | SQLite | Persistência de agenda e tarefas |
| **Interface** | Streamlit | UI web com tema dark |

---

## Arquitetura

```
Usuário (Streamlit)
       ↓
   src/agent.py          ← orquestrador: loop de tool calling
       ↓
   src/llm/client.py     ← cliente OpenAI (chat.completions)
       ↓
   Gemma 3 12B           ← responde com JSON de tool call ou texto final
       ↓
   src/tools/            ← executa a ferramenta e retorna resultado
   ├── agenda.py         ← consultar_agenda, adicionar_agenda
   ├── tarefas.py        ← gerenciar_tarefas (listar/adicionar/concluir)
   ├── rag.py            ← buscar_material_rag
   └── planejamento.py   ← planejar_estudos
       ↓
   src/storage/          ← SQLite (agenda e tarefas)
   src/rag/              ← FAISS + BM25 (materiais de estudo)
```

### Loop do Agente

```
usuário → agente → LLM (system prompt com descrição das tools)
                    ↓ responde: {"tool": "nome", "args": {...}}
          agente → executa tool → resultado
                    ↓
          agente → LLM + resultado
                    ↓ resposta final em texto
usuário ← agente
```

O loop repete até a LLM responder em texto puro (sem JSON de tool), com limite de 5 iterações.

---

## Funcionalidades

### Trabalho 1

**3.1 Consulta a materiais de estudo (RAG)**
- Upload de PDFs via interface web
- Carregamento, chunking, embedding e indexação automáticos
- Busca híbrida (semântica + lexical) com reranking por score combinado
- Respostas geradas pelo Gemma com base nos trechos recuperados

**3.2 Agenda acadêmica**
- Adicionar eventos (aula, prova, evento) com data, hora e descrição
- Consultar por período: hoje, amanhã, semana ou data específica
- Remoção de eventos
- Persistência em SQLite

**3.3 Lista de tarefas**
- Adicionar tarefas com prioridade (alta/média/baixa) e prazo
- Listar pendentes (ordenadas por prioridade) ou todas
- Marcar como concluída ou reabrir
- Remoção de tarefas
- Persistência em SQLite

**Tool Calling (5 ferramentas)**

| Ferramenta | Quando a LLM chama | O que faz |
|---|---|---|
| `consultar_agenda` | "O que tenho hoje?", "Tenho prova amanhã?" | Lê SQLite — agenda |
| `adicionar_agenda` | "Adiciona prova de BD na sexta às 14h" | Escreve SQLite — agenda |
| `gerenciar_tarefas` | "Lista tarefas", "Adiciona tarefa X", "Conclui Y" | Lê/escreve SQLite — tarefas |
| `buscar_material_rag` | "Explique regressão logística" | FAISS + BM25 → Gemma |
| `planejar_estudos` | "Monte um plano para a prova" | Combina agenda + tarefas + RAG |

---

## Estrutura do Projeto

```
jarvis-academico/
├── app.py                      # Entry point Streamlit
├── .env                        # Credenciais (não versionado)
├── requirements.txt
│
├── interface/                  # Páginas Streamlit
│   ├── chat.py                 # Chat com histórico e tool call sidebar
│   ├── agenda.py               # Visualização e cadastro de eventos
│   ├── tarefas.py              # Gerenciamento de tarefas
│   ├── rag.py                  # Upload e indexação de documentos
│   ├── planejamento.py         # Planejamento de estudos
│   └── logs.py                 # Logs de tool calling
│
├── src/
│   ├── agent.py                # Orquestrador: loop de tool calling
│   ├── llm/
│   │   └── client.py           # Cliente OpenAI (chat.completions)
│   ├── rag/
│   │   ├── loader.py           # PDF → Markdown (pymupdf4llm)
│   │   ├── chunker.py          # Estratégia híbrida de chunking
│   │   ├── embedder.py         # FAISS + BM25 + SentenceTransformers
│   │   ├── retriever.py        # Busca e geração de resposta RAG
│   │   └── indexer.py          # Script de indexação standalone
│   ├── storage/
│   │   ├── database.py         # Conexão SQLite + criação de tabelas
│   │   ├── agenda.py           # CRUD de eventos
│   │   └── tarefas.py          # CRUD de tarefas
│   └── tools/
│       ├── agenda.py           # Tools: consultar_agenda, adicionar_agenda
│       ├── tarefas.py          # Tool: gerenciar_tarefas
│       ├── rag.py              # Tool: buscar_material_rag
│       ├── planejamento.py     # Tool: planejar_estudos
│       └── __init__.py         # TOOLS_DEF + executar_tool()
│
├── data/
│   ├── raw/                    # PDFs originais do dataset
│   ├── processed/              # Índices FAISS, BM25 e chunks serializados
│   ├── jarvis.db               # Banco SQLite (agenda e tarefas)
│   └── DATASET.md              # Documentação do dataset
│
└── tests/
    ├── test_storage.py         # Testes de CRUD no SQLite
    └── test_rag.py             # Testes do pipeline de chunking
```

---

## Instalação

**Pré-requisitos:** Python 3.11+

```bash
# Clone o repositório
git clone https://github.com/wellingtoncintra/jarvis-academico.git
cd jarvis-academico

# Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
LLM_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
LLM_API_KEY=seu_token_aqui
LLM_MODEL_NAME=google/gemma-3-12b-it
```

> **Nota:** O endpoint utilizado é a API OpenAI-compatible disponibilizada pelo professor.
> A documentação indica `chat.completions`, que é o endpoint efetivamente usado.

---

## Executando o Projeto

```bash
# A partir da raiz do projeto (obrigatório — garante que src/ está no path)
streamlit run app.py
```

Acesse `http://localhost:8501` no navegador.

### Indexando os materiais de estudo

Coloque os PDFs em `data/raw/` e faça o upload pela interface (aba **Materiais RAG**), ou rode o indexador diretamente:

```bash
python src/rag/indexer.py
```

---

## Executando os Testes

```bash
# Todos os testes
pytest tests/ -v

# Só storage
pytest tests/test_storage.py -v

# Só RAG/chunker
pytest tests/test_rag.py -v
```

Os testes de storage usam um banco separado (`data/test_jarvis.db`) para não contaminar os dados reais.

---

## Dataset

Os documentos do dataset ficam em `data/raw/`. A documentação completa do dataset (origem, tipo, limitações e estratégia de chunking) está em [`data/DATASET.md`](data/DATASET.md).

### Estratégia de Chunking

O chunker em `src/rag/chunker.py` usa uma estratégia híbrida própria:

1. **Divisão por parágrafo** — separa o Markdown por `\n\n`
2. **Agrupamento de curtos** — parágrafos < 150 caracteres são agrupados com o próximo (preserva informações pontuais como "Frequência mínima: 75%")
3. **Janela deslizante** — parágrafos > 1500 caracteres são quebrados com janela de 1000 chars e overlap de 150

| Parâmetro | Valor |
|---|---|
| Mínimo por chunk | 150 caracteres |
| Máximo por parágrafo | 1500 caracteres |
| Tamanho da janela | 1000 caracteres |
| Overlap | 150 caracteres |
| Modelo de embedding | `paraphrase-multilingual-MiniLM-L12-v2` |

### Busca RAG

A busca é híbrida com três modos selecionáveis:

| Modo | Como funciona | Melhor para |
|---|---|---|
| `hibrido` (padrão) | 60% semântico + 40% BM25 | Maioria dos casos |
| `semantico` | Cosseno via FAISS | Perguntas com paráfrases |
| `bm25` | BM25Okapi | Termos técnicos exatos |

---

## Decisões Técnicas

**Por que prompt engineering em vez de tool calling nativo?**

A passagem do parâmetro `tools=` retorna erro 400.

A solução adotada foi descrever as ferramentas no system prompt e instruir o modelo a responder com JSON estruturado (`{"tool": "nome", "args": {...}}`). O agente detecta e executa esse JSON, injetando o resultado de volta no contexto. Essa técnica é conhecida como **ReAct prompting** (Yao et al., 2022) e é academicamente reconhecida como alternativa ao tool calling nativo.

A geração dinâmica do system prompt (`_construir_tools_prompt()` em `agent.py`) garante que novas ferramentas adicionadas em `src/tools/` aparecem automaticamente no prompt sem alteração do agente.

---

## IAs Utilizadas

| IA | Uso |
|---|---|
| **Claude (Anthropic)** | Desenvolvimento da interface Streamlit, arquitetura das tools, revisão de código, debugging |
| **Gemma 3 12B (Google)** | LLM principal do sistema em produção |
