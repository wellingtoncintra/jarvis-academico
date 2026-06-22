# Documentação do Dataset

## Visão Geral

O dataset do JARVIS Acadêmico foi construído pelo grupo com materiais acadêmicos de Linguagens Formais, Autômatos e Gramáticas. Os arquivos ficam em `data/raw/` e os textos convertidos ficam em `data/processed/`.

| # | Arquivo | Origem dos dados | Tipo de conteúdo | Limitações |
|---|---|---|---|---|
| 1 | `AFD.pdf` | Acervo local do grupo para estudo de Linguagens Formais e Autômatos | Apostila/aula sobre autômatos finitos determinísticos | Conversão pode quebrar acentos, fórmulas e diagramas |
| 2 | `afnd.pdf` | Acervo local do grupo para estudo de Linguagens Formais e Autômatos | Apostila/aula sobre autômatos finitos não determinísticos | Diagramas viram marcadores de imagem no Markdown |
| 3 | `GramaticasLineares.pdf` | Acervo local do grupo para estudo de Linguagens Formais e Autômatos | Material sobre gramáticas lineares e linguagens regulares | Algumas notações matemáticas podem ser simplificadas na conversão |
| 4 | `GramaticasLivresDeContexto.pdf` | Acervo local do grupo para estudo de Linguagens Formais e Autômatos | Material sobre gramáticas livres de contexto | Fórmulas longas podem aparecer como `formula-not-decoded` |
| 5 | `LF-7-25.pdf` | Acervo local do grupo para estudo de Linguagens Formais | Capítulo/trecho de livro ou apostila sobre linguagens formais | Texto extraído de páginas selecionadas, não do livro completo |
| 6 | `LF-27-39.pdf` | Acervo local do grupo para estudo de Linguagens Formais | Capítulo/trecho sobre linguagens não regulares e bombeamento | Numeração e referências internas podem ficar incompletas |
| 7 | `LF-41-79.pdf` | Acervo local do grupo para estudo de Linguagens Formais | Capítulo/trecho com exercícios e construções formais | Muitas tabelas e exercícios podem gerar chunks menos explicativos |
| 8 | `LF-81-108.pdf` | Acervo local do grupo para estudo de Linguagens Formais | Capítulo/trecho sobre gramáticas, árvores e LLC | Pode recuperar assunto de LLC quando a pergunta menciona bombeamento |
| 9 | `LF-109-143.pdf` | Acervo local do grupo para estudo de Linguagens Formais | Capítulo/trecho sobre autômatos de pilha e LLC | Símbolos de pilha e epsilon podem ficar ruidosos |
| 10 | `LFA_preliminares_livro.pdf` | Acervo local do grupo para estudo de Linguagens Formais e Autômatos | Material preliminar/conceitual de LFA | Serve mais como apoio geral do que como fonte específica |

## Quantidade de chunks gerados

Os índices atuais em `data/processed/chunks.pkl` possuem 963 chunks.

| Fonte | Chunks |
|---|---:|
| `AFD` | 76 |
| `afnd` | 23 |
| `GramaticasLineares` | 21 |
| `GramaticasLivresDeContexto` | 102 |
| `LF-7-25` | 107 |
| `LF-27-39` | 85 |
| `LF-41-79` | 174 |
| `LF-81-108` | 130 |
| `LF-109-143` | 195 |
| `LFA_preliminares_livro` | 50 |

## Estratégia de Chunking

O projeto não usa LangChain para chunking. A estratégia real esta em `src/rag/chunker.py` e combina parágrafos naturais com janela deslizante.

- Divisão inicial: separação por parágrafos do Markdown (`\n\n`)
- Agrupamento mínimo: parágrafos curtos são agrupados até pelo menos 150 caracteres
- Tamanho maximo direto: parágrafos com menos de 1500 caracteres viram um chunk
- Fallback para parágrafos longos: janela de 1000 caracteres com overlap de 150 caracteres
- Metadados por chunk: `id`, `texto`, `fonte` e `arquivo`

## Por que essa estratégia?

A divisao por parágrafos preserva melhor a organização do material didático. Isso é importante porque muitos conceitos aparecem em blocos curtos, como definições, listas de componentes e observações. Se o sistema descartasse parágrafos pequenos, poderia perder informações essenciais.

Quando um parágrafo é grande demais, a janela deslizante evita enviar blocos enormes ao embedding e mantém sobreposição suficiente para não cortar explicações no meio.

## Impacto no RAG

- Chunks muito pequenos tendem a recuperar definições precisas, mas podem perder contexto.
- Chunks muito grandes preservam contexto, mas podem misturar assuntos diferentes e reduzir a precisão da busca.
- A estratégia atual tenta equilibrar os dois extremos: usa parágrafos quando eles já são bons blocos semânticos e usa janela apenas como fallback.

## Limitações gerais

- Alguns PDFs contem fórmulas, tabelas e imagens que não são perfeitamente convertidas para Markdown.
- Termos matemáticos podem aparecer com ruído, por exemplo `glyph[epsilon1]` ou `formula-not-decoded`.
- O dataset é concentrado em Linguagens Formais e Autômatos; portanto, perguntas fora desse domínio podem não ter contexto suficiente.
- A qualidade da resposta depende da recuperação: se os chunks recuperados forem indiretos, a LLM pode responder parcialmente ou complementar com conhecimento próprio.