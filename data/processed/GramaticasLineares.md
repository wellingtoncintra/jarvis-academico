## Gramáticas e gramáticas Lineares

## Gramáticas

Uma gramática é uma quádrupla ordenada G = ( V, Σ , P , S ), onde V é um conjunto finito cujos elementos são chamados variáveis ; Σ é um conjunto finito disjunto de V chamado alfabeto cujos elementos são ditos símbolos terminais ; P é um conjunto de pares α → β com α ∈ ( V ∪ Σ) + e β ∈ ( V ∪ Σ) ∗ cujos elementos são chamados de regras de produção ; e S ∈ V é um elemento chamado variável inicial .

Um conjunto de regras de produção { α → β 1 , α → β 2 , . . . , α → β n } ⊆ P pode ser abreviado como uma única produção na forma

Uma gramática que faça sentido deve ter pelo menos uma regra onde do lado esquerdo existe somente a variável inicial. Então, se o conjunto de variáveis ou dos elementos do alfabeto são conhecidos, podemos escrever uma gramática simplesmente escrevendo uma sequência de suas regras de produção

onde α 1 é a variável inicial.

Sejam α ∈ ( V ∪ Σ) + e β ∈ ( V ∪ Σ) ∗ . A expressão α G ⇒ β , ou simplesmente α ⇒ β se G está claro no contexto, indica que existem γ 1 , γ 2 , γ 3 ∈ ( V ∪ Σ) ∗ , X ∈ ( V ∪ Σ) +

e X → γ 2 ∈ P tais que α = γ 1 Xγ 2 e β = γ 1 γ 2 γ 3 . Dizemos que α ⇒ β é uma derivação de α em β em 1 passo de G .

Sejam n ∈ N , α ∈ ( V ∪ Σ) + e β ∈ ( V ∪ Σ) ∗ . A expressão α G,n ⇒ β , ou simplesmente α n ⇒ β se G está claro no contexto, indica que α = β quando n = 0, ou que existe ρ ∈ ( V ∪ Σ) + tal que α ⇒ ρ e ρ n -1 ⇒ β quando n &gt; 0. Dizemos que α n ⇒ β é uma derivação de α em β em n passos de G . Escrevemos α ∗ ⇒ β e diremos que α deriva em β se α n ⇒ β para algum n ∈ N .

A linguagem gerada pela gramática G , denotada por L ( G ) é o conjunto de todas as cadeias x ∈ Σ ∗ que são deriváveis da variável a partir da variável inicial. Em outras palavras, se G = ( V, Σ , P , S ), então

A gramática G serve portanto para representar a linguagem L ( G ). Esse formalismo é dito ser gerador ou axiomático gerando as cadeias que a linguagem possui.

Duas gramáticas G 1 e G 2 são ditas equivalentes se L ( G 1 ) = L ( G 2 ).

## Gramáticas Lineares

Seja G = ( V, Σ , P , S ) uma gramática. Na definições que se seguem A, B representam variáveis em V e w representa uma cadeia em Σ ∗ . Dizemos que G é uma Gramática Linear à Direita - GLD se todas as regras de produção são da forma A → wB ou A → w ; G é uma Gramática Linear à Esquerda - GLE se todas as regras de produção são da forma A → Bw ou A → w ; G é uma Gramática Linear Unitária à Direita - GLUD se G é GLD e em cada regra da G , | w | ≤ 1; G é uma Gramática Linear Unitária à Esquerda - GLUE se G é GLE e em cada regra da G , | w | ≤ 1.

Uma gramática regular é qualquer Gramática Linear. A seguir mostramos uma série de resultados mostrando que uma linguagem gerada por uma gramática regular é regular e pode ser gerada por qualquer outra gramática regular.

Lema 1. Seja A uma linguagem. Existe uma GLUD que gera A se e somente se existe uma GLD que gera A .

Prova . Suponha que existe uma GLUD G tal que L ( G ) = A . Como toda GLUD também é uma GLD, temos que G é uma GLD que gera A .

Suponha agora que existe uma GLD G tal que L ( G ) = A . Obtenha uma gramática G ′ equivalente a G substituindo cada regra X → wY com | w | = n &gt; 1 pelas n novas regras

onde cada Z i é uma variável nova não pertencendo ao conjunto de variáveis de G . Também, cada regra X → w com | w | = n &gt; 1 pelas n novas regras

Claramente, G ′ é uma GLUD e L ( G ′ ) = L ( G ). Portanto, existe uma GLUD que gera A . □

Usando uma construção similar à prova do Lema 1, obtemos também o seguinte resultado.

Lema 2. Seja A uma linguagem. Existe uma GLUE que gera A se e somente se existe uma GLE que gera A .

Lema 3. Seja A uma linguagem. Existe uma GLUD que gera A se e somente se A é uma linguagem regular.

Prova . Suponha que G = ( V, Σ , P, S ) é uma GLUD que gera a linguagem A . O AFND N = ( V ∪ { f } , Σ , δ, S, { f } ) onde f ̸∈ V e

para todo A ∈ V e a ∈ Σ ε e δ ( f, a ) = ∅ para todo a ∈ Σ ε reconhece A . Como existe um AFND que reconhece L ( G ), temos que A é regular.

Suponha agora que A é uma linguagem regular. Nesse caso, existe um AFD M = ( Q, Σ , δ, q 0 , F ) que reconhece A . Construímos a gramática G = ( Q, Σ , P, q 0 ), onde, para cada δ ( X,a ) = Y , temos uma regra X → aY ∈ P ; e para cada p ∈ F , temos p → ε ∈ P . Note que L ( M ) = L ( G ). Logo, a gramática G assim construída é uma GLUD e reconhece A . □

Usando uma prova similar (mas com alguns detalhes adicionais) ao Lema 3 obtemos o seguinte resultado.

Lema 4. Seja A uma linguagem. Existe uma GLUE que gera A se e somente se A é uma linguagem regular.

Usando os Lemas 1, 2, 3 e 4, obtemos o seguinte resultado.

Teorema 1. Uma gramática G é regular se e somente se L ( G ) é regular.

## Exercícios

- 1. Descreva gramáticas lineares para cada uma das linguagens abaixo considerando o alfabeto Σ = { 0 , 1 } .
- (a) { x : x tem no máximo um par de 0's como subcadeia e no máximo um par de 1's como subcadeia } .
- (b) { x : qualquer par de 0's antecede qualquer par de 1's } .
- (c) x : x não possui 010 como subcadeia } .
- 2. Descreva uma GLD que gera a linguagem A = { x ∈ { 0 , 1 } ∗ : 0010 é subcadeia de x } .
- 3. Do item anterior, descreva um AFND que reconhece A usando a construção nos Lemas 2.
- 4. A partir do AFN D do item anterior, obtenha um AFD que reconhece A .
- 5. Minimize o AFD obtido no item anterior.

- 6. Descreva uma GLUE que gera uma linguagem A a partir de uma GLE que gera A .
- 7. Descreva uma GLUE que gera uma linguagem A a partir de um AFD que reconhece A .
- 8. Descreva um AFND que reconhece uma linguagem A a partir de uma GLUE que gera A .

## Referências Bibliográficas