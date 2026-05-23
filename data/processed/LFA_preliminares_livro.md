## Preliminares

## Introdu¸ c˜ ao

Neste curso, abordamos principalmente, mas n˜ ao exclusivamente, os conte´ udos encontrados sobre Computabilidade nos livros cl´ assicos de referˆ encia, como Introduction to Automata Theory, Languages, and Computation de Hopcroft e Ullman [HU01], Introduction to the Theory of Computation de Sipser [Sip07] ou suas vers˜ oes traduzidas, e Linguagens Formais e Autˆ onomos de Menezes [Men97]. Esses textos, fundamentais para a teoria da computa¸ c˜ ao, refletem a evolu¸ c˜ ao da ´ area desde seus primeiros trabalhos nos anos 1950 e 1960, quando os pioneiros como Alan Turing [Wik25a], John von Neumann [Wik25b] e outros estabeleceram as bases da computa¸ c˜ ao moderna. Os assuntos gerais s˜ ao abordados em todas essas obras, por´ em a nota¸ c˜ ao n˜ ao ´ e padronizada entre elas - ou seja, cada autor adota uma nota¸ c˜ ao espec´ ıfica que pode diferir das demais.

Al´ em disso, as defini¸ c˜ oes e resultados apresentados, embora equivalentes em termos de conte´ udo, podem ser estruturados de maneira diferente. Por exemplo, o que ´ e tratado como uma consequˆ encia em um livro pode ser uma defini¸ c˜ ao em outro. Como resultado, optamos por explicitar, nestas notas de aula, as nota¸ c˜ oes e defini¸ c˜ oes que utilizaremos ao longo do curso, a fim de proporcionar maior clareza e coes˜ ao. A diversidade de abordagens entre os textos cl´ assicos reflete a riqueza da teoria da computa¸ c˜ ao, que evoluiu de diferentes tradi¸ c˜ oes e escolas de pensamento ao longo do tempo, adaptando-se a novas descobertas e aplica¸ c˜ oes.

Sugest˜ oes e cr´ ıticas s˜ ao bem-vindas, e erros encontrados devem ser apontados para que possamos aprimorar o material continuamente.

Este curso tem como pr´ e-requisito a disciplina Fundamentos da Teoria da Com- puta¸ c˜ ao , mais especificamente os t´ opicos relativos a conjuntos e m´ etodos de prova, que s˜ ao abordados implicitamente ao longo das aulas. Durante o curso, mas n˜ ao nestas notas de aula, faremos uma breve revis˜ ao desses conceitos fundamentais. Caso o aluno perceba lacunas no seu conhecimento, ser´ a necess´ ario realizar um estudo extra para refor¸ car os conceitos aprendidos naquela disciplina.

Al´ em disso, aplicaremos conceitos de programa¸ c˜ ao e teoria dos grafos, cuja cobertura necess´ aria para este curso ser´ a brevemente abordada e considerada suficiente para a compreens˜ ao dos t´ opicos a serem explorados.

Umdos aspectos que a teoria da computa¸ c˜ ao est´ a interessada e que abordamos neste curso ´ e a computabilidade , que estuda a dificuldade intr´ ınseca de resolver um dado problema. O termo 'dificuldade'´ e aqui utilizado de forma propositalmente vaga, mas ser´ a formalizado nas pr´ oximas aulas, com a classifica¸ c˜ ao de problemas segundo um crit´ erio bem definido. O termo 'problema'tamb´ em ´ e vago, mas usaremos, para sua defini¸ c˜ ao, conjuntos de cadeias de caracteres. Por isso, nas pr´ oximas se¸ c˜ oes desta aula, dedicamo-nos ` a revis˜ ao e ` a associa¸ c˜ ao de cadeias de s´ ımbolos a problemas, que chamaremos de linguagens como sinˆ onimo.

## Alfabetos e cadeias

Um alfabeto ´ e um conjunto finito e n˜ ao-vazio de elementos chamados s´ ımbolos . Uma cadeia sobre um alfabeto Σ ´ e uma sequˆ encia finita de s´ ımbolos pertencentes a Σ. O comprimento de uma cadeia x ´ e a quantidade de s´ ımbolos de x e ´ e representado por | x | . H´ a uma ´ unica cadeia de comprimento 0 (zero) sobre qualquer alfabeto, a qual ´ e denominada cadeia vazia , representada pelo s´ ımbolo ε . Portanto, | ε | = 0.

Se a ´ e um s´ ımbolo e x uma cadeia, denotamos por | x | a o n´ umero de ocorrˆ encias do s´ ımbolo a em x . Portanto, temos que ∑ a | x | a = | x | . O i -´ esimo s´ ımbolo de x ´ e denotado por x i . Se | x | = n , tamb´ em escrevemos x 1 x 2 . . . x n para denotar a cadeia x .

Se x e y s˜ ao cadeias de comprimentos n e m , respectivamente, escrevemos xy ou x · y para denotar a cadeia x 1 . . . x n y 1 . . . y m , que ´ e a concatena¸ c˜ ao das cadeias x e y . Dizemos que duas cadeias x e y s˜ ao iguais se | x | = | y | e x i = y i para todo i .

Usando essas defini¸ c˜ oes, podemos demonstrar as seguintes propriedades b´ asicas sobre a concatena¸ c˜ ao de cadeias.

Propriedade 1. [Propriedades b´ asicas da concatena¸ c˜ ao de cadeias] Sejam x , y , e z cadeias. As seguintes propriedades s˜ ao v´ alidas:

P1.1 Identidade : εx = xε = x .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Seja a um s´ ımbolo de algum alfabeto e n ∈ N . Definimos:

<!-- formula-not-decoded -->

Similarmente, se x ´ e uma cadeia, temos:

<!-- formula-not-decoded -->

Denotamos por | x | a a quantidade de ocorrˆ encias do s´ ımbolo a em x .

Sejam x, u, v, w cadeias tais que x = uvw . Dizemos que:

- · u ´ e um prefixo de x ,
- · v ´ e uma subcadeia de x ,
- · w ´ e um sufixo de x .

̸

Al´ em disso, se u = ε e u = x , ent˜ ao dizemos que u ´ e um prefixo pr´ oprio de x . Analogamente, definimos sufixo pr´ oprio e subcadeia pr´ opria .

̸

Se x = x 1 x 2 . . . x n ´ e uma cadeia, o reverso de x ´ e a cadeia

<!-- formula-not-decoded -->

Ou seja, x R ´ e obtido escrevendo os s´ ımbolos de x na ordem inversa, isto ´ e, x R = x n x n -1 . . . x 1 .

̸

Seja Σ um alfabeto e ⪯ uma ordem total em Σ. Se a, b ∈ Σ, a = b e a ⪯ b , denotamos a ≺ b . Seja S um conjunto de cadeias sobre Σ. Dizemos que a rela¸ c˜ ao ⪯ L ´ e a ordem lexicogr´ afica em S se:

<!-- formula-not-decoded -->

Ou seja, a ordem lexicogr´ afica de cadeias ´ e a mesma que a ordena¸ c˜ ao familiar do dicion´ ario, exceto que as cadeias mais curtas precedem as mais longas. Por conseguinte, a ordena¸ c˜ ao lexicogr´ afica de todas as cadeias sobre o alfabeto { 0 , 1 } , considerando que 0 ≺ 1 ´ e: ε, 0 , 1 , 00 , 01 , 10 , 11 , 000 , . . . .

## Linguagens

Seja Σ um alfabeto. O conjunto de todas as cadeias formadas por s´ ımbolos de elementos de Σ (inclusive a cadeia vazia) ´ e denotada por Σ ∗ . Uma linguagem sobre Σ ´ e um subconjunto de Σ ∗ .

Sejam A e B linguagens sobre um alfabeto Σ. Definimos a linguagem A R = { x ∈ Σ ∗ : x R ∈ A } . Tamb´ em definimos as seguintes linguagens que resultam das opera¸ c˜ oes de:

- · Uni˜ ao : A ∪ B = { x ∈ Σ ∗ : x ∈ A ou x ∈ B } .
- · Intersec¸ c˜ ao : A ∩ B = { x ∈ Σ ∗ : x ∈ A e x ∈ B } .
- · Complemento em Σ ∗ : Σ ∗ -A = A = { x ∈ Σ ∗ : x ̸∈ A } .
- · Concatena¸ c˜ ao : AB = A · B = { xy ∈ Σ ∗ : x ∈ A e y ∈ B } .

Para n ∈ N , n &gt; 0, a n -´ esima potˆ encia de A ´ e

<!-- formula-not-decoded -->

A estrela de uma linguagem A e a linguagem A + s˜ ao as linguagens

<!-- formula-not-decoded -->

(perceba que esta defini¸ c˜ ao ´ e compat´ ıvel com a defini¸ c˜ ao dada acima de Σ ∗ .)

## Exerc´ ıcios

- Considere as seguintes linguagens: A = { x ∈ { 0 , 1 } ∗ : | x | 0 ≥ 7 } B = { x ∈ { 0 , 1 } ∗ : | x | 0 %3 = 0 } C = { x ∈ { 0 , 1 } ∗ : | x | 0 = 2 | x | 1 } . Escreva em python 1. uma fun¸ c˜ ao que recebe x e decida se x ∈ A . def q1 (x): conte = 0 i = len(x)-1 while i &gt;= 0: conte += x[i] == '0' i -= 1 return conte &gt;= 7 2. uma fun¸ c˜ ao que recebe x e decida se x ∈ ( A ∪ B ). 3. uma fun¸ c˜ ao que recebe x e decida se x ∈ C . 4. uma fun¸ c˜ ao que recebe x e decida se x ∈ ( A -C ) + . 5. uma fun¸ c˜ ao que recebe x e decida se x ∈ ABC . 6. um programa que imprime x as 10 menores cadeias na ordem lexicogr´ afica de A . 7. um programa que imprime x as 10 menores cadeias na ordem lexicogr´ afica de A ∪ B . 8. um programa que imprime x as 10 menores na ordem lexicogr´ afica de ABC . ∪
- 9. um programa que imprime x as 10 menores na ordem lexicogr´ afica de ABC ( A ∪ B ).

Propriedade 2 (Concatena¸ c˜ ao de linguagens) . Sejam A , B e C linguagens sobre Σ e n ∈ N .

P2.1 A linguagem { ε } ´ e a identidade para a opera¸ c˜ ao de concatena¸ c˜ ao:

<!-- formula-not-decoded -->

Prova . Para mostrar que A = { ε } A = A { ε } , basta mostrar

- ( i ) A ⊆ { ε } A ,
- ( ii ) { ε } A ⊆ A { ε } e
- ( iii ) A { ε } ⊆ A .

Fazemos isto a seguir.

Seja x uma cadeia arbitr´ aria em A . Por P1.1, temos que x = εx . Logo, x ∈ { ε } A . Segue que A ⊆ { ε } A . Usando similares argumentos, mostramos que { ε } A ⊆ A { ε } e que A { ε } ⊆ A . Segue que A = { ε } A = A { ε } . □

## P2.2 A + = A · A ∗ .

Prova . Para provar a propriedade basta mostrar que A + ⊆ A · A ∗ e que A · A ∗ ⊆ A + .

Seja x ∈ A + . Por defini¸ c˜ ao, temos que x ∈ A n = AA n -1 para algum n &gt; 0. Logo, existem cadeias u ∈ A e v ∈ A n -1 tais que x = uv . Como n ≥ 1, temos que n -1 ≥ 0, o que implica, sendo v ∈ A n -1 , que v ∈ A ∗ . Logo, x = uv ∈ AA ∗ . Segue que A + ⊆ A · A ∗ .

Seja y ∈ A · A ∗ . Por defini¸ c˜ ao, existem cadeias u e v tais que y = u · v , u ∈ A e v ∈ A ∗ . Como v ∈ A ∗ , existe um inteiro n ≥ 0 tal que v ∈ A n . Logo, y = uv ∈ AA n = A n +1 ⊆ A + . Segue que A · A ∗ ⊆ A + . □

## P2.3 ( AB ) C = A ( BC ).

Prova . Suponha que x ´ e uma cadeia em ( AB ) C . Ent˜ ao, existem cadeias u, v, w tais que x = ( uv ) w , u ∈ A , v ∈ B e w ∈ C . Segue de P1.2 que x = ( uv ) w = u ( vw ) ∈ A ( BC ). Logo, temos que ( AB ) C ⊆ A ( BC ).

Similarmente, usando racioc´ ınio an´ alogo, temos que A ( BC ) ⊆ ( AB ) C .

Das afirma¸ c˜ oes acima, conclu´ ımos que ( AB ) C = A ( BC

). □

P2.4 Para qualquer inteiro n ≥ 1, temos que A n = A n -1 A .

Prova . A prova ´ e por indu¸ c˜ ao em n .

Base : Por defini¸ c˜ ao e P2.1, temos que A 1 = AA 0 = A { ε } = { ε } A = A 0 A . Portanto, vale a propriedade para n = 1.

Passo de Indu¸ c˜ ao : Suponha que A n -1 = A n -2 A para n &gt; 1. Usando a defini¸ c˜ ao, a hip´ otese de indu¸ c˜ ao e P2.3, temos que A n = AA n -1 = A ( A n -2 A ) = ( AA n -2 ) A = A n -1 A . Portanto, tamb´ em vale a propriedade para n &gt; 1.

□

P2.5 Seja n ∈ N . Para i ∈ N , i ≤ n , temos que A n = A n -i · A i .

Prova . A prova ´ e por indu¸ c˜ ao em i .

Base : Por P2.1 e por defini¸ c˜ ao, temos que A n = A n { ε } = A n A 0 = A n -0 A 0 . Portanto, vale a propriedade para i = 0.

Passo de indu¸ c˜ ao : Suponha que A n = A n -( i -1) · A i -1 e i &gt; 0. Por hip´ otese de indu¸ c˜ ao, P2.4 e P2.3, temos que A n = A n -( i -1) A i -1 = ( A n -i A ) A i -1 = A n -i ( AA i -1 ) = A n -i A i . Portanto, tamb´ em vale a propriedade para i &gt; 0. □

## P2.6 A + = A ∗ A .

## P2.7 A linguagem vazia ∅ ´ e dita 'aniquiladora' para a opera¸ c˜ ao de concatena¸ c˜ ao, pois

<!-- formula-not-decoded -->

Prova . Mostramos que A ∅ = ∅ . A prova de que ∅ A = ∅ ´ e similar.

Suponha por contradi¸ c˜ ao que A ∅ ̸ = ∅ . Logo, existe uma cadeia uv ∈ A ∅ , onde u ∈ A e v ∈ ∅ . Mas v ∈ ∅ ´ e um absurdo pois n˜ ao existem elementos em ∅ . Logo, A ∅ = ∅ .

□

P2.8 A opera¸ c˜ ao de concatena¸ c˜ ao ´ e distributiva com respeito ` a uni˜ ao:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

```
P2.9 A = A A . P2.10 A ∗ = A ∗∗ . Denotamos ( A ∗ ) ∗ por A ∗∗ . P2.11 ∅ ∗ = { ε } .
```

## Problemas e linguagens

Neste curso, tratamos principalmente dos chamados problemas de decis˜ ao. Um problema de decis˜ ao ´ e aquele cuja resposta ´ e sempre 'sim' ( S ) ou 'n˜ ao' ( N ). Para especificar um problema de decis˜ ao, n´ os devemos especificar o conjunto A de todas as poss´ ıveis entradas do problema e o conjunto B ⊆ A de todas as entradas cujas respostas s˜ ao 'sim'. Por exemplo, para especificar o problema de decidir se um dado n´ umero inteiro ´ e primo, definimos o conjunto A como sendo o conjunto de todos os inteiros e o conjunto B como sendo o conjunto de todos os n´ umeros inteiros que s˜ ao primos. ` A primeira vista, a ideia de considerar apenas os problemas de decis˜ ao pode parecer bastante restrita, mas a verdade ´ e que esses problemas s˜ ao suficientes para se estudar as principais quest˜ oes de Computabilidade e Complexidade, duas das trˆ es principais sub´ areas da Teoria da Computa¸ c˜ ao.

Surpreendentemente, os termos 'problema de decis˜ ao' e 'linguagem' possuem uma forte rela¸ c˜ ao pois, qualquer problema de decis˜ ao pode ser visto como sendo o problema de decidir se uma dada cadeia pertence a uma dada linguagem. Em outras palavras, a entrada de um problema de um problema de decis˜ ao pode ser codificada por uma cadeia sobre um alfabeto Σ e o conjunto das entradas para as quais a resposta do problema de decis˜ ao ´ e S ´ e uma linguagem que ´ e subconjunto de Σ ∗ .

## Exerc´ ıcios

- 1. Defina um alfabeto Σ e duas cadeias x e y sobre Σ tais que xy = yx (isto ´ e, mostre que a opera¸ c˜ ao de concatena¸ c˜ ao de (duas) cadeias n˜ ao ´ e comutativa).

̸

<!-- formula-not-decoded -->

- 2. Seja x = abaab uma cadeia sobre o alfabeto { a, b } . Liste todos os prefixos, sufixos e subcadeias de x . Quantos prefixos e sufixos pr´ oprios x possui?

Solu¸ c˜ ao . Prefixos: ϵ , a , ab , aba , abaa , abaab .

Sufixos: ϵ , b , ab , aab , baab , abaab .

Subcadeias: ϵ , a , ab , aba , abaa , abaab . b , ba , baa , baab , aa , aab .

Considerando pr´ oprios os prefixos e sufixos conforme a defini¸ c˜ ao, temos: 7 cadeias.

- 3. Quantas subcadeias h´ a uma cadeia com n s´ ımbolos?

Solu¸ c˜ ao . Considerando uma cadeia com todos os s´ ımbolos diferentes, h´ a ( n + n +1) / 2 subcadeias.

- 4. Sejam A = { ε, a, ba } e B = { c, bc, cca } duas linguagens sobre { a, b, c } . Calcule A 2 , B 2 e AB . ´ E verdade que A ⊆ A 2 ? ´ E verdade que B ⊆ B 2 ? Discuta sobre isto.
- Solu¸ c˜ ao . A 2 = { ϵ, a, ba, aa, aba, baa, baba } ; e como podemos verificar, A ⊆ A 2 . B 2 = { cc, cbc, ccca, bcc, bcbc, bccca, ccac, ccabc, ccacca } e portanto, B ̸⊆ B 2 . Podemos verificar que X ⊆ X 2 para um conjunto de cadeias X se e somente se ϵ ∈ X e por isso A ⊆ A 2 mas B ̸⊆ B 2 . Finalmente temos AB = { c, ac, bc, abc, bac, cca, acca, baba, bacca } .

̸

- 5. Seja A = ∅ uma linguagem. Motivado pelo exerc´ ıcio anterior, mostre que A ⊆ A 2 se e somente se ε ∈ A .

Solu¸ c˜ ao . Primeiro verificamos que se ϵ ∈ A = { x 1 , x 2 , . . . , x n } , x i = ϵx i ∈ A 2 para cada i . Logo A ⊆ A 2 .

Suponha agora que ϵ ̸∈ A e suponha que n &gt; 1 ´ e uma cadeia x de menor comprimento em A . Nesse caso, a menor cadeia de A 2 deve ser obrigatoriamente igual a 2 n . Segue que 2 n &gt; n o que implica que x ̸∈ A 2 e nesse caso A ̸⊆ A 2 .

- 6. Seja A uma linguagem sobre um alfabeto Σ. Mostre que, para quaisquer inteiros n e m , com n, m ≥ 0, A n A m = A n + m .

Solu¸ c˜ ao . Prova ´ e por indu¸ c˜ ao em n .

<!-- formula-not-decoded -->

Para n &gt; 0, temos

<!-- formula-not-decoded -->

onde, a primeira e a ´ ultima igualdades decorrem da defini¸ c˜ ao de pot` encia; a segunda igualdade decorre da propriedade associativa e a terceira igualdade decorre da HI. Portanto, a afirma¸ c˜ ao tamb´ em vale para n &gt; 0.

- 7. Mostre que A ∗ -A + = { ε } para qualquer linguagem A , ou mostre um contraexemplo de que a afirma¸ c˜ ao n˜ ao ´ e verdadeira.
- 8. Seja A uma linguagem sobre um alfabeto Σ. Mostre que A ∗ A ∗ = A ∗ .
- 9. Seja A uma linguagem sobre um alfabeto Σ. Mostre que A ∗∗ = ( A ∗ ) ∗ = A ∗ .
- 10. Seja A uma linguagem sobre um alfabeto Σ. Mostre que A ∗ = { ε } ∪ AA ∗ = { ε } ∪ A ∗ A .
- 11. Mostre que ∅ ∗ = { ε } .
- 12. Seja A uma linguagem sobre um alfabeto Σ. N´ os dizemos que A ´ e transitiva se AA ⊆ A e reflexiva se ε ∈ A . Mostre que se A ´ e uma linguagem transitiva e reflexiva, ent˜ ao A ∗ ⊆ A .
- 13. Dado qualquer alfabeto Σ, prove que, para quaisquer duas cadeias x e y sobre Σ, xy = yx se e somente se existir uma cadeia w sobre Σ tal que x = w m e y = w n , onde m e n s˜ ao inteiros n˜ ao-negativos.
- 14. Sejam A e B linguagens tais que | A | = n e | B | = m . Discuta como determinar | A × B | .
- 15. Sejam A e B linguagens sobre um mesmo alfabeto. Determine as seguintes linguagens em fun¸ c˜ ao de A R e B R .
- (a) ( A · B ) R ,
- (b) ( A ∪ B ) R ,
- (c) ( A ∩ B ) R ,
- (d) ( A ) R ,
- (e) ( A ∗ ) R .

Demonstre formalmente os resultados obtidos.

- 16. Mostre por indu¸ c˜ ao em n ∈ N que, para n ≥ 2 e as linguagens A 1 , A 2 , . . . , A n sobre um mesmo alfabeto, vale que

<!-- formula-not-decoded -->

## Referˆ encias Bibliogr´ aficas

[HU01] John E. Hopcroft and Jeffrey D. Ullman. Introduction to Automata The- ory, Languages, and Computation . Addison-Wesley, 2001.

[Men97] . Editora Sagra-

Paulo Blauth Menezes. Linguagens Formais e Autˆ omatos Luzzatto, 1997.

[Sip07]

Michael Sipser. Introduction to the Theory of Computation . Thomson Course Technology, 2007.

[Wik25a] Wikip´ edia. Alan turing, 2025. Acesso em: 22 fev. 2025.

[Wik25b] Wikip´ edia. John von neumann, 2025. Acesso em: 22 fev. 2025.