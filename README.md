# Estudantes
Wellington Cintra e Cézar Dias

# Video de Apresentação
Trabalho 1 - Link do Drive: https://drive.google.com/file/d/1aMq6JRgaV8YomS9Ohz1Z9L5uBFKd2G39/view?usp=sharing
Trabalho 2 - Link do Drive: https://drive.google.com/file/d/12B94gJykUwoOP1OkhBuvnRGkXyBjMA2O/view?usp=drive_link
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
| **Storage** | SQLite | Persistência de agenda, tarefas e desempenho de aprendizado |
| **Logging** | Loguru + JSONL | Log de aplicação e registro estruturado de tool calls |
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
   src/storage/          ← SQLite (agenda, tarefas, desempenho)
   src/rag/              ← FAISS + BM25 (materiais de estudo)

Módulos transversais:
   src/prompts/          ← prompts centralizados por domínio
   src/logging_config.py ← log de aplicação + tool_calls.jsonl
   src/utils.py          ← utilitários compartilhados
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
- Busca híbrida (semântica + lexical) com fusão ponderada de scores
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

### Trabalho 2

**3.4 Planejamento de estudos**
- A tool `planejar_estudos` combina as **três fontes** exigidas: agenda (eventos e provas próximas), tarefas (pendentes e urgentes) e materiais (trechos relevantes via RAG)
- Responde a pedidos como "monte um plano para a prova" ou "o que priorizar hoje?"
- A LLM recebe o contexto consolidado e elabora o plano

**Melhorias de aprendizado (2 funcionalidades, ≥1 interativa)**
- **Active Recall (interativa):** o sistema gera uma pergunta a partir dos materiais indexados, o aluno responde, e o Gemma avalia a resposta classificando-a em correta / parcialmente correta / incorreta. Atende ao requisito de "o sistema pergunta e avalia".
- **Geração de exercícios:** questões de múltipla escolha criadas a partir dos materiais (RAG), com gabarito e explicação por questão.
- **Identificação de dificuldades:** cada tentativa de Active Recall é persistida (tópico + classificação) e o desempenho é agregado por tópico, destacando os assuntos com menor aproveitamento — transformando o feedback efêmero em histórico acionável.

As perguntas e exercícios são **ancorados no RAG**: nascem dos materiais que o aluno indexou, não do conhecimento geral da LLM.

**Avaliação e análise de erros**
- Artefato com 10 perguntas avaliadas (pergunta, chunks recuperados, resposta, classificação e justificativa) em `data/evaluation/avaliacao_rag.json`
- Análise de pelo menos 3 falhas (tipo, causa e possível solução)
- Visualização direta no app pela aba **Avaliação**

**Citações inline**
- As respostas do chat baseadas em materiais exibem um rodapé discreto com as fontes consultadas (📎 Fontes: ...), aumentando a transparência sobre a origem da informação

**Logging persistido**
- Log de aplicação em `logs/jarvis.log` (rotação automática) via Loguru
- Registro estruturado de tool calling em `logs/tool_calls.jsonl` (uma linha por chamada: ferramenta, entrada, saída, status, timestamp), além da visualização em sessão na aba **Logs**

---

## Estrutura do Projeto

```
jarvis-academico/
├── app.py                      # Entry point Streamlit (inicializa logging)
├── .env                        # Credenciais (não versionado)
├── requirements.txt
│
├── interface/                  # Páginas Streamlit
│   ├── chat.py                 # Chat com histórico, tool calls e citações inline
│   ├── agenda.py               # Visualização e cadastro de eventos
│   ├── tarefas.py              # Gerenciamento de tarefas
│   ├── rag.py                  # Upload e indexação de documentos
│   ├── planejamento.py         # Planejamento de estudos
│   ├── aprendizado.py          # Active Recall, exercícios e dificuldades
│   ├── avaliacao.py            # Painel de avaliação e análise de erros
│   └── logs.py                 # Logs de tool calling (sessão)
│
├── src/
│   ├── agent.py                # Orquestrador: loop de tool calling
│   ├── utils.py                # Utilitários (extração robusta de JSON)
│   ├── logging_config.py       # Setup de logging + persistência de tool calls
│   ├── llm/
│   │   └── client.py           # Cliente OpenAI (chat.completions)
│   ├── rag/
│   │   ├── loader.py           # PDF → Markdown (Docling)
│   │   ├── chunker.py          # Estratégia híbrida de chunking
│   │   ├── embedder.py         # FAISS + BM25 + SentenceTransformers
│   │   ├── retriever.py        # Busca e geração de resposta RAG
│   │   ├── paths.py            # Caminhos dos índices + checagem (módulo leve)
│   │   └── indexer.py          # Script de indexação standalone
│   ├── storage/
│   │   ├── database.py         # Conexão SQLite (context manager) + tabelas
│   │   ├── agenda.py           # CRUD de eventos
│   │   ├── tarefas.py          # CRUD de tarefas
│   │   └── desempenho.py       # Persistência do desempenho de Active Recall
│   ├── prompts/                # Prompts centralizados por domínio
│   │   ├── agent.py            # System prompt e diretrizes do agente
│   │   ├── rag.py              # Prompt de geração de resposta RAG
│   │   ├── aprendizado.py      # Prompts de Active Recall e exercícios
│   │   └── planejamento.py     # Prompt de planejamento de estudos
│   ├── evaluation/
│   │   └── gerar_recuperacao.py # Gera a recuperação das perguntas de avaliação
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
│   ├── evaluation/             # Artefato de avaliação (perguntas + recuperação)
│   ├── jarvis.db               # Banco SQLite (não versionado)
│   └── DATASET.md              # Documentação do dataset
│
├── logs/                       # Logs de aplicação e tool calls (não versionado)
│
└── tests/
    ├── test_storage.py         # Testes de CRUD no SQLite
    ├── test_rag.py             # Testes do pipeline de chunking
    ├── test_utils.py           # Testes da extração de JSON
    └── test_desempenho.py      # Testes da persistência de desempenho
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

A suíte cobre o storage (CRUD de agenda e tarefas), o pipeline de chunking do RAG, a extração de JSON e a persistência de desempenho.

```bash
# Todos os testes
pytest tests/ -v

# Por módulo
pytest tests/test_storage.py -v      # CRUD no SQLite
pytest tests/test_rag.py -v          # pipeline de chunking
pytest tests/test_utils.py -v        # extração de JSON
pytest tests/test_desempenho.py -v   # persistência de desempenho
```

Os testes que tocam o banco usam um arquivo SQLite temporário isolado (via `tmp_path` do pytest), definido antes da importação dos módulos de storage, de modo que nunca tocam o `data/jarvis.db` real.

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

**Por que uma única `gerenciar_tarefas` em vez de três ferramentas separadas?**

A especificação cita `adicionar_tarefa`, `listar_tarefas` e `concluir_tarefa` como exemplos de ferramentas. Optamos conscientemente por consolidá-las em uma única ferramenta `gerenciar_tarefas`, parametrizada por um campo `acao` (`adicionar`, `listar_pendentes`, `listar_todas`, `concluir`). A decisão é técnica, não de conveniência:

- **A decisão de chamada é feita por prompt engineering, não por tool calling nativo.** O Gemma 12B escolhe a ferramenta montando um JSON a partir da descrição no system prompt. Quanto menor a quantidade de ferramentas expostas, menor a superfície de ambiguidade e menor a chance de o modelo escolher errado — algo especialmente relevante para um modelo desse porte sem suporte nativo a tools. Agrupar operações de um mesmo domínio (tarefas) em uma ferramenta com sub-ação reduz a carga de decisão do modelo.
- **O loop do agente tem limite de 5 iterações** (`MAX_ITERACOES`). Manter o número de ferramentas enxuto preserva margem nesse orçamento e torna o comportamento mais previsível e testável.
- **O padrão "ferramenta com sub-ação" é legítimo** e amplamente usado em catálogos de ferramentas para LLMs. A lógica de negócio permanece totalmente separada: `gerenciar_tarefas` é uma casca fina sobre as funções de `src/storage/tarefas.py` (`adicionar_tarefa`, `listar_tarefas_pendentes`, `concluir_tarefa`, etc.), que já são distintas e testáveis individualmente.
- **O requisito mínimo de 5 ferramentas é atendido**: `consultar_agenda`, `adicionar_agenda`, `gerenciar_tarefas`, `buscar_material_rag` e `planejar_estudos`.

Em resumo, as três operações de tarefa continuam existindo e sendo decididas pela LLM; apenas são expostas sob uma única ferramenta para maximizar a confiabilidade da escolha pelo modelo.

---

## IAs Utilizadas

| IA | Uso |
|---|---|
| **Claude (Anthropic)** | Desenvolvimento da interface Streamlit, arquitetura das tools, revisão de código, debugging |
| **Gemma 3 12B (Google)** | LLM principal do sistema em produção |
