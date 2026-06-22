## Preliminares

## Introdução

Neste curso, abordamos principalmente, mas não exclusivamente, os conteúdos encontrados sobre Computabilidade nos livros clássicos de referência, como Introduction to Automata Theory, Languages, and Computation de Hopcroft e Ullman [HU01], Introduction to the Theory of Computation de Sipser [Sip07] ou suas versões traduzidas, e Linguagens Formais e Autônomos de Menezes [Men97]. Esses textos, fundamentais para a teoria da computação, refletem a evolução da área desde seus primeiros trabalhos nos anos 1950 e 1960, quando os pioneiros como Alan Turing [Wik25a], John von Neumann [Wik25b] e outros estabeleceram as bases da computação moderna. Os assuntos gerais são abordados em todas essas obras, porém a notação não é padronizada entre elas - ou seja, cada autor adota uma notação específica que pode diferir das demais.

Além disso, as definições e resultados apresentados, embora equivalentes em termos de conteúdo, podem ser estruturados de maneira diferente. Por exemplo, o que é tratado como uma consequência em um livro pode ser uma definição em outro. Como resultado, optamos por explicitar, nestas notas de aula, as notações e definições que utilizaremos ao longo do curso, a fim de proporcionar maior clareza e coesão. A diversidade de abordagens entre os textos clássicos reflete a riqueza da teoria da computação, que evoluiu de diferentes tradições e escolas de pensamento ao longo do tempo, adaptando-se a novas descobertas e aplicações.

Sugestões e críticas são bem-vindas, e erros encontrados devem ser apontados para que possamos aprimorar o material continuamente.

Este curso tem como pré-requisito a disciplina Fundamentos da Teoria da Com- putação , mais especificamente os tópicos relativos a conjuntos e métodos de prova, que são abordados implicitamente ao longo das aulas. Durante o curso, mas não nestas notas de aula, faremos uma breve revisão desses conceitos fundamentais. Caso o aluno perceba lacunas no seu conhecimento, será necessário realizar um estudo extra para reforçar os conceitos aprendidos naquela disciplina.

Além disso, aplicaremos conceitos de programação e teoria dos grafos, cuja cobertura necessária para este curso será brevemente abordada e considerada suficiente para a compreensão dos tópicos a serem explorados.

Umdos aspectos que a teoria da computação está interessada e que abordamos neste curso é a computabilidade , que estuda a dificuldade intrínseca de resolver um dado problema. O termo 'dificuldade'é aqui utilizado de forma propositalmente vaga, mas será formalizado nas próximas aulas, com a classificação de problemas segundo um critério bem definido. O termo 'problema'também é vago, mas usaremos, para sua definição, conjuntos de cadeias de caracteres. Por isso, nas próximas seções desta aula, dedicamo-nos à revisão e à associação de cadeias de símbolos a problemas, que chamaremos de linguagens como sinônimo.

## Alfabetos e cadeias

Um alfabeto é um conjunto finito e não-vazio de elementos chamados símbolos . Uma cadeia sobre um alfabeto Σ é uma sequência finita de símbolos pertencentes a Σ. O comprimento de uma cadeia x é a quantidade de símbolos de x e é representado por | x | . Há uma única cadeia de comprimento 0 (zero) sobre qualquer alfabeto, a qual é denominada cadeia vazia , representada pelo símbolo ε . Portanto, | ε | = 0.

Se a é um símbolo e x uma cadeia, denotamos por | x | a o número de ocorrências do símbolo a em x . Portanto, temos que ∑ a | x | a = | x | . O i -ésimo símbolo de x é denotado por x i . Se | x | = n , também escrevemos x 1 x 2 . . . x n para denotar a cadeia x .

Se x e y são cadeias de comprimentos n e m , respectivamente, escrevemos xy ou x · y para denotar a cadeia x 1 . . . x n y 1 . . . y m , que é a concatenação das cadeias x e y . Dizemos que duas cadeias x e y são iguais se | x | = | y | e x i = y i para todo i .

Usando essas definições, podemos demonstrar as seguintes propriedades básicas sobre a concatenação de cadeias.

Propriedade 1. [Propriedades básicas da concatenação de cadeias] Sejam x , y , e z cadeias. As seguintes propriedades são válidas:

P1.1 Identidade : εx = xε = x .

Seja a um símbolo de algum alfabeto e n ∈ N . Definimos:

Similarmente, se x é uma cadeia, temos:

Denotamos por | x | a a quantidade de ocorrências do símbolo a em x .

Sejam x, u, v, w cadeias tais que x = uvw . Dizemos que:

- · u é um prefixo de x ,
- · v é uma subcadeia de x ,
- · w é um sufixo de x .

̸

Além disso, se u = ε e u = x , então dizemos que u é um prefixo próprio de x . Analogamente, definimos sufixo próprio e subcadeia própria .

̸

Se x = x 1 x 2 . . . x n é uma cadeia, o reverso de x é a cadeia

Ou seja, x R é obtido escrevendo os símbolos de x na ordem inversa, isto é, x R = x n x n -1 . . . x 1 .

̸

Seja Σ um alfabeto e ⪯ uma ordem total em Σ. Se a, b ∈ Σ, a = b e a ⪯ b , denotamos a ≺ b . Seja S um conjunto de cadeias sobre Σ. Dizemos que a relação ⪯ L é a ordem lexicográfica em S se:

Ou seja, a ordem lexicográfica de cadeias é a mesma que a ordenação familiar do dicionário, exceto que as cadeias mais curtas precedem as mais longas. Por conseguinte, a ordenação lexicográfica de todas as cadeias sobre o alfabeto { 0 , 1 } , considerando que 0 ≺ 1 é: ε, 0 , 1 , 00 , 01 , 10 , 11 , 000 , . . . .

## Linguagens

Seja Σ um alfabeto. O conjunto de todas as cadeias formadas por símbolos de elementos de Σ (inclusive a cadeia vazia) é denotada por Σ ∗ . Uma linguagem sobre Σ é um subconjunto de Σ ∗ .

Sejam A e B linguagens sobre um alfabeto Σ. Definimos a linguagem A R = { x ∈ Σ ∗ : x R ∈ A } . Também definimos as seguintes linguagens que resultam das operações de:

- · União : A ∪ B = { x ∈ Σ ∗ : x ∈ A ou x ∈ B } .
- · Intersecção : A ∩ B = { x ∈ Σ ∗ : x ∈ A e x ∈ B } .
- · Complemento em Σ ∗ : Σ ∗ -A = A = { x ∈ Σ ∗ : x ̸∈ A } .
- · Concatenação : AB = A · B = { xy ∈ Σ ∗ : x ∈ A e y ∈ B } .

Para n ∈ N , n &gt; 0, a n -ésima potência de A é

A estrela de uma linguagem A e a linguagem A + são as linguagens

(perceba que esta definição é compatível com a definição dada acima de Σ ∗ .)

## Exercícios

- Considere as seguintes linguagens: A = { x ∈ { 0 , 1 } ∗ : | x | 0 ≥ 7 } B = { x ∈ { 0 , 1 } ∗ : | x | 0 %3 = 0 } C = { x ∈ { 0 , 1 } ∗ : | x | 0 = 2 | x | 1 } . Escreva em python 1. uma função que recebe x e decida se x ∈ A . def q1 (x): conte = 0 i = len(x)-1 while i &gt;= 0: conte += x[i] == '0' i -= 1 return conte &gt;= 7 2. uma função que recebe x e decida se x ∈ ( A ∪ B ). 3. uma função que recebe x e decida se x ∈ C . 4. uma função que recebe x e decida se x ∈ ( A -C ) + . 5. uma função que recebe x e decida se x ∈ ABC . 6. um programa que imprime x as 10 menores cadeias na ordem lexicográfica de A . 7. um programa que imprime x as 10 menores cadeias na ordem lexicográfica de A ∪ B . 8. um programa que imprime x as 10 menores na ordem lexicográfica de ABC . ∪
- 9. um programa que imprime x as 10 menores na ordem lexicográfica de ABC ( A ∪ B ).

Propriedade 2 (Concatenação de linguagens) . Sejam A , B e C linguagens sobre Σ e n ∈ N .

P2.1 A linguagem { ε } é a identidade para a operação de concatenação:

Prova . Para mostrar que A = { ε } A = A { ε } , basta mostrar

- ( i ) A ⊆ { ε } A ,
- ( ii ) { ε } A ⊆ A { ε } e
- ( iii ) A { ε } ⊆ A .

Fazemos isto a seguir.

Seja x uma cadeia arbitrária em A . Por P1.1, temos que x = εx . Logo, x ∈ { ε } A . Segue que A ⊆ { ε } A . Usando similares argumentos, mostramos que { ε } A ⊆ A { ε } e que A { ε } ⊆ A . Segue que A = { ε } A = A { ε } . □

## P2.2 A + = A · A ∗ .

Prova . Para provar a propriedade basta mostrar que A + ⊆ A · A ∗ e que A · A ∗ ⊆ A + .

Seja x ∈ A + . Por definição, temos que x ∈ A n = AA n -1 para algum n &gt; 0. Logo, existem cadeias u ∈ A e v ∈ A n -1 tais que x = uv . Como n ≥ 1, temos que n -1 ≥ 0, o que implica, sendo v ∈ A n -1 , que v ∈ A ∗ . Logo, x = uv ∈ AA ∗ . Segue que A + ⊆ A · A ∗ .

Seja y ∈ A · A ∗ . Por definição, existem cadeias u e v tais que y = u · v , u ∈ A e v ∈ A ∗ . Como v ∈ A ∗ , existe um inteiro n ≥ 0 tal que v ∈ A n . Logo, y = uv ∈ AA n = A n +1 ⊆ A + . Segue que A · A ∗ ⊆ A + . □

## P2.3 ( AB ) C = A ( BC ).

Prova . Suponha que x é uma cadeia em ( AB ) C . Então, existem cadeias u, v, w tais que x = ( uv ) w , u ∈ A , v ∈ B e w ∈ C . Segue de P1.2 que x = ( uv ) w = u ( vw ) ∈ A ( BC ). Logo, temos que ( AB ) C ⊆ A ( BC ).

Similarmente, usando raciocínio análogo, temos que A ( BC ) ⊆ ( AB ) C .

Das afirmações acima, concluímos que ( AB ) C = A ( BC

). □

P2.4 Para qualquer inteiro n ≥ 1, temos que A n = A n -1 A .

Prova . A prova é por indução em n .

Base : Por definição e P2.1, temos que A 1 = AA 0 = A { ε } = { ε } A = A 0 A . Portanto, vale a propriedade para n = 1.

Passo de Indução : Suponha que A n -1 = A n -2 A para n &gt; 1. Usando a definição, a hipótese de indução e P2.3, temos que A n = AA n -1 = A ( A n -2 A ) = ( AA n -2 ) A = A n -1 A . Portanto, também vale a propriedade para n &gt; 1.

□

P2.5 Seja n ∈ N . Para i ∈ N , i ≤ n , temos que A n = A n -i · A i .

Prova . A prova é por indução em i .

Base : Por P2.1 e por definição, temos que A n = A n { ε } = A n A 0 = A n -0 A 0 . Portanto, vale a propriedade para i = 0.

Passo de indução : Suponha que A n = A n -( i -1) · A i -1 e i &gt; 0. Por hipótese de indução, P2.4 e P2.3, temos que A n = A n -( i -1) A i -1 = ( A n -i A ) A i -1 = A n -i ( AA i -1 ) = A n -i A i . Portanto, também vale a propriedade para i &gt; 0. □

## P2.6 A + = A ∗ A .

## P2.7 A linguagem vazia ∅ é dita 'aniquiladora' para a operação de concatenação, pois

Prova . Mostramos que A ∅ = ∅ . A prova de que ∅ A = ∅ é similar.

Suponha por contradição que A ∅ ̸ = ∅ . Logo, existe uma cadeia uv ∈ A ∅ , onde u ∈ A e v ∈ ∅ . Mas v ∈ ∅ é um absurdo pois não existem elementos em ∅ . Logo, A ∅ = ∅ .

□

P2.8 A operação de concatenação é distributiva com respeito à união:

```
P2.9 A = A A . P2.10 A ∗ = A ∗∗ . Denotamos ( A ∗ ) ∗ por A ∗∗ . P2.11 ∅ ∗ = { ε } .
```

## Problemas e linguagens

Neste curso, tratamos principalmente dos chamados problemas de decisão. Um problema de decisão é aquele cuja resposta é sempre 'sim' ( S ) ou 'não' ( N ). Para especificar um problema de decisão, nós devemos especificar o conjunto A de todas as possíveis entradas do problema e o conjunto B ⊆ A de todas as entradas cujas respostas são 'sim'. Por exemplo, para especificar o problema de decidir se um dado número inteiro é primo, definimos o conjunto A como sendo o conjunto de todos os inteiros e o conjunto B como sendo o conjunto de todos os números inteiros que são primos. À primeira vista, a ideia de considerar apenas os problemas de decisão pode parecer bastante restrita, mas a verdade é que esses problemas são suficientes para se estudar as principais questões de Computabilidade e Complexidade, duas das três principais subáreas da Teoria da Computação.

Surpreendentemente, os termos 'problema de decisão' e 'linguagem' possuem uma forte relação pois, qualquer problema de decisão pode ser visto como sendo o problema de decidir se uma dada cadeia pertence a uma dada linguagem. Em outras palavras, a entrada de um problema de um problema de decisão pode ser codificada por uma cadeia sobre um alfabeto Σ e o conjunto das entradas para as quais a resposta do problema de decisão é S é uma linguagem que é subconjunto de Σ ∗ .

## Exercícios

- 1. Defina um alfabeto Σ e duas cadeias x e y sobre Σ tais que xy = yx (isto é, mostre que a operação de concatenação de (duas) cadeias não é comutativa).

̸

- 2. Seja x = abaab uma cadeia sobre o alfabeto { a, b } . Liste todos os prefixos, sufixos e subcadeias de x . Quantos prefixos e sufixos próprios x possui?

Solução . Prefixos: ϵ , a , ab , aba , abaa , abaab .

Sufixos: ϵ , b , ab , aab , baab , abaab .

Subcadeias: ϵ , a , ab , aba , abaa , abaab . b , ba , baa , baab , aa , aab .

Considerando próprios os prefixos e sufixos conforme a definição, temos: 7 cadeias.

- 3. Quantas subcadeias há uma cadeia com n símbolos?

Solução . Considerando uma cadeia com todos os símbolos diferentes, há ( n + n +1) / 2 subcadeias.

- 4. Sejam A = { ε, a, ba } e B = { c, bc, cca } duas linguagens sobre { a, b, c } . Calcule A 2 , B 2 e AB . É verdade que A ⊆ A 2 ? É verdade que B ⊆ B 2 ? Discuta sobre isto.
- Solução . A 2 = { ϵ, a, ba, aa, aba, baa, baba } ; e como podemos verificar, A ⊆ A 2 . B 2 = { cc, cbc, ccca, bcc, bcbc, bccca, ccac, ccabc, ccacca } e portanto, B ̸⊆ B 2 . Podemos verificar que X ⊆ X 2 para um conjunto de cadeias X se e somente se ϵ ∈ X e por isso A ⊆ A 2 mas B ̸⊆ B 2 . Finalmente temos AB = { c, ac, bc, abc, bac, cca, acca, baba, bacca } .

̸

- 5. Seja A = ∅ uma linguagem. Motivado pelo exercício anterior, mostre que A ⊆ A 2 se e somente se ε ∈ A .

Solução . Primeiro verificamos que se ϵ ∈ A = { x 1 , x 2 , . . . , x n } , x i = ϵx i ∈ A 2 para cada i . Logo A ⊆ A 2 .

Suponha agora que ϵ ̸∈ A e suponha que n &gt; 1 é uma cadeia x de menor comprimento em A . Nesse caso, a menor cadeia de A 2 deve ser obrigatoriamente igual a 2 n . Segue que 2 n &gt; n o que implica que x ̸∈ A 2 e nesse caso A ̸⊆ A 2 .

- 6. Seja A uma linguagem sobre um alfabeto Σ. Mostre que, para quaisquer inteiros n e m , com n, m ≥ 0, A n A m = A n + m .

Solução . Prova é por indução em n .

Para n &gt; 0, temos

onde, a primeira e a última igualdades decorrem da definição de pot` encia; a segunda igualdade decorre da propriedade associativa e a terceira igualdade decorre da HI. Portanto, a afirmação também vale para n &gt; 0.

- 7. Mostre que A ∗ -A + = { ε } para qualquer linguagem A , ou mostre um contraexemplo de que a afirmação não é verdadeira.
- 8. Seja A uma linguagem sobre um alfabeto Σ. Mostre que A ∗ A ∗ = A ∗ .
- 9. Seja A uma linguagem sobre um alfabeto Σ. Mostre que A ∗∗ = ( A ∗ ) ∗ = A ∗ .
- 10. Seja A uma linguagem sobre um alfabeto Σ. Mostre que A ∗ = { ε } ∪ AA ∗ = { ε } ∪ A ∗ A .
- 11. Mostre que ∅ ∗ = { ε } .
- 12. Seja A uma linguagem sobre um alfabeto Σ. Nós dizemos que A é transitiva se AA ⊆ A e reflexiva se ε ∈ A . Mostre que se A é uma linguagem transitiva e reflexiva, então A ∗ ⊆ A .
- 13. Dado qualquer alfabeto Σ, prove que, para quaisquer duas cadeias x e y sobre Σ, xy = yx se e somente se existir uma cadeia w sobre Σ tal que x = w m e y = w n , onde m e n são inteiros não-negativos.
- 14. Sejam A e B linguagens tais que | A | = n e | B | = m . Discuta como determinar | A × B | .
- 15. Sejam A e B linguagens sobre um mesmo alfabeto. Determine as seguintes linguagens em função de A R e B R .
- (a) ( A · B ) R ,
- (b) ( A ∪ B ) R ,
- (c) ( A ∩ B ) R ,
- (d) ( A ) R ,
- (e) ( A ∗ ) R .

Demonstre formalmente os resultados obtidos.

- 16. Mostre por indução em n ∈ N que, para n ≥ 2 e as linguagens A 1 , A 2 , . . . , A n sobre um mesmo alfabeto, vale que

## Referências Bibliográficas

[HU01] John E. Hopcroft and Jeffrey D. Ullman. Introduction to Automata The- ory, Languages, and Computation . Addison-Wesley, 2001.

[Men97] . Editora Sagra-

Paulo Blauth Menezes. Linguagens Formais e Autômatos Luzzatto, 1997.

[Sip07]

Michael Sipser. Introduction to the Theory of Computation . Thomson Course Technology, 2007.

[Wik25a] Wikipédia. Alan turing, 2025. Acesso em: 22 fev. 2025.

[Wik25b] Wikipédia. John von neumann, 2025. Acesso em: 22 fev. 2025.