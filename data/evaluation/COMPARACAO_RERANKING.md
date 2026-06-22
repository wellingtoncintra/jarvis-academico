# Comparação do Reranking

## Configuração

- Corpus limpo: 892 chunks
- Linha de base: busca híbrida, `alpha=0.6`
- Candidatos do reranker: top 10 da busca híbrida
- Cross-encoder: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`
- Saídas: `recuperacao_hibrida.json` e `recuperacao_rerank.json`

## Resultado manual

| Pergunta | Híbrido | Híbrido + reranking | Observação |
|---|---|---|---|
| Q01 | Parcial | Parcial | Nenhum método priorizou a lista formal dos componentes do AFD |
| Q02 | Correta | Correta | O reranker colocou a regra formal de aceitação em primeiro lugar |
| Q03 | Correta | Correta | A expansão comparativa trouxe definição, diferença e equivalência |
| Q04 | Correta | Correta | Ambos recuperaram a definição de transição ε após a limpeza dos acentos |
| Q05 | Parcial | Correta | O reranker encontrou a definição de gramática linear |
| Q06 | Correta | Correta | Ambos recuperaram a característica de uma GLC |
| Q07 | Correta | Correta | A definição da Forma Normal de Chomsky ficou em primeiro lugar |
| Q08 | Correta | Correta | Ambos recuperaram definição e exemplos de expressões regulares |
| Q09 | Correta | Parcial | O reranker priorizou bombeamento de linguagens livres de contexto |
| Q10 | Parcial | Parcial | Há relação entre os formalismos, mas faltam regras completas da construção |

| Método | Corretas | Parciais | Incorretas |
|---|---:|---:|---:|
| Híbrido | 7 | 3 | 0 |
| Híbrido + reranking | 7 | 3 | 0 |

## Decisão

O reranking foi mantido como recurso opcional (`rerank=True`), mas não foi ativado por padrão. Neste dataset, ele melhorou Q02 e Q05, mas piorou Q09 ao priorizar bombeamento de linguagens livres de contexto. O resultado agregado empatou com o híbrido, enquanto adicionou custo de memória, latência e carregamento de modelo. A produção e a avaliação oficial continuam usando busca híbrida, e o experimento permanece reproduzível para demonstrar que a decisão foi baseada em medição.

## Reprodução

```bash
python src/evaluation/gerar_recuperacao.py --saida data/evaluation/recuperacao_hibrida.json
python src/evaluation/gerar_recuperacao.py --rerank --saida data/evaluation/recuperacao_rerank.json
```
