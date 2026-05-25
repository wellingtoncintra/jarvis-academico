## Gram´ aticas e gram´ aticas Lineares

## Gram´ aticas

Uma gram´ atica ´ e uma qu´ adrupla ordenada G = ( V, Σ , P , S ), onde V ´ e um conjunto finito cujos elementos s˜ ao chamados vari´ aveis ; Σ ´ e um conjunto finito disjunto de V chamado alfabeto cujos elementos s˜ ao ditos s´ ımbolos terminais ; P ´ e um conjunto de pares α → β com α ∈ ( V ∪ Σ) + e β ∈ ( V ∪ Σ) ∗ cujos elementos s˜ ao chamados de regras de produ¸ c˜ ao ; e S ∈ V ´ e um elemento chamado vari´ avel inicial .

Um conjunto de regras de produ¸ c˜ ao { α → β 1 , α → β 2 , . . . , α → β n } ⊆ P pode ser abreviado como uma ´ unica produ¸ c˜ ao na forma

<!-- formula-not-decoded -->

Uma gram´ atica que fa¸ ca sentido deve ter pelo menos uma regra onde do lado esquerdo existe somente a vari´ avel inicial. Ent˜ ao, se o conjunto de vari´ aveis ou dos elementos do alfabeto s˜ ao conhecidos, podemos escrever uma gram´ atica simplesmente escrevendo uma sequˆ encia de suas regras de produ¸ c˜ ao

<!-- formula-not-decoded -->

onde α 1 ´ e a vari´ avel inicial.

Sejam α ∈ ( V ∪ Σ) + e β ∈ ( V ∪ Σ) ∗ . A express˜ ao α G ⇒ β , ou simplesmente α ⇒ β se G est´ a claro no contexto, indica que existem γ 1 , γ 2 , γ 3 ∈ ( V ∪ Σ) ∗ , X ∈ ( V ∪ Σ) +

e X → γ 2 ∈ P tais que α = γ 1 Xγ 2 e β = γ 1 γ 2 γ 3 . Dizemos que α ⇒ β ´ e uma deriva¸ c˜ ao de α em β em 1 passo de G .

Sejam n ∈ N , α ∈ ( V ∪ Σ) + e β ∈ ( V ∪ Σ) ∗ . A express˜ ao α G,n ⇒ β , ou simplesmente α n ⇒ β se G est´ a claro no contexto, indica que α = β quando n = 0, ou que existe ρ ∈ ( V ∪ Σ) + tal que α ⇒ ρ e ρ n -1 ⇒ β quando n &gt; 0. Dizemos que α n ⇒ β ´ e uma deriva¸ c˜ ao de α em β em n passos de G . Escrevemos α ∗ ⇒ β e diremos que α deriva em β se α n ⇒ β para algum n ∈ N .

A linguagem gerada pela gram´ atica G , denotada por L ( G ) ´ e o conjunto de todas as cadeias x ∈ Σ ∗ que s˜ ao deriv´ aveis da vari´ avel a partir da vari´ avel inicial. Em outras palavras, se G = ( V, Σ , P , S ), ent˜ ao

<!-- formula-not-decoded -->

A gram´ atica G serve portanto para representar a linguagem L ( G ). Esse formalismo ´ e dito ser gerador ou axiom´ atico gerando as cadeias que a linguagem possui.

Duas gram´ aticas G 1 e G 2 s˜ ao ditas equivalentes se L ( G 1 ) = L ( G 2 ).

## Gram´ aticas Lineares

Seja G = ( V, Σ , P , S ) uma gram´ atica. Na defini¸ c˜ oes que se seguem A, B representam vari´ aveis em V e w representa uma cadeia em Σ ∗ . Dizemos que G ´ e uma Gram´ atica Linear ` a Direita - GLD se todas as regras de produ¸ c˜ ao s˜ ao da forma A → wB ou A → w ; G ´ e uma Gram´ atica Linear ` a Esquerda - GLE se todas as regras de produ¸ c˜ ao s˜ ao da forma A → Bw ou A → w ; G ´ e uma Gram´ atica Linear Unit´ aria ` a Direita - GLUD se G ´ e GLD e em cada regra da G , | w | ≤ 1; G ´ e uma Gram´ atica Linear Unit´ aria ` a Esquerda - GLUE se G ´ e GLE e em cada regra da G , | w | ≤ 1.

Uma gram´ atica regular ´ e qualquer Gram´ atica Linear. A seguir mostramos uma s´ erie de resultados mostrando que uma linguagem gerada por uma gram´ atica regular ´ e regular e pode ser gerada por qualquer outra gram´ atica regular.

Lema 1. Seja A uma linguagem. Existe uma GLUD que gera A se e somente se existe uma GLD que gera A .

Prova . Suponha que existe uma GLUD G tal que L ( G ) = A . Como toda GLUD tamb´ em ´ e uma GLD, temos que G ´ e uma GLD que gera A .

Suponha agora que existe uma GLD G tal que L ( G ) = A . Obtenha uma gram´ atica G ′ equivalente a G substituindo cada regra X → wY com | w | = n &gt; 1 pelas n novas regras

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

onde cada Z i ´ e uma vari´ avel nova n˜ ao pertencendo ao conjunto de vari´ aveis de G . Tamb´ em, cada regra X → w com | w | = n &gt; 1 pelas n novas regras

<!-- formula-not-decoded -->

Claramente, G ′ ´ e uma GLUD e L ( G ′ ) = L ( G ). Portanto, existe uma GLUD que gera A . □

Usando uma constru¸ c˜ ao similar ` a prova do Lema 1, obtemos tamb´ em o seguinte resultado.

Lema 2. Seja A uma linguagem. Existe uma GLUE que gera A se e somente se existe uma GLE que gera A .

Lema 3. Seja A uma linguagem. Existe uma GLUD que gera A se e somente se A ´ e uma linguagem regular.

Prova . Suponha que G = ( V, Σ , P, S ) ´ e uma GLUD que gera a linguagem A . O AFND N = ( V ∪ { f } , Σ , δ, S, { f } ) onde f ̸∈ V e

<!-- formula-not-decoded -->

para todo A ∈ V e a ∈ Σ ε e δ ( f, a ) = ∅ para todo a ∈ Σ ε reconhece A . Como existe um AFND que reconhece L ( G ), temos que A ´ e regular.

Suponha agora que A ´ e uma linguagem regular. Nesse caso, existe um AFD M = ( Q, Σ , δ, q 0 , F ) que reconhece A . Constru´ ımos a gram´ atica G = ( Q, Σ , P, q 0 ), onde, para cada δ ( X,a ) = Y , temos uma regra X → aY ∈ P ; e para cada p ∈ F , temos p → ε ∈ P . Note que L ( M ) = L ( G ). Logo, a gram´ atica G assim constru´ ıda ´ e uma GLUD e reconhece A . □

Usando uma prova similar (mas com alguns detalhes adicionais) ao Lema 3 obtemos o seguinte resultado.

Lema 4. Seja A uma linguagem. Existe uma GLUE que gera A se e somente se A ´ e uma linguagem regular.

Usando os Lemas 1, 2, 3 e 4, obtemos o seguinte resultado.

Teorema 1. Uma gram´ atica G ´ e regular se e somente se L ( G ) ´ e regular.

## Exerc´ ıcios

- 1. Descreva gram´ aticas lineares para cada uma das linguagens abaixo considerando o alfabeto Σ = { 0 , 1 } .
- (a) { x : x tem no m´ aximo um par de 0's como subcadeia e no m´ aximo um par de 1's como subcadeia } .
- (b) { x : qualquer par de 0's antecede qualquer par de 1's } .
- (c) x : x n˜ ao possui 010 como subcadeia } .
- 2. Descreva uma GLD que gera a linguagem A = { x ∈ { 0 , 1 } ∗ : 0010 ´ e subcadeia de x } .
- 3. Do item anterior, descreva um AFND que reconhece A usando a constru¸ c˜ ao nos Lemas 2.
- 4. A partir do AFN D do item anterior, obtenha um AFD que reconhece A .
- 5. Minimize o AFD obtido no item anterior.

- 6. Descreva uma GLUE que gera uma linguagem A a partir de uma GLE que gera A .
- 7. Descreva uma GLUE que gera uma linguagem A a partir de um AFD que reconhece A .
- 8. Descreva um AFND que reconhece uma linguagem A a partir de uma GLUE que gera A .

## Referˆ encias Bibliogr´ aficas