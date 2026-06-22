# Avaliação do Sistema e Análise de Erros - JARVIS Acadêmico

## Contexto da avaliação

Esta avaliação cobre o requisíto obrigatório de avaliar o sistema com pelo menos 10 perguntas. Para cada pergunta foram registrados: pergunta, chunks recuperados, resposta gerada/esperada pelo JARVIS e classificação manual.

- Data: 2026-06-14
- Base avaliada: documentos em `data/raw/` e chunks persistidos em `data/processed/chunks.pkl`
- Método registrado: `bm25`
- Número de chunks por pergunta: `k=3`
- Arquivo estruturado: `data/evaluation/avaliacao_rag.json`

## Resultado geral

| Classificação | Quantidade |
|---|---:|
| Correta | 7 |
| Parcialmente correta | 3 |
| Incorreta | 0 |

O desempenho geral foi bom para perguntas definicionais, principalmente quando o termo aparece explicitamente no material. As respostas parciais ocorreram em perguntas que exigiam comparação, equivalência entre formalismos ou construção de algoritmos, pois a recuperação trouxe evidências indiretas.

## Perguntas avaliadas

### Q01 - O que é um autômato finito determinístico e quais são seus componentes?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `afnd_chunk_0000` | `afnd` | 17.554 |
| `AFD_chunk_0000` | `AFD` | 16.508 |
| `AFD_chunk_0001` | `AFD` | 14.628 |

**Resposta:** Um AFD e uma maquina abstrata deterministica para reconhecer linguagens. Formalmente, e definido por uma quintupla formada por conjunto finito de estados Q, alfabeto Sigma, funcao de transicao delta, estado inicial q0 e conjunto de estados finais F.

**Classificação:** correta.

### Q02 - Como um AFD aceita ou rejeita uma palavra?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `AFD_chunk_0003` | `AFD` | 14.033 |
| `AFD_chunk_0014` | `AFD` | 12.900 |
| `afnd_chunk_0008` | `afnd` | 9.943 |

**Resposta:** O AFD processa a palavra a partir do estado inicial, aplicando a funcao de transicao para cada simbolo. Ao final, se o estado alcancado esta em F, a palavra e aceita; caso contrario, e rejeitada.

**Classificação:** correta.

### Q03 - O que diferencia um AFND de um AFD?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `afnd_chunk_0011` | `afnd` | 17.654 |
| `afnd_chunk_0013` | `afnd` | 17.487 |
| `afnd_chunk_0021` | `afnd` | 14.685 |

**Resposta:** AFD e deterministico: para cada estado e simbolo ha uma unica proxima escolha. AFND permite zero, uma ou varias transicoes possiveis, inclusive transicoes vazias em alguns modelos. Apesar dessa diferenca operacional, AFD e AFND reconhecem a mesma classe de linguagens regulares.

**Classificação:** parcialmente correta.

**Motivo:** A resposta esta boa, mas os chunks recuperados privilegiaram equivalência entre AFD e AFND, não a definição operacional direta do AFND.

### Q04 - O que são transições vazias em AFND?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `afnd_chunk_0011` | `afnd` | 13.540 |
| `afnd_chunk_0012` | `afnd` | 11.460 |
| `afnd_chunk_0001` | `afnd` | 10.930 |

**Resposta:** Transicoes vazias, ou epsilon-transicoes, sao movimentos que o AFND pode fazer sem consumir simbolo da entrada. Elas permitem mudar de estado espontaneamente e ajudam a modelar varias possibilidades de computacao.

**Classificação:** correta.

### Q05 - O que são gramáticas lineares?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `GramaticasLineares_chunk_0000` | `GramaticasLineares` | 11.015 |
| `GramaticasLineares_chunk_0007` | `GramaticasLineares` | 10.874 |
| `LF-41-79_chunk_0100` | `LF-41-79` | 9.555 |

**Resposta:** Gramaticas lineares sao gramaticas em que as producoes restringem a quantidade e a posicao de variaveis no lado direito. Nas variantes mais comuns, a variavel pode aparecer no fim da producao, formando uma gramatica linear a direita, ou no inicio, formando uma gramatica linear a esquerda.

**Classificação:** correta.

### Q06 - O que é uma gramática livre de contexto?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `GramaticasLivresDeContexto_chunk_0000` | `GramaticasLivresDeContexto` | 19.388 |
| `GramaticasLivresDeContexto_chunk_0001` | `GramaticasLivresDeContexto` | 16.840 |
| `GramaticasLivresDeContexto_chunk_0095` | `GramaticasLivresDeContexto` | 16.423 |

**Resposta:** Uma GLC e uma gramatica G = (V, Sigma, P, S) em que cada producao tem uma unica variavel no lado esquerdo e uma cadeia de variaveis e/ou terminais no lado direito. Uma linguagem e livre de contexto quando pode ser gerada por alguma GLC.

**Classificação:** correta.

### Q07 - Qual é a ideia da Forma Normal de Chomsky?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `GramaticasLivresDeContexto_chunk_0052` | `GramaticasLivresDeContexto` | 25.727 |
| `GramaticasLivresDeContexto_chunk_0051` | `GramaticasLivresDeContexto` | 23.337 |
| `GramaticasLivresDeContexto_chunk_0068` | `GramaticasLivresDeContexto` | 16.142 |

**Resposta:** A Forma Normal de Chomsky padroniza uma GLC para que suas producoes tenham apenas dois formatos principais: uma variavel gerando duas variaveis, A -> BC, ou uma variavel gerando um terminal, A -> a. Em alguns casos tambem se permite S -> epsilon.

**Classificação:** correta.

### Q08 - Como expressões regulares se relacionam com linguagens regulares?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `AFD_chunk_0029` | `AFD` | 13.673 |
| `LF-27-39_chunk_0001` | `LF-27-39` | 11.657 |
| `LF-7-25_chunk_0080` | `LF-7-25` | 11.639 |

**Resposta:** Expressoes regulares descrevem linguagens regulares usando operacoes como uniao, concatenacao e estrela. Como essas operacoes preservam regularidade, elas servem como uma forma declarativa de especificar linguagens que tambem podem ser reconhecidas por automatos finitos.

**Classificação:** parcialmente correta.

**Motivo:** A resposta está correta em teoria, mas os chunks recuperados dão evidência indireta. Não apareceu um trecho direto provando equivalência entre expressões regulares e autômatos finitos.

### Q09 - O que a propriedade do bombeamento permite provar sobre linguagens regulares?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `LF-27-39_chunk_0001` | `LF-27-39` | 23.740 |
| `LF-81-108_chunk_0082` | `LF-81-108` | 23.450 |
| `LF-27-39_chunk_0000` | `LF-27-39` | 21.460 |

**Resposta:** A propriedade do bombeamento e usada como criterio necessario: toda linguagem regular deve satisfaze-la. Assim, para provar que uma linguagem nao e regular, busca-se uma contradicao mostrando que nenhuma decomposicao adequada permite bombear a palavra mantendo-a na linguagem.

**Classificação:** correta.

### Q10 - Como construir um AFND a partir de uma gramática linear à direita?

**Chunks recuperados:**

| Chunk | Fonte | Score |
|---|---|---:|
| `LF-41-79_chunk_0109` | `LF-41-79` | 19.370 |
| `GramaticasLineares_chunk_0007` | `GramaticasLineares` | 19.350 |
| `GramaticasLineares_chunk_0019` | `GramaticasLineares` | 17.180 |

**Resposta:** A ideia e tratar variaveis da gramatica como estados do automato. Para uma regra do tipo A -> aB, cria-se uma transicao de A para B lendo a; para uma regra A -> a, cria-se uma transicao para um estado final novo lendo a. O simbolo inicial vira o estado inicial.

**Classificação:** parcialmente correta.

**Motivo:** A resposta descreve o algoritmo esperado, mas os chunks recuperados contem mais definições e exercícios do que a construção formal completa.

## Análise de erros

### Falha 1 - Recuperação em perguntas comparativas

**Tipo:** recuperação.

**Causa:** perguntas comparativas sobre AFD e AFND recuperaram trechos sobre equivalência, porque os termos AFD/AFND aparecem muitas vezes nesses trechos e o BM25 valoriza coincidência lexical.

**Possível solução:** usar busca híbrida como padrão, aumentar `k` para 5 em perguntas comparativas e aplicar reranking semântico para priorizar trechos definicionais.

### Falha 2 - Ruído da conversão PDF para Markdown

**Tipo:** pré-processamento/OCR.

**Causa:** alguns PDFs foram convertidos com acentos quebrados, símbolos como `glyph[epsilon1]` e marcadores como `formula-not-decoded`. Isso dificulta a recuperação quando a pergunta usa a notação matemática correta.

**Possível solução:** adicionar limpeza pós-conversão para normalizar símbolos frequentes, substituir `glyph[epsilon1]` por `epsilon`, revisar manualmente documentos centrais e preservar melhor fórmulas importantes.

### Falha 3 - Resposta correta com evidência fraca

**Tipo:** geração.

**Causa:** a LLM pode completar lacunas com conhecimento próprio quando os chunks recuperados são indiretos. Isso aparece nas perguntas sobre expressões regulares e construção de AFND a partir de gramáticas.

**Possível solução:** exibir fontes e scores na resposta, exigir que a resposta cite quais chunks sustentam cada afirmação e mostrar aviso quando os scores forem baixos ou a evidência for indireta.