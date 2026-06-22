# Avaliação do Sistema e Análise de Erros - JARVIS Acadêmico

## Contexto da avaliação

Avaliação manual reproduzida sobre 892 chunks limpos. A recuperação usa o mesmo método híbrido da produção (60% semântico e 40% BM25), com expansão para 6 chunks em perguntas comparativas.

- Data: 2026-06-21
- Método: `hibrido`
- Alpha: `0.6`
- K base: `3`
- K comparativo: `6`
- Arquivo estruturado: `data/evaluation/avaliacao_rag.json`
- Regeneração: `python src/evaluation/gerar_recuperacao.py --atualizar-avaliacao`
- Validação: `python src/evaluation/validar_avaliacao.py`

## Resultado geral

| Classificação | Quantidade |
|---|---:|
| Correta | 7 |
| Parcialmente correta | 3 |
| Incorreta | 0 |

## Perguntas avaliadas

### Q01 - O que é um autômato finito determinístico e quais são seus componentes?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `afnd_chunk_0000` | `afnd` | 0.972679 | `hibrido` |
| `LF-41-79_chunk_0000` | `LF-41-79` | 0.934137 | `hibrido` |
| `LF-27-39_chunk_0081` | `LF-27-39` | 0.931152 | `hibrido` |

**Resposta:** Um AFD é uma máquina abstrata determinística para reconhecer linguagens. Formalmente, é definido por uma quíntupla formada pelo conjunto de estados Q, alfabeto Σ, função de transição δ, estado inicial q0 e conjunto de estados finais F.

**Classificação:** parcialmente correta.

**Justificativa:** A resposta está correta, mas os chunks recuperados apresentam uma introdução e exercícios sobre AFD; eles não listam diretamente todos os componentes da quíntupla.

### Q02 - Como um AFD aceita ou rejeita uma palavra?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `AFD_chunk_0012` | `AFD` | 0.921511 | `hibrido` |
| `LF-109-143_chunk_0100` | `LF-109-143` | 0.807064 | `hibrido` |
| `AFD_chunk_0002` | `AFD` | 0.797712 | `hibrido` |

**Resposta:** O AFD processa a palavra a partir do estado inicial, aplicando a função de transição a cada símbolo. Ao final, se o estado alcançado pertence a F, a palavra é aceita; caso contrário, é rejeitada.

**Classificação:** correta.

**Justificativa:** O chunk AFD_chunk_0002 contém diretamente as regras de aceitação e rejeição.

### Q03 - O que diferencia um AFND de um AFD?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `afnd_chunk_0010` | `afnd` | 0.996319 | `hibrido` |
| `afnd_chunk_0008` | `afnd` | 0.904225 | `hibrido` |
| `afnd_chunk_0012` | `afnd` | 0.845611 | `hibrido` |
| `afnd_chunk_0019` | `afnd` | 0.730958 | `hibrido` |
| `afnd_chunk_0000` | `afnd` | 0.725567 | `hibrido` |
| `afnd_chunk_0013` | `afnd` | 0.719139 | `hibrido` |

**Resposta:** O AFD é determinístico: para cada estado e símbolo existe uma única próxima transição. O AFND pode ter zero, uma ou várias transições possíveis, inclusive transições vazias. Apesar dessa diferença operacional, ambos reconhecem a classe das linguagens regulares.

**Classificação:** correta.

**Justificativa:** A expansão comparativa recuperou seis chunks. O chunk afnd_chunk_0008 contrasta as funções de transição, o chunk 0000 define os dois comportamentos e os chunks 0010 e 0012 sustentam a equivalência.

### Q04 - O que são transições vazias em AFND?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `afnd_chunk_0010` | `afnd` | 0.812217 | `hibrido` |
| `afnd_chunk_0011` | `afnd` | 0.777421 | `hibrido` |
| `afnd_chunk_0001` | `afnd` | 0.773384 | `hibrido` |

**Resposta:** Transições vazias, ou transições ε, são movimentos que o AFND pode realizar sem consumir um símbolo da entrada. Elas permitem mudar de estado e explorar outras possibilidades de computação.

**Classificação:** correta.

**Justificativa:** Os chunks afnd_chunk_0001 e 0011 explicam diretamente as transições ε e os estados alcançáveis sem consumir símbolos da entrada.

### Q05 - O que são gramáticas lineares?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `LF-41-79_chunk_0094` | `LF-41-79` | 0.938209 | `hibrido` |
| `LF-41-79_chunk_0098` | `LF-41-79` | 0.881573 | `hibrido` |
| `LF-81-108_chunk_0071` | `LF-81-108` | 0.878314 | `hibrido` |

**Resposta:** Gramáticas lineares são gramáticas cujas regras têm, no máximo, uma variável no lado direito. Conforme a posição dessa variável, a gramática pode ser linear à direita ou linear à esquerda.

**Classificação:** parcialmente correta.

**Justificativa:** Os chunks recuperados introduzem gramáticas lineares à direita e sua relação com linguagens regulares, mas não apresentam diretamente a definição formal completa.

### Q06 - O que é uma gramática livre de contexto?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `LF-109-143_chunk_0102` | `LF-109-143` | 0.988684 | `hibrido` |
| `GramaticasLivresDeContexto_chunk_0000` | `GramaticasLivresDeContexto` | 0.956912 | `hibrido` |
| `LF-41-79_chunk_0122` | `LF-41-79` | 0.914502 | `hibrido` |

**Resposta:** Uma GLC é uma gramática G = (V, Σ, P, S) em que cada produção possui uma única variável no lado esquerdo e uma cadeia de variáveis e/ou terminais no lado direito. Uma linguagem é livre de contexto quando pode ser gerada por alguma GLC.

**Classificação:** correta.

**Justificativa:** O chunk GramaticasLivresDeContexto_chunk_0000 contém a definição formal; os outros chunks reforçam a característica das regras e a relação com a linguagem gerada.

### Q07 - Qual é a ideia da Forma Normal de Chomsky?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `GramaticasLivresDeContexto_chunk_0042` | `GramaticasLivresDeContexto` | 1.000000 | `hibrido` |
| `GramaticasLivresDeContexto_chunk_0041` | `GramaticasLivresDeContexto` | 0.814236 | `hibrido` |
| `GramaticasLivresDeContexto_chunk_0055` | `GramaticasLivresDeContexto` | 0.578063 | `hibrido` |

**Resposta:** A Forma Normal de Chomsky padroniza uma GLC para que suas produções tenham dois formatos principais: A → BC ou A → a. Também pode ser permitida a regra S → ε.

**Classificação:** correta.

**Justificativa:** O chunk GramaticasLivresDeContexto_chunk_0042 contém exatamente a definição solicitada.

### Q08 - Como expressões regulares se relacionam com linguagens regulares?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `LF-7-25_chunk_0059` | `LF-7-25` | 0.966544 | `hibrido` |
| `AFD_chunk_0026` | `AFD` | 0.834568 | `hibrido` |
| `LF-7-25_chunk_0056` | `LF-7-25` | 0.832048 | `hibrido` |

**Resposta:** Expressões regulares descrevem linguagens regulares por meio de operações como união, concatenação e estrela. Expressões diferentes podem denotar a mesma linguagem, e essas operações preservam a regularidade.

**Classificação:** correta.

**Justificativa:** Os chunks LF-7-25_chunk_0056 e 0059 definem expressões regulares e sua denotação, enquanto AFD_chunk_0026 sustenta o fechamento das linguagens regulares.

### Q09 - O que a propriedade do bombeamento permite provar sobre linguagens regulares?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `LF-27-39_chunk_0000` | `LF-27-39` | 0.965006 | `hibrido` |
| `LF-81-108_chunk_0082` | `LF-81-108` | 0.961974 | `hibrido` |
| `LF-81-108_chunk_0091` | `LF-81-108` | 0.930454 | `hibrido` |

**Resposta:** A propriedade do bombeamento é uma condição necessária das linguagens regulares. Para provar que uma linguagem não é regular, pode-se mostrar por contradição que ela não satisfaz essa propriedade.

**Classificação:** correta.

**Justificativa:** O chunk LF-27-39_chunk_0000 explica diretamente a estratégia de usar a propriedade do bombeamento para demonstrar que uma linguagem não é regular.

### Q10 - Como construir um AFND a partir de uma gramática linear à direita?

**Chunks recuperados:**

| Chunk | Fonte | Score | Método |
|---|---|---:|---|
| `LF-41-79_chunk_0101` | `LF-41-79` | 0.924869 | `hibrido` |
| `LF-109-143_chunk_0103` | `LF-109-143` | 0.923362 | `hibrido` |
| `LF-81-108_chunk_0078` | `LF-81-108` | 0.914802 | `hibrido` |

**Resposta:** A construção trata as variáveis da gramática como estados do autômato. Uma regra A → aB origina uma transição de A para B lendo a; uma regra A → a leva a um estado final, e o símbolo inicial da gramática torna-se o estado inicial.

**Classificação:** parcialmente correta.

**Justificativa:** Os chunks indicam que o autômato simula derivações da gramática e confirmam a relação entre os formalismos, mas não apresentam todas as etapas específicas descritas na resposta.

## Análise de erros

### E01 - Recuperação

**Falha:** A pergunta Q01 não recuperou diretamente o chunk que enumera todos os componentes formais de um AFD.

**Causa:** Os termos gerais da pergunta aparecem em capítulos e exercícios sobre autômatos, que obtiveram scores híbridos maiores que a definição formal.

**Possível solução:** Adicionar expansão por subperguntas definicionais, como 'definição formal de AFD' e 'quíntupla do AFD', ou usar metadados de seção no ranking.

### E02 - Ambiguidade de domínio

**Falha:** Perguntas sobre bombeamento de linguagens regulares também recuperam trechos sobre bombeamento de linguagens livres de contexto.

**Causa:** Os dois assuntos compartilham quase todo o vocabulário, e alguns materiais explicam um caso fazendo referência explícita ao outro.

**Possível solução:** Adicionar o tipo de linguagem como metadado do chunk e penalizar documentos de outro domínio durante o ranking.

### E03 - Geração

**Falha:** Na Q10, a resposta descreve detalhes da construção do AFND que não aparecem integralmente nos chunks recuperados.

**Causa:** A LLM completa uma evidência indireta com conhecimento paramétrico correto, mas não totalmente rastreável ao contexto fornecido.

**Possível solução:** Exigir citações por afirmação, avisar quando a evidência for indireta e buscar mais chunks da mesma seção antes de gerar a resposta.

## Melhorias verificadas

- O corpus foi normalizado e reindexado sem tokens glyph[ ou formula-not-decoded.
- A pergunta comparativa Q03 passou a recuperar seis chunks e agora inclui o contraste direto entre AFD e AFND.
- O reranking foi medido separadamente e permaneceu opcional porque piorou perguntas com domínios próximos, como bombeamento de linguagens regulares e livres de contexto.

A comparação experimental do cross-encoder está em `data/evaluation/COMPARACAO_RERANKING.md`.
