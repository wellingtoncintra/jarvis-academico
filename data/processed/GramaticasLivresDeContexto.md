## Gramáticas e linguagens livre de contexto

## Gramáticas livres de contexto

Uma gramática livre de contexto é uma gramática G = ( V, Σ , P , S ) onde cada regra de produção α → β em P é tal que α ∈ V e β ∈ ( V ∪ Σ) ∗ , ou seja, o que caracteriza o fato de uma linguagem ser livre de contexto é que do lado esquerdo de cada regra de produção há exatamente uma variável.

Umalinguagem A é dita livre de contexto - LLC ou do tipo 2 se existe uma gramática livre de contexto G tal que L ( G ) = A . Por exemplo, a linguagem A = { a n b n : n ≥ 0 } é livre de contexto pois

gera a linguagem A e é LLC.

## Exercícios

Mostre que as seguintes linguagens são LLC.

- 1. { a n b n : n ≥ 0 } ;
- 2. { a n b m c n : n, m ≥ 0 } ;
- 3. { a n b m : n ≤ m ≤ 2 n } ;

Argumente do porque vale o seguinte resultado.

Lema 1. Toda linguagem regular é LLC.

## Derivações mais a esquerda e mais a direita

Há algumas vantagens práticas e teóricas em substituirmos a variável mais à esquerda em cada derivação ou, analogamente, a variável mais à direita. Tais derivações são denominadas derivações mais à esquerda e derivações mais à direita , respectivamente, e são formalmente definidas como segue:

Sejam ( V, Σ , P , S ) uma GLC, e α, β ∈ ( V ∪ Σ) ∗ . Então, nós dizemos que α ⇒ β é um passo de uma derivação mais à esquerda se existirem x ∈ Σ ∗ , ρ ∈ ( V ∪ Σ) ∗ e uma produção ( A → γ ) ∈ P tais que

é uma derivação mais a esquerda em n passos de γ 0 em γ n se cada γ i -1 ⇒ γ i é um passo de uma derivação mais a esquerda para cada i = 1 , . . . , n . Similarmente definimos um passo de uma derivação mais a direita e derivação mais a direita em n passos .

## Exemplo 1. Considere a GLC

Então, a cadeia a + a × a possui as derivações mais à esquerda e mais à direita em G mostradas a seguir respectivamente (usamos negrito para identificar a variável substituída):

e

Uma derivação

- O lema a seguir tem implicações práticas importantes para a complexidade dos algoritmos de análise sintática em Compiladores.

Fato 1. Sejam G = ( V, Σ , P , S ) uma GLC, w ∈ Σ ∗ e α ∈ ( V ∪ Σ) ∗ . Se α n ⇒ w para n ∈ N , então há uma derivação mais à esquerda (direita) de α para w em n passos.

Prova . Indução em n provamos que há uma derivação à esquerda. Uma prova da mesma afirmação para derivações mais à direita é análoga.

Vale por vacuidade para n = 0.

Suponha então que n &gt; 0. Então, a derivação α n ⇒ w é da forma

Há dois casos a considerar:

- 1) Suponha que α ⇒ β é o passo de uma derivação mais à esquerda. Pela hipótese de indução, há uma derivação mais à esquerda em n -1 passos de β a w o que implica por definição que existe uma derivação mais a esquerda de α a w em n passos.
- 2) Suponha agora que o passo de derivação α ⇒ β não é uma derivação mais à esquerda. Então n &gt; 1 e existem x ∈ Σ ∗ , µ, ρ ∈ ( V ∪ Σ) ∗ , variáveis A e B e uma produção B → δ tais que

Como β n -1 ⇒ w , pela hipótese de indução, deve existir uma derivação mais à esquerda de β a w . Como β = xAµδρ e A é a variável mais à esquerda em β , o primeiro passo de uma derivação mais à esquerda de β a w é da forma xAµδρ ⇒ xγµδρ, para alguma produção A → γ . Logo,

Nós podemos trocar a ordem dos dois primeiros passos envolvendo as regras B → δ e A → γ , e obtemos a derivação

A derivação acima pode ser feita em n passo e o primeiro passo é uma derivação mais à esquerda. Isto implica que estamos de volta ao caso 1. Logo, existe uma derivação mais à esquerda de α a w em n passos.

Como consequência do fato acima temos:

Lema 2. Seja G = ( V, Σ , P , S ) uma GLC. Então, para toda cadeia w ∈ Σ ∗ tal que w ∈ L ( G ) , há uma derivação mais à esquerda e uma derivação mais à direita em G que geram w .

## Exercícios

- 1. Considere a gramática

tal que

Então,

- (a) Quais cadeias de L ( G ) podem ser produzidas por derivações de, no máximo, quatro passos?
- (b) Forneça pelo menos quatro derivações diferentes para a cadeia babbab ?
- (c) Para quaisquer inteiros positivos, m , n , e p , descreva uma derivação em G da cadeia b m ab n ab p .

## Árvores de análise sintática

Uma árvore sintática é uma estrutura que representa uma coleção de derivações que gera uma cadeia em (Σ ∪ V ) ∗ a partir de uma variável inicial em GLC. Formalmente, uma árvore sintática para uma GLC G = ( V, Σ , P , S ) é uma árvore enraizada e ordenada que satisfaz as seguintes condições:

- 1. Cada nó interior é rotulado por uma variável em V .

- 2. Cada folha é rotulada por uma variável, um símbolo do alfabeto ou ϵ . No entanto, se a folha for rotulada por ϵ , ela deve ser o único filho de seu pai.
- 3. Se um nó interior é rotulado A e seus filhos são rotulados α 1 , α 2 , . . . , α , respectivamente, da esquerda para a direita e com cada α i ∈ ( V ∪ Σ) ∗ , então A → α 1 α 2 · · · α n é uma produção em P .

A Figura 1 mostra uma árvore sintática que gera a cadeia ()( S ) pela derivação S ⇒ SS ⇒ ( S ) S ⇒ ( S )( S ) ⇒ ()( S ) através da gramática

que gera a linguagem PARBAL = { x ∈ { ( , ) } ∗ | x é balanceada } . A raiz é identificada com a produção S → SS , pois os dois filhos da raiz possuem rótulo S e S , respectivamente, da esquerda para a direita. Os filhos mais à esquerda e mais à direita da raiz são ambos associados com a produção S → ( S ), pois os três filhos do filho mais à esquerda (resp. mais à direita) da raiz são rotulados com (, S e ), respectivamente, da esquerda para a direita.

Figura 1: Uma árvore sintática para a gramática que gera a linguagem PARBAL.

<!-- image -->

Se examinarmos as folhas de uma árvore sintática e as concatenarmos a partir da esquerda, obteremos uma cadeia em (Σ ∪ V ) ∗ chamada resultado da árvore , que é sempre uma cadeia derivada da variável raiz. São importantes as árvores sintáticas cujas raízes são rotuladas com o símbolo inicial da gramática e seus resultados são cadeias em Σ ∗ .

## Exercícios

- 1. Considere a gramática

Mostre para a cadeia aab ∈ L ( G ) uma

- (a) Árvores sintáticas.
- (b) Derivações mais à esquerda.
- (c) Derivações mais à direita.
- 2. Suponha que G seja uma GLC sem quaisquer produções que tenha ϵ como lado direito. Se w está em L ( G ), o comprimento de w é n , e w pode ser derivada em G com m passos de derivação a partir do símbolo inicial de G , mostre que w possui uma árvore sintática com n + m nós.

## Simplificação de Gramáticas Livres de Contexto

A definição de uma LLC não impõe nenhuma restrição no 'lado direito' de uma produção. Entretanto, em algumas ocasiões, impor restrições na gramática pode facilitar uma demonstração ou reduzir a complexidade de um algoritmo. Nesta seção, estudamos várias transformações e substituições que podem ser utilizadas para transformar uma GLC em outra GLC equivalente e cujas produções obedecem a certas restrições.

## Uma regra útil de substituição

Teorema 1. Sejam G = ( V, Σ , P , S ) uma GLC e A → α 1 Bα 2 ∈ P com α 1 , α 2 ∈ (Σ ∪ V ) ∗ e A, B ∈ V . Suponha que B → β 1 | β 2 | · · · | β m seja o conjunto de todas as produções em P que possuem B do 'lado esquerdo' e β i ∈ (Σ ∪ V ) ∗ , para todo i .

Considere a GLC G ′ = ( V, Σ , P ′ , S ) onde P ′ é obtido pela remoção de A → α 1 Bα 2 e a inclusão de A → α 1 β 1 α 2 | α 1 β 2 α 2 | · · · | α 1 β m α 2 em P .

Então, temos que L ( G ) = L ( G ′ ) .

## Exemplo 2. Considere

tal que L ( G ′ ) = L ( G ) .

## Eliminação de produções inúteis

Seja G = ( V, Σ , P , S ) uma GLC. Uma variável A ∈ V é dita útil se existe pelo menos uma cadeia w ∈ L ( G ) tal que S ∗ ⇒ αAβ ∗ ⇒ w , com α, β ∈ ( V ∪ Σ) ∗ . Em outras palavras, uma variável é útil se ela é usada em pelo menos uma derivação de alguma cadeia. Uma variável que não é útil é dita inútil . Uma produção é inútil se ela contém pelo menos uma variável inútil.

Queremos eliminar produções inúteis pois elas não servem para gerar cadeias da gramática que ela gera. Por exemplo, seja

uma GLC.

Primeiramente computamos o conjunto Φ de símbolos geradores de G .

algoritmo computa Φ( G ) :=

- 1. Φ := ∅ ;
- 2. enquanto existir ( A → α ) ∈ P tal que α ∈ (Σ ∪ Φ) ∗ faça
- 3. Φ ← Φ ∪ { A }
- 4. devolva Φ.

Usando o Teorema 1, podemos obter uma nova GLC G ′ removendo a produção A → abBc e acrescentando as regras A → ababbAc | abbc . Assim,

O tempo gasto pelo algoritmo é O ( |P| · | V | ) se o número de símbolos em cada produção é constante. Em cada iteração, examinamos cada produção e o número total de iterações é | V | .

Se executarmos o algoritmo acima com a GLC do nosso exemplo, obteremos Φ = { S, A, B } e a gramática que é induzida por essas variáveis é

Depois de encontrar Φ, computamos o conjunto Ψ de variáveis atingíveis de G ′ a partir de S . Mais precisamente consideramos o digrafo D = (Φ , A ) onde

e determinamos Ψ := { A ∈ Φ : existe um caminho de S a A em D } . Note que se S ̸∈ Φ, então Ψ = ∅ .

<!-- image -->

Figura 2: Executando o segundo passo para o grafo G ′ , obtemos Ψ := { S, A } . Geramos uma GLC, G ′′ , que contém todas as produções de G em que todos as variáveis pertencem a Ψ: G ′′ := S → aS | A, A → a .

Oalgoritmo acima gasta tempo O |P| para construir o digrafo D quando o número de símbolos em cada produção é constante e O ( |P| + | V | ) para encontrar as variáveis alcançáveis por S usando nesse último caso algum algoritmo de busca tais como busca em profundidade e busca e largura. A construção acima nos permite concluir o seguinte resultado.

Teorema 2. Seja G uma GLC qualquer. Então, existe uma GLC equivalente a G que não possui nenhuma variável inútil.

Prova . Prova construtiva mas sendo os detalhes omitidos.

As produções úteis são aquelas que não contém variáveis inúteis.

## Eliminação de produções nulas

Em uma GLC, qualquer produção da forma

é chamada de produção nula .

Lema 3. Seja G uma GLC e S sua variável inicial. Existe uma GLC G ′ sem produções nulas, exceto eventualmente a produção S → ϵ , tal que L ( G ′ ) = L ( G ) .

̸

Aplicando a regra da prova do Lema 3 (são vários passos, verifique - primeiro eliminamos B → ϵ , depois C → ϵ e finalmente A → ϵ ), obtemos

Prova . ( Esboço ) A obtenção de G ′ é construtiva e é algorítmica. Primeiro, enquanto houver uma produção A → ϵ com A = S , para cada produção B → αAβ com α, β ∈ (Σ ∪ V ) ∗ , acrescente a produção B → αβ . Se α = β = ϵ , acrescente a regra B → ϵ a menos que esta regra tenha sido previamente removida. Repetimos esses passos até que eliminemos todas as produções nulas que não envolvam a variável inicial e obtemos a gramática G ′ . Note que L ( G ) = L ( G ′ ). □

## Exemplo 3. Seja a gramática

□

## Eliminação de produções unitárias

Em uma GLC G = ( V, Σ , P , S ), qualquer produção da forma

onde A, B ∈ V , é chamada de produção unitária .

Lema 4. Seja G uma GLC. Existe GLC G ′ sem produções unitárias tal que L ( G ′ ) = L ( G ) .

Prova . ( Esboço ) Semelhante à prova do Lema 3, construa uma gramática G ′ a partir de G acrescentando produções A → γ sempre que tivermos A → B e B → γ . Se γ é uma variável, acrescente a regra A → γ a menos que esta regra tenha sido removida anteriormente. Repita esse processo até que não existam mais produções unitárias. Note que L ( G ) = L ( G ′ ). □

## Exemplo 4. Seja a gramática

Usando a regra da prova do Lema 4 (elimine nessa ordem as regras S → B , S → A , B → A e a → B ) obtemos

removendo as produções unitárias.

## Exercícios

- 1. Mostre que as gramáticas

e

são equivalentes.

- 2. Elimine todas as produções inúteis da gramática

Qual é a linguagem gerada pela gramática?

- 3. Elimine todas as produções nulas da gramática

- 4. Elimine todas as produções nulas, unitárias e inúteis da gramática

Qual é a linguagem gerada pela gramática?

- 5. Dê um exemplo de uma situação em que a eliminação de produções nulas introduz produções unitárias que não existiam antes. Em seguida, argumente sobre a ordem em que os procedimentos de eliminação de produções nulas e de produções unitárias devem ser aplicados se queremos uma gramática sem produções nulas e sem produções unitárias.
- 6. Prove que se uma gramática não possui nenhuma produção nula e nenhuma produção unitária, então a eliminação de produções inúteis, pela construção dada neste capítulo, não introduz nenhuma produção nula nem unitária. Em seguida, argumente sobre a ordem em que os procedimentos de eliminação de produções nulas, unitárias e inúteis devem ser aplicados se não queremos esses tipos de produção em nossa gramática.

- 7. Suponha que uma GLC G tenha uma produção da forma

Prove que se esta regra for substituída por

onde B é uma nova variável introduzida em G , então a gramática resultante será equivalente à original.

- 8. Considere o procedimento de dois passos, dado neste capítulo, para eliminar produções inúteis. Inverta a ordem dos dois passos. Isto é, primeiro calcule o conjunto Ψ dos símbolos atingíveis e, em seguida, calcule o conjunto Φ dos símbolos geradores. Você acha que esta inversão de passos produz um procedimento correto para gerar uma gramática equivalente à original, mas sem produções inúteis? Se sim, prove que você está correto. Caso contrário, forneça um contraexemplo.

## Formas Normais

Em muitas aplicações é comum assumirmos que as produções de uma GLC's estão restritas a uma dada forma especial. Duas dessas formas úteis são a Forma Normal de Chomsky (FNC) e a Forma Normal de Greibach (FNG).

## Forma Normal de Chomsky

̸

Uma GLC G = ( V, Σ , P , S ) está na Forma Normal de Chomsky (FNC) se e somente se todas as produções de G são da forma A → BC ou A → a , onde A, B, C ∈ V e a ∈ Σ e A = S . Adicionalmente, permitimos a regra S → ϵ .

Exemplo 5. A gramática

está na FNC. Note que a linguagem L ( G ) gerada por G é exatamente

Teorema 3. Dada uma GLC G = ( V, Σ , P , S ) , há uma GLC G ′ na FNC com L ( G ′ ) = L ( G ) .

Prova . (esboço) A prova é construtiva. A gramática será modificada sem mudar a linguagem por ela gerada. Vamos acompanhar um exemplo para acompanhar essa transformação. Considere inicialmente a gramática

Passo 1. Crie uma variável inicial S ′ e a regra S ′ → S para garantir que a variável inicial não apareça do lado direito de alguma regra. Ficamos assim

com a gramática de nosso exemplo.

Passo 2. Elimine as transições nulas usando o Lema 3 e obtenha a gramática

que é equivalente à gramática de nosso exemplo.

Passo 3. Elimine as transições unitárias usando o Lema 4 e obtenha a gramática

Passo 4. As regras remanescentes indesejáveis da forma

onde k ≥ 3 e cada u i ∈ (Σ ∪ V ) são substituídas por k -1 novas regras

onde cada A i é uma nova variável. A gramática de nosso exemplo fica assim.

Passo 5. Para cada regra X → uv onde u ∈ Σ ou v ∈ Σ, substitua o elemento em Σ por uma variável e acrescente mais uma regra convertendo essa variável no símbolo em Σ. Assim, em nosso exemplo

que está na FNC e L ( G ′ ) = L ( G ).

□

Exemplo 6. Seja a GLC G := S → aSb | ϵ . Note que L ( G ) = { a n b n | n ∈ Z , n ≥ 0 } .

Passo 1

Passo 2

Passo 3

Passo 4

Passo 5

Exemplo 7. Seja G := S → ( S ) | SS | ϵ uma GLC. Note que L ( G ) é PARBAL definida em (1).

Passo 1

Passo 2

Passo 3

Passo 4

Passo 5

Exemplo 8. Seja a GLC

## Passo 1

## Passo 2

## Passo 3

```
S ′ → CBh | be | SABC | ABC | ϵ S → CBh | be | SABC | ABC A → aaD B → Sf | ggg | f C → cA | d D → be | SABC | ABC E → be.
```

## Passo 4

```
S ′ → CX 1 | be | SX 2 | AX 3 | ϵ S → CX 1 | be | SX 2 | AX 3 A → aX 4 B → Sf | gX 5 | f C → cA | d D → be | SX 2 | AX 3 E → be X 1 → Bh X 2 → AX 3 X 3 → BC X 4 → aD X 5 → gg.
```

## Passo 5

## Exercícios

1. Seja

```
S ′ → CX 1 | U 1 U 2 | SX 2 | AX 3 | ϵ S → CX 1 | U 1 U 2 | SX 2 | AX 3 A → U 3 X 4 B → SU 4 | U 6 X 5 | f C → U 5 A | d D → U 1 U 2 | SX 2 | AX 3 E → U 1 U 2 X 1 → BU 8 X 2 → AX 3 X 3 → BC X 4 → U 3 D X 5 → U 6 U 6 U 1 → b U 2 → e U 3 → a U 4 → f U 5 → c U 6 → g U 7 → d
```

U 8 → h

uma GLC. Forneça uma GLC G ′ na FNC tal que L ( G ′ ) = L ( G ).

- 2. Seja G uma gramática livre de contexto na FNC. Então, mostre que qualquer

cadeia w ∈ L ( G ) é derivada a partir do símbolo inicial de G com exatamente 2 · | w | -1 passos de derivação.

## Forma Normal de Greibach

Vide [Enc14]. Uma GLC G = ( V, Σ , P , S ) está na Forma Normal de Greibach (FNG) se a variável inicial nunca aparece do lado direito de uma regra e todas as produções de G são da forma S → ϵ ou

para algum k ∈ N , A, B 1 , . . . , B k ∈ V e a ∈ Σ. Note que k = 0 é permitido, o que implica que podemos ter produções da forma A → a .

Exemplo 9. A gramática

está na Forma Normal de Greibach. Note que a linguagem deste exemplo é PARBAL (1).

Nessa seção mostramos como transformar uma GLC qualquer em uma GLC na FNG. Para isso usamos o resultado obtido no próximo lema. Nessa seção nos referimos a uma produção com a variável A do lado esquerdo como produção -A .

e A → β 1 | β 2 | · · · | β s as demais produçõesA em uma GLC G . Considere G ′ uma gramática obtida a partir de G pela substituição de cada A → Aα ∈ A pelas produções

onde B é uma nova variável. Então, L ( G ′ ) = L ( G ) .

Prova . (esboço) Mostrar que L ( G ) ⊆ L ( G ′ ) e que L ( G ′ ) ⊆ L ( G ). Seja B o conjunto de todas as regras adicionadas após a remoção dos elementos em A para a obtenção de G ′ .

Seja G ′′ uma GLC que possui conjunto de produções de G e de G ′ . Temos então que os conjuntos de produções de G , G ′ e G ′′ são respectivamente P , ( P -A ) ∪B e P ∪ B . Logo,

Seja w uma cadeia arbitrária em L ( G ′′ ).

Queremos mostrar primeiramente que existe uma derivação de w em G ′′ que não usa regras em A . Então, suponha por contradição que toda derivação de w usa pelo menos uma regra em A . O Lema 2 garante existir uma derivação mais a esquerda de w . Considere a seguir aquela que usa a menor quantidade de vezes uma regra em A onde destacamos a última vez que uma dessas regras é utilizada:

Note que a sequência de derivações em destaque pode ser substituída por

que é uma derivação de w que usa menos vezes uma regra em A o que é uma contradição. Logo, existe uma derivação de w em G ′′ que não usa regras em A . Isto implica que L ( G ′′ ) ⊆ L ( G ′ ). Segue de (2) que L ( G ) ⊆ L ( G ′′ ) ⊆ L ( G ′ ) o que implica que L ( G ) ⊆ L ( G ′ ).

′′

Vamos mostrar agora que existe uma derivação de w em G que não usa regras em B . Suponha por contradição que toda derivação de w usa pelo menos uma regra em B . O Lema 2 garante existir uma derivação mais a direita de w . Considere uma delas em n passos que usa a menor quantidade de vezes uma regra em B pode ser esboçada abaixo:

onde v ∈ Σ ∗ . Note que a sequência de derivações em (4) pode ser substituída por

uAv ⇒ uβAα k +1 v ⇒ uAα k α k +1 v ⇒ . . . ⇒ uAα 1 . . . α k α k +1 v ⇒ uβα 1 . . . α k α k +1 v

que é uma derivação a direita em n passos de w que usa menos vezes uma regra em B o que é uma contradição. Logo, existe uma derivação de w em G ′′ que não usa regras em B . Isto implica que L ( G ′′ ) ⊆ L ( G ). Segue de (2) que L ( G ′ ) ⊆ L ( G ′′ ) ⊆ L ( G ) o que implica que L ( G ) ⊆ L ( G ′ ). □

Voltamos agora à nossa transformação de uma GLC qualquer em uma FNG na FNG.

Teorema 4. Dada qualquer GLC G , há uma GLC G ′ na FNG tal que L ( G ′ ) = L ( G ) .

Prova . (esboço) Como sempre, não faremos uma prova formal do resultado. Mostramos simplesmente uma construção que transforma uma GLC qualquer em uma na FNG. Explicamos cada passo no caso geral e no caso particular de um exemplo utilizado para exemplificar a construção. A justificativa dos passos fica por conta dos resultados estudados anteriormente e da intuição.

Passo 1. Dada uma GCL, obtenha a gramática na FNC.

Passo 2. Estabeleça uma ordenação das variáveis da GLC obtida no Passo 1.

Suponha então que a GLC obtida após o Passo 2 seja

Passo 3. Esse passo modifica as produções da GLC de modo que as produções resultantes sejam tais que se A i → A j α é uma produção, então j &gt; i . Começando com A 1 e procedendo até A m , usamos o seguinte procedimento indutivo explicado a seguir.

Assuma que as produções já tenham sido modificadas de tal modo que, para todo 1 ≤ i &lt; k , se A i → A j α é uma produção, então j &gt; i . Então, modificamos as produçõesA k .

Se A k → A j α é uma produção com j &lt; k , nós geramos um novo conjunto de produções que substitui o lado direito de A k → A j α pelo lado direito das produçõesA j usando o Lema 1. Repetindo este processo, no máximo, k -1 vezes, para cada produção A k → A j α , com j &lt; k , nós obtemos produções da forma A k → A l α , com l ≥ k .

No nosso exemplo, modificaríamos primeiro a produção

A → A A

Em seguida, nós substituímos as produções com l = k através da introdução de um novo variável B k como explicado no enunciado do Lema 5.

O resultado do passo anterior é um conjunto de produções da forma

Assim, no nosso exemplo a GLD ficaria assim.

substituindo-a por

e depois por

obtendo a GLD

que podemos escrever

```
A 0 → A 2 A 3 A 1 → A 2 A 3 A 2 → A 3 A 1 | b, A 3 → bA 3 A 2 | a | bA 3 A 2 B 3 | aB 3 B 3 → A 1 A 3 A 2 | A 1 A 3 A 2 B 3 .
```

As observações a seguir valem para o nosso mas, mais forte do que isto, como consequência do método utilizado, vale para qualquer gramática.

Passo 3. Note que o símbolo mais à esquerda do lado direito de qualquer produçãoA m deve ser um símbolo do alfabeto. O símbolo mais à esquerda do lado direito de qualquer produçãoA m -1 deve ser A m ou um elemento de Σ. Quando ele for A m , nós podemos gerar novas produçõesA m -1 substituindo A m pelo lado direito das produçõesA m de acordo com o Lema 1. Cada uma destas novas produções possui lado direito começando com um símbolo de Σ. Logo, podemos repetir o mesmo procedimento para A m -2 , . . . , A 2 , A 1 , nesta ordem, até que o lado direito de cada produçãoA i comece com um elemento em Σ. O resultado é um conjunto de produções da forma

com a ∈ Σ e γ ∈ ( V ∪ Σ ∪ { B 1 , . . . , B i -1 } ) ∗ . Note que o lado direito de cada B i pode começar com um variável do tipo A i . Assim, em nosso exemplo, obtemos a gramática

```
A 0 → bA 3 A 2 A 1 A 3 | bA 3 A 2 B 3 A 1 A 3 | aA 1 A 3 | aB 3 A 1 A 3 | bA 3 A 1 → bA 3 A 2 A 1 A 3 | bA 3 A 2 B 3 A 1 A 3 | aA 1 A 3 | aB 3 A 1 A 3 | bA 3 A 2 → bA 3 A 2 A 1 | bA 3 A 2 B 3 A 1 | aA 1 | aB 3 A 1 | b A 3 → bA 3 A 2 | bA 3 A 2 B 3 | a | aB 3 B 3 → A 1 A 3 A 2 | A 1 A 3 A 2 B 3 .
```

Como todas as produçõesB j possuem lados direitos que iniciam com um símbolo do alfabeto ou um variável A i . Logo, uma aplicação a mais do Lema 1 para cada produçãoB j completa a construção da gramática G ′ na FNG. Assim, no nosso exemplo, temos

```
A 0 → bA 3 A 2 A 1 A 3 | bA 3 A 2 B 3 A 1 A 3 | aA 1 A 3 | aB 3 A 1 A 3 | bA 3 A 1 → bA 3 A 2 A 1 A 3 | bA 3 A 2 B 3 A 1 A 3 | aA 1 A 3 | aB 3 A 1 A 3 | bA 3 A 2 → bA 3 A 2 A 1 | bA 3 A 2 B 3 A 1 | aA 1 | aB 3 A 1 | b A 3 → bA 3 A 2 | bA 3 A 2 B 3 | a | aB 3 B 3 → bA 3 A 2 A 1 A 3 A 3 A 2 | bA 3 A 2 B 3 A 1 A 3 A 3 A 2 | aA 1 A 3 A 3 A 2 | aB 3 A 1 A 3 A 3 A 2 | bA 3 A 3 A 2 | bA 3 A 2 A 1 A 3 A 3 A 2 B 3 | bA 3 A 2 B 3 A 1 A 3 A 3 A 2 B 3 | aA 1 A 3 A 3 A 2 B 3 | aB 3 A 1 A 3 A 3 A 2 B 3 | bA 3 A 3 A 2 B 3 .
```

□

## Exercícios

- 1. Seja
- 4. Dada a GLD

uma GLC. Forneça uma GLC G ′ na FNG tal que L ( G ′ ) = L ( G ).

- 2. Seja G uma gramática livre de contexto na FNG. Então, mostre que qualquer cadeia w ∈ L ( G ) é derivada a partir do símbolo inicial de G com exatamente | w | -1 passos de derivação.
- 3. Construa uma gramática livre de contexto que gere a linguagem

5.

encontre uma GLC sem variáveis e produções inúteis.

encontre uma GLC equivalente, onde o símbolo reservado S não aparece do lado direito das produções e S → ϵ é a única produção nula.

## 6. Considere a GLC

determine a linguagem gerada por essa gramática.

- 7. Encontre uma GLC sem varíaveis nem produções inúteis equivalente a GLC

Construa uma GLC equivalente sem variáveis nem produções inúteis.

- 8. Considere a GLC

## 9. Considere a GLC

Descreva informalmente quem é L ( G ) e encontre uma gramática equivalente a G , na FNC.

## 10. Considere a GLC

Descreva informalmente quem é L ( G ) e encontre uma gramática equivalente a G, escrita na FNG.

## Referências Bibliográficas

[Enc14] Wikipedia The Free Encyclopedia. Greibach normal form. http://en.wikipedia.org/wiki/Greibach normal form, March 2014.