# 🤖 JARVIS Acadêmico

Assistente pessoal inteligente para estudantes, desenvolvido com RAG, Tool Calling e LLM (Gemma 12B).

---

## 📋 Funcionalidades

- **Consulta a materiais** — faça perguntas sobre PDFs e anotações via RAG
- **Agenda acadêmica** — consulte aulas, provas e eventos por linguagem natural
- **Lista de tarefas** — adicione, liste e conclua tarefas via chat ou interface
- **Planejamento de estudos** — o assistente combina agenda + tarefas + materiais para montar planos
- **Active Recall** — o sistema faz perguntas e avalia suas respostas
- **Geração de exercícios** — cria questões baseadas nos seus materiais

---

## 🗂️ Estrutura do Projeto

```
jarvis-academico/
├── data/
│   ├── raw/              # Documentos originais (PDFs, textos)
│   ├── processed/        # Chunks gerados pelo pipeline RAG
│   └── jarvis.db         # Banco SQLite (agenda + tarefas)
├── src/
│   ├── rag/              # Pipeline RAG (loader, chunker, embedder, retriever)
│   ├── tools/            # Tools para o agente LLM
│   ├── learning/         # Funcionalidades de aprendizado
│   ├── storage/          # Acesso ao banco SQLite
│   └── llm/              # Cliente e configuração do Gemma 12B
├── interface/            # Interface Streamlit
├── evaluation/           # Avaliação do sistema (10 perguntas)
├── tests/                # Testes automatizados
├── logs/                 # Logs de execução e tool calling
├── .env.example          # Modelo de variáveis de ambiente
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/wellingtoncintra/jarvis-academico.git
cd jarvis-academico
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com o token e URL fornecidos pelo professor
```

### 5. Adicione documentos ao dataset

Coloque seus PDFs e textos na pasta `data/raw/`.

---

## 🚀 Execução

### Interface completa (Streamlit)

```bash
streamlit run interface/app.py
```

### Somente via terminal (modo chat)

```bash
python src/agent.py
```

### Indexar novos documentos

```bash
python src/rag/indexer.py
```

---

## 🛠️ Ferramentas do Agente

| Ferramenta | Descrição |
|---|---|
| `consultar_agenda` | Busca eventos por data ou período |
| `adicionar_agenda` | Cadastra aulas, provas ou eventos |
| `listar_tarefas` | Lista tarefas pendentes ou concluídas |
| `adicionar_tarefa` | Cria uma nova tarefa com prazo |
| `concluir_tarefa` | Marca uma tarefa como concluída |
| `buscar_material_rag` | Busca semântica nos documentos indexados |
| `gerar_exercicios` | Gera questões sobre um tópico do material |

---

## 🧪 Testes

```bash
pytest tests/ -v
```

---

## 📊 Avaliação

Os resultados da avaliação do sistema estão em `evaluation/eval.json`, com 10 perguntas classificadas como corretas, parcialmente corretas ou incorretas.

---

## 🤖 IAs utilizadas no desenvolvimento

- **Claude (Anthropic)** — arquitetura, revisão de código e documentação
- **Gemma 12B** — modelo de linguagem principal do assistente

---

## 👥 Integrantes

- Cézar Dias Martins
- Wellington Cintra da Silva