## Gram´ aticas e linguagens livre de contexto

## Gram´ aticas livres de contexto

Uma gram´ atica livre de contexto ´ e uma gram´ atica G = ( V, Σ , P , S ) onde cada regra de produ¸ c˜ ao α → β em P ´ e tal que α ∈ V e β ∈ ( V ∪ Σ) ∗ , ou seja, o que caracteriza o fato de uma linguagem ser livre de contexto ´ e que do lado esquerdo de cada regra de produ¸ c˜ ao h´ a exatamente uma vari´ avel.

Umalinguagem A ´ e dita livre de contexto - LLC ou do tipo 2 se existe uma gram´ atica livre de contexto G tal que L ( G ) = A . Por exemplo, a linguagem A = { a n b n : n ≥ 0 } ´ e livre de contexto pois

<!-- formula-not-decoded -->

gera a linguagem A e ´ e LLC.

## Exerc´ ıcios

Mostre que as seguintes linguagens s˜ ao LLC.

- 1. { a n b n : n ≥ 0 } ;
- 2. { a n b m c n : n, m ≥ 0 } ;
- 3. { a n b m : n ≤ m ≤ 2 n } ;

<!-- formula-not-decoded -->

Argumente do porque vale o seguinte resultado.

Lema 1. Toda linguagem regular ´ e LLC.

## Deriva¸ c˜ oes mais a esquerda e mais a direita

H´ a algumas vantagens pr´ aticas e te´ oricas em substituirmos a vari´ avel mais ` a esquerda em cada deriva¸ c˜ ao ou, analogamente, a vari´ avel mais ` a direita. Tais deriva¸ c˜ oes s˜ ao denominadas deriva¸ c˜ oes mais ` a esquerda e deriva¸ c˜ oes mais ` a direita , respectivamente, e s˜ ao formalmente definidas como segue:

Sejam ( V, Σ , P , S ) uma GLC, e α, β ∈ ( V ∪ Σ) ∗ . Ent˜ ao, n´ os dizemos que α ⇒ β ´ e um passo de uma deriva¸ c˜ ao mais ` a esquerda se existirem x ∈ Σ ∗ , ρ ∈ ( V ∪ Σ) ∗ e uma produ¸ c˜ ao ( A → γ ) ∈ P tais que

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

´ e uma deriva¸ c˜ ao mais a esquerda em n passos de γ 0 em γ n se cada γ i -1 ⇒ γ i ´ e um passo de uma deriva¸ c˜ ao mais a esquerda para cada i = 1 , . . . , n . Similarmente definimos um passo de uma deriva¸ c˜ ao mais a direita e deriva¸ c˜ ao mais a direita em n passos .

## Exemplo 1. Considere a GLC

<!-- formula-not-decoded -->

Ent˜ ao, a cadeia a + a × a possui as deriva¸ c˜ oes mais ` a esquerda e mais ` a direita em G mostradas a seguir respectivamente (usamos negrito para identificar a vari´ avel substitu´ ıda):

<!-- formula-not-decoded -->

e

Uma deriva¸ c˜ ao

<!-- formula-not-decoded -->

- O lema a seguir tem implica¸ c˜ oes pr´ aticas importantes para a complexidade dos algoritmos de an´ alise sint´ atica em Compiladores.

Fato 1. Sejam G = ( V, Σ , P , S ) uma GLC, w ∈ Σ ∗ e α ∈ ( V ∪ Σ) ∗ . Se α n ⇒ w para n ∈ N , ent˜ ao h´ a uma deriva¸ c˜ ao mais ` a esquerda (direita) de α para w em n passos.

Prova . Indu¸ c˜ ao em n provamos que h´ a uma deriva¸ c˜ ao ` a esquerda. Uma prova da mesma afirma¸ c˜ ao para deriva¸ c˜ oes mais ` a direita ´ e an´ aloga.

Vale por vacuidade para n = 0.

Suponha ent˜ ao que n &gt; 0. Ent˜ ao, a deriva¸ c˜ ao α n ⇒ w ´ e da forma

<!-- formula-not-decoded -->

H´ a dois casos a considerar:

- 1) Suponha que α ⇒ β ´ e o passo de uma deriva¸ c˜ ao mais ` a esquerda. Pela hip´ otese de indu¸ c˜ ao, h´ a uma deriva¸ c˜ ao mais ` a esquerda em n -1 passos de β a w o que implica por defini¸ c˜ ao que existe uma deriva¸ c˜ ao mais a esquerda de α a w em n passos.
- 2) Suponha agora que o passo de deriva¸ c˜ ao α ⇒ β n˜ ao ´ e uma deriva¸ c˜ ao mais ` a esquerda. Ent˜ ao n &gt; 1 e existem x ∈ Σ ∗ , µ, ρ ∈ ( V ∪ Σ) ∗ , vari´ aveis A e B e uma produ¸ c˜ ao B → δ tais que

<!-- formula-not-decoded -->

Como β n -1 ⇒ w , pela hip´ otese de indu¸ c˜ ao, deve existir uma deriva¸ c˜ ao mais ` a esquerda de β a w . Como β = xAµδρ e A ´ e a vari´ avel mais ` a esquerda em β , o primeiro passo de uma deriva¸ c˜ ao mais ` a esquerda de β a w ´ e da forma xAµδρ ⇒ xγµδρ, para alguma produ¸ c˜ ao A → γ . Logo,

<!-- formula-not-decoded -->

N´ os podemos trocar a ordem dos dois primeiros passos envolvendo as regras B → δ e A → γ , e obtemos a deriva¸ c˜ ao

<!-- formula-not-decoded -->

A deriva¸ c˜ ao acima pode ser feita em n passo e o primeiro passo ´ e uma deriva¸ c˜ ao mais ` a esquerda. Isto implica que estamos de volta ao caso 1. Logo, existe uma deriva¸ c˜ ao mais ` a esquerda de α a w em n passos.

Como consequˆ encia do fato acima temos:

Lema 2. Seja G = ( V, Σ , P , S ) uma GLC. Ent˜ ao, para toda cadeia w ∈ Σ ∗ tal que w ∈ L ( G ) , h´ a uma deriva¸ c˜ ao mais ` a esquerda e uma deriva¸ c˜ ao mais ` a direita em G que geram w .

## Exerc´ ıcios

- 1. Considere a gram´ atica

tal que

<!-- formula-not-decoded -->

Ent˜ ao,

- (a) Quais cadeias de L ( G ) podem ser produzidas por deriva¸ c˜ oes de, no m´ aximo, quatro passos?
- (b) Forne¸ ca pelo menos quatro deriva¸ c˜ oes diferentes para a cadeia babbab ?
- (c) Para quaisquer inteiros positivos, m , n , e p , descreva uma deriva¸ c˜ ao em G da cadeia b m ab n ab p .

## ´ Arvores de an´ alise sint´ atica

Uma ´ arvore sint´ atica ´ e uma estrutura que representa uma cole¸ c˜ ao de deriva¸ c˜ oes que gera uma cadeia em (Σ ∪ V ) ∗ a partir de uma vari´ avel inicial em GLC. Formalmente, uma ´ arvore sint´ atica para uma GLC G = ( V, Σ , P , S ) ´ e uma ´ arvore enraizada e ordenada que satisfaz as seguintes condi¸ c˜ oes:

- 1. Cada n´ o interior ´ e rotulado por uma vari´ avel em V .

<!-- formula-not-decoded -->

- 2. Cada folha ´ e rotulada por uma vari´ avel, um s´ ımbolo do alfabeto ou ϵ . No entanto, se a folha for rotulada por ϵ , ela deve ser o ´ unico filho de seu pai.
- 3. Se um n´ o interior ´ e rotulado A e seus filhos s˜ ao rotulados α 1 , α 2 , . . . , α , respectivamente, da esquerda para a direita e com cada α i ∈ ( V ∪ Σ) ∗ , ent˜ ao A → α 1 α 2 · · · α n ´ e uma produ¸ c˜ ao em P .

A Figura 1 mostra uma ´ arvore sint´ atica que gera a cadeia ()( S ) pela deriva¸ c˜ ao S ⇒ SS ⇒ ( S ) S ⇒ ( S )( S ) ⇒ ()( S ) atrav´ es da gram´ atica

<!-- formula-not-decoded -->

que gera a linguagem PARBAL = { x ∈ { ( , ) } ∗ | x ´ e balanceada } . A raiz ´ e identificada com a produ¸ c˜ ao S → SS , pois os dois filhos da raiz possuem r´ otulo S e S , respectivamente, da esquerda para a direita. Os filhos mais ` a esquerda e mais ` a direita da raiz s˜ ao ambos associados com a produ¸ c˜ ao S → ( S ), pois os trˆ es filhos do filho mais ` a esquerda (resp. mais ` a direita) da raiz s˜ ao rotulados com (, S e ), respectivamente, da esquerda para a direita.

Figura 1: Uma ´ arvore sint´ atica para a gram´ atica que gera a linguagem PARBAL.

<!-- image -->

Se examinarmos as folhas de uma ´ arvore sint´ atica e as concatenarmos a partir da esquerda, obteremos uma cadeia em (Σ ∪ V ) ∗ chamada resultado da ´ arvore , que ´ e sempre uma cadeia derivada da vari´ avel raiz. S˜ ao importantes as ´ arvores sint´ aticas cujas ra´ ızes s˜ ao rotuladas com o s´ ımbolo inicial da gram´ atica e seus resultados s˜ ao cadeias em Σ ∗ .

## Exerc´ ıcios

- 1. Considere a gram´ atica

<!-- formula-not-decoded -->

Mostre para a cadeia aab ∈ L ( G ) uma

- (a) ´ Arvores sint´ aticas.
- (b) Deriva¸ c˜ oes mais ` a esquerda.
- (c) Deriva¸ c˜ oes mais ` a direita.
- 2. Suponha que G seja uma GLC sem quaisquer produ¸ c˜ oes que tenha ϵ como lado direito. Se w est´ a em L ( G ), o comprimento de w ´ e n , e w pode ser derivada em G com m passos de deriva¸ c˜ ao a partir do s´ ımbolo inicial de G , mostre que w possui uma ´ arvore sint´ atica com n + m n´ os.

## Simplifica¸ c˜ ao de Gram´ aticas Livres de Contexto

A defini¸ c˜ ao de uma LLC n˜ ao imp˜ oe nenhuma restri¸ c˜ ao no 'lado direito' de uma produ¸ c˜ ao. Entretanto, em algumas ocasi˜ oes, impor restri¸ c˜ oes na gram´ atica pode facilitar uma demonstra¸ c˜ ao ou reduzir a complexidade de um algoritmo. Nesta se¸ c˜ ao, estudamos v´ arias transforma¸ c˜ oes e substitui¸ c˜ oes que podem ser utilizadas para transformar uma GLC em outra GLC equivalente e cujas produ¸ c˜ oes obedecem a certas restri¸ c˜ oes.

## Uma regra ´ util de substitui¸ c˜ ao

Teorema 1. Sejam G = ( V, Σ , P , S ) uma GLC e A → α 1 Bα 2 ∈ P com α 1 , α 2 ∈ (Σ ∪ V ) ∗ e A, B ∈ V . Suponha que B → β 1 | β 2 | · · · | β m seja o conjunto de todas as produ¸ c˜ oes em P que possuem B do 'lado esquerdo' e β i ∈ (Σ ∪ V ) ∗ , para todo i .

Considere a GLC G ′ = ( V, Σ , P ′ , S ) onde P ′ ´ e obtido pela remo¸ c˜ ao de A → α 1 Bα 2 e a inclus˜ ao de A → α 1 β 1 α 2 | α 1 β 2 α 2 | · · · | α 1 β m α 2 em P .

Ent˜ ao, temos que L ( G ) = L ( G ′ ) .

## Exemplo 2. Considere

tal que L ( G ′ ) = L ( G ) .

## Elimina¸ c˜ ao de produ¸ c˜ oes in´ uteis

Seja G = ( V, Σ , P , S ) uma GLC. Uma vari´ avel A ∈ V ´ e dita ´ util se existe pelo menos uma cadeia w ∈ L ( G ) tal que S ∗ ⇒ αAβ ∗ ⇒ w , com α, β ∈ ( V ∪ Σ) ∗ . Em outras palavras, uma vari´ avel ´ e ´ util se ela ´ e usada em pelo menos uma deriva¸ c˜ ao de alguma cadeia. Uma vari´ avel que n˜ ao ´ e ´ util ´ e dita in´ util . Uma produ¸ c˜ ao ´ e in´ util se ela cont´ em pelo menos uma vari´ avel in´ util.

Queremos eliminar produ¸ c˜ oes in´ uteis pois elas n˜ ao servem para gerar cadeias da gram´ atica que ela gera. Por exemplo, seja

<!-- formula-not-decoded -->

uma GLC.

Primeiramente computamos o conjunto Φ de s´ ımbolos geradores de G .

algoritmo computa Φ( G ) :=

- 1. Φ := ∅ ;
- 2. enquanto existir ( A → α ) ∈ P tal que α ∈ (Σ ∪ Φ) ∗ fa¸ ca
- 3. Φ ← Φ ∪ { A }
- 4. devolva Φ.

<!-- formula-not-decoded -->

Usando o Teorema 1, podemos obter uma nova GLC G ′ removendo a produ¸ c˜ ao A → abBc e acrescentando as regras A → ababbAc | abbc . Assim,

<!-- formula-not-decoded -->

O tempo gasto pelo algoritmo ´ e O ( |P| · | V | ) se o n´ umero de s´ ımbolos em cada produ¸ c˜ ao ´ e constante. Em cada itera¸ c˜ ao, examinamos cada produ¸ c˜ ao e o n´ umero total de itera¸ c˜ oes ´ e | V | .

Se executarmos o algoritmo acima com a GLC do nosso exemplo, obteremos Φ = { S, A, B } e a gram´ atica que ´ e induzida por essas vari´ aveis ´ e

<!-- formula-not-decoded -->

Depois de encontrar Φ, computamos o conjunto Ψ de vari´ aveis ating´ ıveis de G ′ a partir de S . Mais precisamente consideramos o digrafo D = (Φ , A ) onde

<!-- formula-not-decoded -->

e determinamos Ψ := { A ∈ Φ : existe um caminho de S a A em D } . Note que se S ̸∈ Φ, ent˜ ao Ψ = ∅ .

<!-- image -->

Figura 2: Executando o segundo passo para o grafo G ′ , obtemos Ψ := { S, A } . Geramos uma GLC, G ′′ , que cont´ em todas as produ¸ c˜ oes de G em que todos as vari´ aveis pertencem a Ψ: G ′′ := S → aS | A, A → a .

Oalgoritmo acima gasta tempo O |P| para construir o digrafo D quando o n´ umero de s´ ımbolos em cada produ¸ c˜ ao ´ e constante e O ( |P| + | V | ) para encontrar as vari´ aveis alcan¸ c´ aveis por S usando nesse ´ ultimo caso algum algoritmo de busca tais como busca em profundidade e busca e largura. A constru¸ c˜ ao acima nos permite concluir o seguinte resultado.

Teorema 2. Seja G uma GLC qualquer. Ent˜ ao, existe uma GLC equivalente a G que n˜ ao possui nenhuma vari´ avel in´ util.

Prova . Prova construtiva mas sendo os detalhes omitidos.

As produ¸ c˜ oes ´ uteis s˜ ao aquelas que n˜ ao cont´ em vari´ aveis in´ uteis.

## Elimina¸ c˜ ao de produ¸ c˜ oes nulas

Em uma GLC, qualquer produ¸ c˜ ao da forma

<!-- formula-not-decoded -->

´ e chamada de produ¸ c˜ ao nula .

Lema 3. Seja G uma GLC e S sua vari´ avel inicial. Existe uma GLC G ′ sem produ¸ c˜ oes nulas, exceto eventualmente a produ¸ c˜ ao S → ϵ , tal que L ( G ′ ) = L ( G ) .

̸

<!-- formula-not-decoded -->

Aplicando a regra da prova do Lema 3 (s˜ ao v´ arios passos, verifique - primeiro eliminamos B → ϵ , depois C → ϵ e finalmente A → ϵ ), obtemos

<!-- formula-not-decoded -->

Prova . ( Esbo¸ co ) A obten¸ c˜ ao de G ′ ´ e construtiva e ´ e algor´ ıtmica. Primeiro, enquanto houver uma produ¸ c˜ ao A → ϵ com A = S , para cada produ¸ c˜ ao B → αAβ com α, β ∈ (Σ ∪ V ) ∗ , acrescente a produ¸ c˜ ao B → αβ . Se α = β = ϵ , acrescente a regra B → ϵ a menos que esta regra tenha sido previamente removida. Repetimos esses passos at´ e que eliminemos todas as produ¸ c˜ oes nulas que n˜ ao envolvam a vari´ avel inicial e obtemos a gram´ atica G ′ . Note que L ( G ) = L ( G ′ ). □

## Exemplo 3. Seja a gram´ atica

□

## Elimina¸ c˜ ao de produ¸ c˜ oes unit´ arias

Em uma GLC G = ( V, Σ , P , S ), qualquer produ¸ c˜ ao da forma

<!-- formula-not-decoded -->

onde A, B ∈ V , ´ e chamada de produ¸ c˜ ao unit´ aria .

Lema 4. Seja G uma GLC. Existe GLC G ′ sem produ¸ c˜ oes unit´ arias tal que L ( G ′ ) = L ( G ) .

Prova . ( Esbo¸ co ) Semelhante ` a prova do Lema 3, construa uma gram´ atica G ′ a partir de G acrescentando produ¸ c˜ oes A → γ sempre que tivermos A → B e B → γ . Se γ ´ e uma vari´ avel, acrescente a regra A → γ a menos que esta regra tenha sido removida anteriormente. Repita esse processo at´ e que n˜ ao existam mais produ¸ c˜ oes unit´ arias. Note que L ( G ) = L ( G ′ ). □

## Exemplo 4. Seja a gram´ atica

<!-- formula-not-decoded -->

Usando a regra da prova do Lema 4 (elimine nessa ordem as regras S → B , S → A , B → A e a → B ) obtemos

<!-- formula-not-decoded -->

removendo as produ¸ c˜ oes unit´ arias.

## Exerc´ ıcios

- 1. Mostre que as gram´ aticas

<!-- formula-not-decoded -->

e

s˜ ao equivalentes.

- 2. Elimine todas as produ¸ c˜ oes in´ uteis da gram´ atica

<!-- formula-not-decoded -->

Qual ´ e a linguagem gerada pela gram´ atica?

- 3. Elimine todas as produ¸ c˜ oes nulas da gram´ atica

<!-- formula-not-decoded -->

- 4. Elimine todas as produ¸ c˜ oes nulas, unit´ arias e in´ uteis da gram´ atica

<!-- formula-not-decoded -->

Qual ´ e a linguagem gerada pela gram´ atica?

- 5. Dˆ e um exemplo de uma situa¸ c˜ ao em que a elimina¸ c˜ ao de produ¸ c˜ oes nulas introduz produ¸ c˜ oes unit´ arias que n˜ ao existiam antes. Em seguida, argumente sobre a ordem em que os procedimentos de elimina¸ c˜ ao de produ¸ c˜ oes nulas e de produ¸ c˜ oes unit´ arias devem ser aplicados se queremos uma gram´ atica sem produ¸ c˜ oes nulas e sem produ¸ c˜ oes unit´ arias.
- 6. Prove que se uma gram´ atica n˜ ao possui nenhuma produ¸ c˜ ao nula e nenhuma produ¸ c˜ ao unit´ aria, ent˜ ao a elimina¸ c˜ ao de produ¸ c˜ oes in´ uteis, pela constru¸ c˜ ao dada neste cap´ ıtulo, n˜ ao introduz nenhuma produ¸ c˜ ao nula nem unit´ aria. Em seguida, argumente sobre a ordem em que os procedimentos de elimina¸ c˜ ao de produ¸ c˜ oes nulas, unit´ arias e in´ uteis devem ser aplicados se n˜ ao queremos esses tipos de produ¸ c˜ ao em nossa gram´ atica.

<!-- formula-not-decoded -->

- 7. Suponha que uma GLC G tenha uma produ¸ c˜ ao da forma

<!-- formula-not-decoded -->

Prove que se esta regra for substitu´ ıda por

<!-- formula-not-decoded -->

onde B ´ e uma nova vari´ avel introduzida em G , ent˜ ao a gram´ atica resultante ser´ a equivalente ` a original.

- 8. Considere o procedimento de dois passos, dado neste cap´ ıtulo, para eliminar produ¸ c˜ oes in´ uteis. Inverta a ordem dos dois passos. Isto ´ e, primeiro calcule o conjunto Ψ dos s´ ımbolos ating´ ıveis e, em seguida, calcule o conjunto Φ dos s´ ımbolos geradores. Vocˆ e acha que esta invers˜ ao de passos produz um procedimento correto para gerar uma gram´ atica equivalente ` a original, mas sem produ¸ c˜ oes in´ uteis? Se sim, prove que vocˆ e est´ a correto. Caso contr´ ario, forne¸ ca um contraexemplo.

## Formas Normais

Em muitas aplica¸ c˜ oes ´ e comum assumirmos que as produ¸ c˜ oes de uma GLC's est˜ ao restritas a uma dada forma especial. Duas dessas formas ´ uteis s˜ ao a Forma Normal de Chomsky (FNC) e a Forma Normal de Greibach (FNG).

## Forma Normal de Chomsky

̸

Uma GLC G = ( V, Σ , P , S ) est´ a na Forma Normal de Chomsky (FNC) se e somente se todas as produ¸ c˜ oes de G s˜ ao da forma A → BC ou A → a , onde A, B, C ∈ V e a ∈ Σ e A = S . Adicionalmente, permitimos a regra S → ϵ .

Exemplo 5. A gram´ atica

<!-- formula-not-decoded -->

est´ a na FNC. Note que a linguagem L ( G ) gerada por G ´ e exatamente

<!-- formula-not-decoded -->

Teorema 3. Dada uma GLC G = ( V, Σ , P , S ) , h´ a uma GLC G ′ na FNC com L ( G ′ ) = L ( G ) .

Prova . (esbo¸ co) A prova ´ e construtiva. A gram´ atica ser´ a modificada sem mudar a linguagem por ela gerada. Vamos acompanhar um exemplo para acompanhar essa transforma¸ c˜ ao. Considere inicialmente a gram´ atica

<!-- formula-not-decoded -->

Passo 1. Crie uma vari´ avel inicial S ′ e a regra S ′ → S para garantir que a vari´ avel inicial n˜ ao apare¸ ca do lado direito de alguma regra. Ficamos assim

<!-- formula-not-decoded -->

com a gram´ atica de nosso exemplo.

Passo 2. Elimine as transi¸ c˜ oes nulas usando o Lema 3 e obtenha a gram´ atica

<!-- formula-not-decoded -->

que ´ e equivalente ` a gram´ atica de nosso exemplo.

Passo 3. Elimine as transi¸ c˜ oes unit´ arias usando o Lema 4 e obtenha a gram´ atica

<!-- formula-not-decoded -->

Passo 4. As regras remanescentes indesej´ aveis da forma

<!-- formula-not-decoded -->

onde k ≥ 3 e cada u i ∈ (Σ ∪ V ) s˜ ao substitu´ ıdas por k -1 novas regras

<!-- formula-not-decoded -->

onde cada A i ´ e uma nova vari´ avel. A gram´ atica de nosso exemplo fica assim.

<!-- formula-not-decoded -->

Passo 5. Para cada regra X → uv onde u ∈ Σ ou v ∈ Σ, substitua o elemento em Σ por uma vari´ avel e acrescente mais uma regra convertendo essa vari´ avel no s´ ımbolo em Σ. Assim, em nosso exemplo

<!-- formula-not-decoded -->

que est´ a na FNC e L ( G ′ ) = L ( G ).

□

Exemplo 6. Seja a GLC G := S → aSb | ϵ . Note que L ( G ) = { a n b n | n ∈ Z , n ≥ 0 } .

Passo 1

Passo 2

Passo 3

Passo 4

Passo 5

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Exemplo 7. Seja G := S → ( S ) | SS | ϵ uma GLC. Note que L ( G ) ´ e PARBAL definida em (1).

Passo 1

<!-- formula-not-decoded -->

Passo 2

Passo 3

Passo 4

Passo 5

Exemplo 8. Seja a GLC

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## Passo 1

## Passo 2

## Passo 3

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

```
S ′ → CBh | be | SABC | ABC | ϵ S → CBh | be | SABC | ABC A → aaD B → Sf | ggg | f C → cA | d D → be | SABC | ABC E → be.
```

## Passo 4

```
S ′ → CX 1 | be | SX 2 | AX 3 | ϵ S → CX 1 | be | SX 2 | AX 3 A → aX 4 B → Sf | gX 5 | f C → cA | d D → be | SX 2 | AX 3 E → be X 1 → Bh X 2 → AX 3 X 3 → BC X 4 → aD X 5 → gg.
```

## Passo 5

## Exerc´ ıcios

1. Seja

```
S ′ → CX 1 | U 1 U 2 | SX 2 | AX 3 | ϵ S → CX 1 | U 1 U 2 | SX 2 | AX 3 A → U 3 X 4 B → SU 4 | U 6 X 5 | f C → U 5 A | d D → U 1 U 2 | SX 2 | AX 3 E → U 1 U 2 X 1 → BU 8 X 2 → AX 3 X 3 → BC X 4 → U 3 D X 5 → U 6 U 6 U 1 → b U 2 → e U 3 → a U 4 → f U 5 → c U 6 → g U 7 → d
```

U 8 → h

<!-- formula-not-decoded -->

uma GLC. Forne¸ ca uma GLC G ′ na FNC tal que L ( G ′ ) = L ( G ).

- 2. Seja G uma gram´ atica livre de contexto na FNC. Ent˜ ao, mostre que qualquer

cadeia w ∈ L ( G ) ´ e derivada a partir do s´ ımbolo inicial de G com exatamente 2 · | w | -1 passos de deriva¸ c˜ ao.

## Forma Normal de Greibach

Vide [Enc14]. Uma GLC G = ( V, Σ , P , S ) est´ a na Forma Normal de Greibach (FNG) se a vari´ avel inicial nunca aparece do lado direito de uma regra e todas as produ¸ c˜ oes de G s˜ ao da forma S → ϵ ou

<!-- formula-not-decoded -->

para algum k ∈ N , A, B 1 , . . . , B k ∈ V e a ∈ Σ. Note que k = 0 ´ e permitido, o que implica que podemos ter produ¸ c˜ oes da forma A → a .

Exemplo 9. A gram´ atica

<!-- formula-not-decoded -->

est´ a na Forma Normal de Greibach. Note que a linguagem deste exemplo ´ e PARBAL (1).

Nessa se¸ c˜ ao mostramos como transformar uma GLC qualquer em uma GLC na FNG. Para isso usamos o resultado obtido no pr´ oximo lema. Nessa se¸ c˜ ao nos referimos a uma produ¸ c˜ ao com a vari´ avel A do lado esquerdo como produ¸ c˜ ao -A .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

e A → β 1 | β 2 | · · · | β s as demais produ¸ c˜ oesA em uma GLC G . Considere G ′ uma gram´ atica obtida a partir de G pela substitui¸ c˜ ao de cada A → Aα ∈ A pelas produ¸ c˜ oes

<!-- formula-not-decoded -->

onde B ´ e uma nova vari´ avel. Ent˜ ao, L ( G ′ ) = L ( G ) .

Prova . (esbo¸ co) Mostrar que L ( G ) ⊆ L ( G ′ ) e que L ( G ′ ) ⊆ L ( G ). Seja B o conjunto de todas as regras adicionadas ap´ os a remo¸ c˜ ao dos elementos em A para a obten¸ c˜ ao de G ′ .

Seja G ′′ uma GLC que possui conjunto de produ¸ c˜ oes de G e de G ′ . Temos ent˜ ao que os conjuntos de produ¸ c˜ oes de G , G ′ e G ′′ s˜ ao respectivamente P , ( P -A ) ∪B e P ∪ B . Logo,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Seja w uma cadeia arbitr´ aria em L ( G ′′ ).

Queremos mostrar primeiramente que existe uma deriva¸ c˜ ao de w em G ′′ que n˜ ao usa regras em A . Ent˜ ao, suponha por contradi¸ c˜ ao que toda deriva¸ c˜ ao de w usa pelo menos uma regra em A . O Lema 2 garante existir uma deriva¸ c˜ ao mais a esquerda de w . Considere a seguir aquela que usa a menor quantidade de vezes uma regra em A onde destacamos a ´ ultima vez que uma dessas regras ´ e utilizada:

<!-- formula-not-decoded -->

Note que a sequˆ encia de deriva¸ c˜ oes em destaque pode ser substitu´ ıda por

<!-- formula-not-decoded -->

que ´ e uma deriva¸ c˜ ao de w que usa menos vezes uma regra em A o que ´ e uma contradi¸ c˜ ao. Logo, existe uma deriva¸ c˜ ao de w em G ′′ que n˜ ao usa regras em A . Isto implica que L ( G ′′ ) ⊆ L ( G ′ ). Segue de (2) que L ( G ) ⊆ L ( G ′′ ) ⊆ L ( G ′ ) o que implica que L ( G ) ⊆ L ( G ′ ).

′′

Vamos mostrar agora que existe uma deriva¸ c˜ ao de w em G que n˜ ao usa regras em B . Suponha por contradi¸ c˜ ao que toda deriva¸ c˜ ao de w usa pelo menos uma regra em B . O Lema 2 garante existir uma deriva¸ c˜ ao mais a direita de w . Considere uma delas em n passos que usa a menor quantidade de vezes uma regra em B pode ser esbo¸ cada abaixo:

<!-- formula-not-decoded -->

onde v ∈ Σ ∗ . Note que a sequˆ encia de deriva¸ c˜ oes em (4) pode ser substitu´ ıda por

uAv ⇒ uβAα k +1 v ⇒ uAα k α k +1 v ⇒ . . . ⇒ uAα 1 . . . α k α k +1 v ⇒ uβα 1 . . . α k α k +1 v

que ´ e uma deriva¸ c˜ ao a direita em n passos de w que usa menos vezes uma regra em B o que ´ e uma contradi¸ c˜ ao. Logo, existe uma deriva¸ c˜ ao de w em G ′′ que n˜ ao usa regras em B . Isto implica que L ( G ′′ ) ⊆ L ( G ). Segue de (2) que L ( G ′ ) ⊆ L ( G ′′ ) ⊆ L ( G ) o que implica que L ( G ) ⊆ L ( G ′ ). □

Voltamos agora ` a nossa transforma¸ c˜ ao de uma GLC qualquer em uma FNG na FNG.

Teorema 4. Dada qualquer GLC G , h´ a uma GLC G ′ na FNG tal que L ( G ′ ) = L ( G ) .

Prova . (esbo¸ co) Como sempre, n˜ ao faremos uma prova formal do resultado. Mostramos simplesmente uma constru¸ c˜ ao que transforma uma GLC qualquer em uma na FNG. Explicamos cada passo no caso geral e no caso particular de um exemplo utilizado para exemplificar a constru¸ c˜ ao. A justificativa dos passos fica por conta dos resultados estudados anteriormente e da intui¸ c˜ ao.

Passo 1. Dada uma GCL, obtenha a gram´ atica na FNC.

Passo 2. Estabele¸ ca uma ordena¸ c˜ ao das vari´ aveis da GLC obtida no Passo 1.

Suponha ent˜ ao que a GLC obtida ap´ os o Passo 2 seja

<!-- formula-not-decoded -->

Passo 3. Esse passo modifica as produ¸ c˜ oes da GLC de modo que as produ¸ c˜ oes resultantes sejam tais que se A i → A j α ´ e uma produ¸ c˜ ao, ent˜ ao j &gt; i . Come¸ cando com A 1 e procedendo at´ e A m , usamos o seguinte procedimento indutivo explicado a seguir.

Assuma que as produ¸ c˜ oes j´ a tenham sido modificadas de tal modo que, para todo 1 ≤ i &lt; k , se A i → A j α ´ e uma produ¸ c˜ ao, ent˜ ao j &gt; i . Ent˜ ao, modificamos as produ¸ c˜ oesA k .

Se A k → A j α ´ e uma produ¸ c˜ ao com j &lt; k , n´ os geramos um novo conjunto de produ¸ c˜ oes que substitui o lado direito de A k → A j α pelo lado direito das produ¸ c˜ oesA j usando o Lema 1. Repetindo este processo, no m´ aximo, k -1 vezes, para cada produ¸ c˜ ao A k → A j α , com j &lt; k , n´ os obtemos produ¸ c˜ oes da forma A k → A l α , com l ≥ k .

No nosso exemplo, modificar´ ıamos primeiro a produ¸ c˜ ao

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

A → A A

<!-- formula-not-decoded -->

Em seguida, n´ os substitu´ ımos as produ¸ c˜ oes com l = k atrav´ es da introdu¸ c˜ ao de um novo vari´ avel B k como explicado no enunciado do Lema 5.

O resultado do passo anterior ´ e um conjunto de produ¸ c˜ oes da forma

<!-- formula-not-decoded -->

Assim, no nosso exemplo a GLD ficaria assim.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

substituindo-a por

e depois por

obtendo a GLD

que podemos escrever

```
A 0 → A 2 A 3 A 1 → A 2 A 3 A 2 → A 3 A 1 | b, A 3 → bA 3 A 2 | a | bA 3 A 2 B 3 | aB 3 B 3 → A 1 A 3 A 2 | A 1 A 3 A 2 B 3 .
```

As observa¸ c˜ oes a seguir valem para o nosso mas, mais forte do que isto, como consequˆ encia do m´ etodo utilizado, vale para qualquer gram´ atica.

Passo 3. Note que o s´ ımbolo mais ` a esquerda do lado direito de qualquer produ¸ c˜ aoA m deve ser um s´ ımbolo do alfabeto. O s´ ımbolo mais ` a esquerda do lado direito de qualquer produ¸ c˜ aoA m -1 deve ser A m ou um elemento de Σ. Quando ele for A m , n´ os podemos gerar novas produ¸ c˜ oesA m -1 substituindo A m pelo lado direito das produ¸ c˜ oesA m de acordo com o Lema 1. Cada uma destas novas produ¸ c˜ oes possui lado direito come¸ cando com um s´ ımbolo de Σ. Logo, podemos repetir o mesmo procedimento para A m -2 , . . . , A 2 , A 1 , nesta ordem, at´ e que o lado direito de cada produ¸ c˜ aoA i comece com um elemento em Σ. O resultado ´ e um conjunto de produ¸ c˜ oes da forma

<!-- formula-not-decoded -->

com a ∈ Σ e γ ∈ ( V ∪ Σ ∪ { B 1 , . . . , B i -1 } ) ∗ . Note que o lado direito de cada B i pode come¸ car com um vari´ avel do tipo A i . Assim, em nosso exemplo, obtemos a gram´ atica

```
A 0 → bA 3 A 2 A 1 A 3 | bA 3 A 2 B 3 A 1 A 3 | aA 1 A 3 | aB 3 A 1 A 3 | bA 3 A 1 → bA 3 A 2 A 1 A 3 | bA 3 A 2 B 3 A 1 A 3 | aA 1 A 3 | aB 3 A 1 A 3 | bA 3 A 2 → bA 3 A 2 A 1 | bA 3 A 2 B 3 A 1 | aA 1 | aB 3 A 1 | b A 3 → bA 3 A 2 | bA 3 A 2 B 3 | a | aB 3 B 3 → A 1 A 3 A 2 | A 1 A 3 A 2 B 3 .
```

Como todas as produ¸ c˜ oesB j possuem lados direitos que iniciam com um s´ ımbolo do alfabeto ou um vari´ avel A i . Logo, uma aplica¸ c˜ ao a mais do Lema 1 para cada produ¸ c˜ aoB j completa a constru¸ c˜ ao da gram´ atica G ′ na FNG. Assim, no nosso exemplo, temos

```
A 0 → bA 3 A 2 A 1 A 3 | bA 3 A 2 B 3 A 1 A 3 | aA 1 A 3 | aB 3 A 1 A 3 | bA 3 A 1 → bA 3 A 2 A 1 A 3 | bA 3 A 2 B 3 A 1 A 3 | aA 1 A 3 | aB 3 A 1 A 3 | bA 3 A 2 → bA 3 A 2 A 1 | bA 3 A 2 B 3 A 1 | aA 1 | aB 3 A 1 | b A 3 → bA 3 A 2 | bA 3 A 2 B 3 | a | aB 3 B 3 → bA 3 A 2 A 1 A 3 A 3 A 2 | bA 3 A 2 B 3 A 1 A 3 A 3 A 2 | aA 1 A 3 A 3 A 2 | aB 3 A 1 A 3 A 3 A 2 | bA 3 A 3 A 2 | bA 3 A 2 A 1 A 3 A 3 A 2 B 3 | bA 3 A 2 B 3 A 1 A 3 A 3 A 2 B 3 | aA 1 A 3 A 3 A 2 B 3 | aB 3 A 1 A 3 A 3 A 2 B 3 | bA 3 A 3 A 2 B 3 .
```

□

## Exerc´ ıcios

- 1. Seja
- 4. Dada a GLD

<!-- formula-not-decoded -->

uma GLC. Forne¸ ca uma GLC G ′ na FNG tal que L ( G ′ ) = L ( G ).

- 2. Seja G uma gram´ atica livre de contexto na FNG. Ent˜ ao, mostre que qualquer cadeia w ∈ L ( G ) ´ e derivada a partir do s´ ımbolo inicial de G com exatamente | w | -1 passos de deriva¸ c˜ ao.
- 3. Construa uma gram´ atica livre de contexto que gere a linguagem

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

5.

encontre uma GLC sem vari´ aveis e produ¸ c˜ oes in´ uteis.

<!-- formula-not-decoded -->

encontre uma GLC equivalente, onde o s´ ımbolo reservado S n˜ ao aparece do lado direito das produ¸ c˜ oes e S → ϵ ´ e a ´ unica produ¸ c˜ ao nula.

## 6. Considere a GLC

<!-- formula-not-decoded -->

determine a linguagem gerada por essa gram´ atica.

- 7. Encontre uma GLC sem var´ ıaveis nem produ¸ c˜ oes in´ uteis equivalente a GLC

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Construa uma GLC equivalente sem vari´ aveis nem produ¸ c˜ oes in´ uteis.

- 8. Considere a GLC

## 9. Considere a GLC

<!-- formula-not-decoded -->

Descreva informalmente quem ´ e L ( G ) e encontre uma gram´ atica equivalente a G , na FNC.

## 10. Considere a GLC

<!-- formula-not-decoded -->

Descreva informalmente quem ´ e L ( G ) e encontre uma gram´ atica equivalente a G, escrita na FNG.

## Referˆ encias Bibliogr´ aficas

[Enc14] Wikipedia The Free Encyclopedia. Greibach normal form. http://en.wikipedia.org/wiki/Greibach normal form, March 2014.