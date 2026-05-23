## Autˆ omato Finito Determin´ ıstico

## Defini¸ c˜ ao

Um autˆ omato finito determin´ ıstico (AFD) M ´ e uma qu´ ıntupla

<!-- formula-not-decoded -->

onde:

- · Q : conjunto finito de estados ;
- · Σ: conjunto finito de s´ ımbolos -alfabeto de entrada ;
- · δ : Q × Σ → Q : fun¸ c˜ ao de transi¸ c˜ ao ;
- · q 0 ∈ Q : estado inicial ;
- · F ⊆ Q : estados finais ou de aceita¸ c˜ ao .

Seja x ∈ Σ ∗ , | x | = n . Definimos a fun¸ c˜ ao ∆ : Q × Σ ∗ → Q de computa¸ c˜ ao de M , onde

<!-- formula-not-decoded -->

Se p ´ e o estado inicial podemos escrever simplesmente ∆( x ) significando ∆( p, x ).

Dizemos que:

- 1. M aceita x se ∆( x ) ∈ F . Denotamos isso por M ( x ) = aceita ;

- 2. M rejeita x se ¬ ( M ( x ) = aceita ). Denotamos isso por M ( x ) = rejeita ;
- 3. M reconhece a linguagem L ( M ) = { x ∈ Σ ∗ : M ( x ) = aceita } ;
- 4. M e N s˜ ao equivalentes se L ( M ) = L ( N ). Denotamos isso por M ≡ N ;
- 5. a linguagem A ⊆ Σ ∗ ´ e dita regular se A = L ( M ) para algum AFD M .

## Representa¸ c˜ ao de um AFD

Podemos representamos um AFD neste texto usando

- 1. a defini¸ c˜ ao vista na se¸ c˜ ao anterior;
- 2. uma tabela representando a fun¸ c˜ ao de transi¸ c˜ ao;
- 3. um diagrama de transi¸ c˜ ao de estados.

## Exemplo 1. Considere o AFD

<!-- formula-not-decoded -->

onde δ ( q 0 , a ) = q 1 , δ ( q 1 , a ) = q 2 , δ ( q 2 , a ) = δ ( q 3 , a ) = q 3 , δ ( q, b ) = q para todo q ∈ Q .

Usando uma tabela como na Tabela 1, a 'seta' ` a esquerda de q 0 indica que q 0 ´ e o estado inicial e o F ao lado de q 3 indica que q 3 ´ e um estado final.

Tabela 1: Representa¸ c˜ ao de um AFD por uma tabela

|      |       | a   | b   |
|------|-------|-----|-----|
| →    | q 0   | q 1 | q 0 |
| M := | q 1   | q 2 | q 1 |
|      | q 2   | q 3 | q 2 |
|      | q 3 F | q 3 | q 3 |

Usando um diagrama de transi¸ c˜ ao de estados, a seta apontando para o q 0 indica que q 0 ´ e o estado inicial; e todo estado com c´ ırculo duplo ´ e um estado de aceita¸ c˜ ao. A Figura 1 mostra um diagrama de estados do Exemplo 1.

Figura 1: Diagrama de transi¸ c˜ ao de estados do AFD do Exemplo 1.

<!-- image -->

Exemplo 2. Descreva um AFD que reconhece a linguagem { x ∈ { 0 , 1 } ∗ : | x | ´ e par } .

Solu¸ c˜ ao:

Exemplo 3. Descreva um AFD que reconhece a linguagem

<!-- image -->

<!-- formula-not-decoded -->

Solu¸ c˜ ao:

O AFD descrito tem 5 estados q 0 , q 1 , q 2 , q 3 , q 4 , q 5 sobre o alfabeto { 0 , 1 } e fun¸ c˜ ao de transi¸ c˜ ao dada pela tabela

| δ     | 0   | 1   |
|-------|-----|-----|
| q 0   | q 1 | q 4 |
| q 1   | q 3 | q 2 |
| q 2 F | q 2 | q 2 |
| q 3   | q 3 | q 5 |
| q 4   | q 3 | q 4 |
| q 5 F | q 3 | q 4 |

Exemplo 4. Descreva um AFD que reconhece

{ x ∈ { 0 , · · · , 9 } ∗ : o n´ umero x em decimal ´ e um m´ ultiplo de 3 } .

## Solu¸ c˜ ao:

O AFD descrito possui 3 estados q 0 q 1 , q 2 sobre o alfabeto Σ = { 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 } , e fun¸ c˜ ao de transi¸ c˜ ao dada pela tabela

| δ     | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| q 0 F | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 |
| q 1   | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 |
| q 2   | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 |

<!-- image -->

## Implementa¸ c˜ ao

Um AFD pode ser visto como um formalismo reconhecedor para representar uma linguagem, ou seja, uma m´ aquina que aceita cadeias de uma determinada linguagem. Esse mecanismo pode ser implementado por um programa de computador. A seguir mostramos um exemplo em python que devolve True se uma cadeia s ´ e aceita pelo AFD do Exemplo 1; e devolve False caso contr´ ario.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

```
q = estadoInicial i = 0 n = len(s) while i < n: q = transicao[q][s[i]] i += 1
```

return q in estadoFinal

## Prova de que um AFD reconhece uma linguagem

Vejamos primeiramente o Exemplo 2 e provamos o seguinte invariante.

Invariante 1. Seja x ∈ Σ ∗ , n = | x | . Ent˜ ao,

<!-- formula-not-decoded -->

Prova . A prova ´ e por indu¸ c˜ ao em n = | x | .

Suponha que n = 0. Nesse caso, x = ϵ . Como ∆( ϵ ) = q 0 e | ϵ | ´ e par, temos que nesse caso vale o invariante.

Suponha ent˜ ao que n &gt; 0. Por hip´ otese de indu¸ c˜ ao, temos que

<!-- formula-not-decoded -->

Se | x | ´ e par, | y | ´ e ´ ımpar o que implica, por HI que ∆( y ) = q 1 e, portanto, ∆( x ) = δ (∆( y ) , x n ) = δ ( q 1 , x n ) = q 0 ; similarmente, ∆( x ) = q 1 se | x | ´ e ´ ımpar. Logo, vale o invariante para n &gt; 0.

□

Desde que F = { q 0 } , segue do invariante acima mostra que M aceita somente as cadeias de comprimento par.

## Seja o AFD

<!-- image -->

Esse AFD reconhece a linguagem { x ∈ { 0 , 1 } ∗ : x come¸ ca ou termina com 01 } . Para mostrar que isto ´ e verdade basta mostrar o seguinte invariante.

Invariante 2. Seja x ∈ { 0 , 1 } ∗ . Ent˜ ao,

<!-- formula-not-decoded -->

Prova . A prova ´ e por indu¸ c˜ ao em n = | x | .

Suponha que n ≤ 2. Nesse caso, x ∈ { ϵ, 0 , 1 , 00 , 01 , 10 , 11 } . Verificamos que o invariante vale para cada valor poss´ ıvel para x . Portanto, vale o invariante para n ≤ 2.

Suponha ent˜ ao que n &gt; 2. Por hip´ otese de indu¸ c˜ ao, temos que

<!-- formula-not-decoded -->

̸

(Note que y = ϵ , y = 0 e y = 1 porque | y | ≥ 2.)

̸

̸

Suponha que x come¸ ca com 01. Neste caso y come¸ ca por 01 e, por HI, ∆( y ) = q 2 . Logo, ∆( x ) = δ (∆( y ) , x n ) = δ ( q 2 , x n ) = q 2 o que implica que vale o invariante quando x come¸ ca com 01. Assumimos ent˜ ao que x n˜ ao come¸ ca com 01. E claramente y tamb´ em n˜ ao come¸ ca com 01. Logo, para mostrar que vale o invariante para n &gt; 2, basta mostrar que vale consideramos individualmente que: ( i ) x termina por 00 ou por 01; ( ii ) x termina por 010 ou por 011; ( iii ) x termina por 110 ou por 111, abrangendo todos os casos poss´ ıveis.

Se x termina por 00 ou por 01, temos que y termina por 0 o que implica, desde que y n˜ ao come¸ ca por 01, que ∆( y ) = q 3 . Logo, se x termina por 00, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 3 , 0) = q 3 ; e se x termina por 01, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 3 , 1) = q 5 o que implica que vale o invariante se x termina por 00 ou x termina por 01.

Se x termina por 010 ou por 011, temos que y termina por 01 o que implica, desde que y n˜ ao come¸ ca por 01, que ∆( y ) = q 5 . Logo, se x termina por 010, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 5 , 0) = q 3 ; e se x termina por 011, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 5 , 1) = q 4 o que implica que vale o invariante se x termina por 010 ou por 011.

Se x termina por 110 ou por 111, temos que y termina por 11 o que implica, desde que y n˜ ao come¸ ca por 01, que ∆( y ) = q 4 . Logo, se x termina por 110, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 4 , 0) = q 3 ; e se x termina por 111, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 4 , 1) = q 4 o que implica que vale o invariante se x termina por 010 ou por 011. □

## Opera¸ c˜ oes Regulares

As seguintes opera¸ c˜ oes sobre linguagens s˜ ao chamadas opera¸ c˜ oes regulares :

- 1. Uni˜ ao : A ∪ B = { x : x ∈ A ou x ∈ B } ;
- 2. Concatena¸ c˜ ao : A · B ( ≡ AB ) = { xy : x ∈ A e y ∈ B } ;
- 3. Estrela : A ∗ = { x 1 x 2 . . . x k : k ≥ 0 e cada x i ∈ A } .

Seja A um conjunto. Denotamos por 2 A o conjunto das partes de A , ou seja o conjunto formado por todos os subconjuntos de A . Reescrevendo,

<!-- formula-not-decoded -->

Note que | 2 A | = 2 | A | .

Lema 1. Seja A uma linguagem regular. Ent˜ ao A ∪ { ϵ } tamb´ em ´ e regular.

Prova . ( Esbo¸ co ) Como A ´ e regular, existe um AFD M ′ = ( Q, Σ , δ ′ , r 0 , F ) que reconhece A . Ent˜ ao, o AFD M = ( Q ∪{ q 0 } , Σ , δ, q 0 , F ∪{ q 0 } ), q 0 ̸∈ Q , tal que para todo a ∈ Σ

reconhece A ∪ { ϵ } .

<!-- formula-not-decoded -->

□

Teorema 1. Sejam A e B linguagens regulares sobre Σ . Ent˜ ao A ∪ B , A · B e A ∗ s˜ ao regulares.

Prova . ( Esbo¸ co ) Como A e B s˜ ao regulares, existem AFDs

<!-- formula-not-decoded -->

que reconhecem A e B respectivamente. Sem perda de generalidade assumimos Q A ∩ Q B = ∅ .

O AFD ( Q A × Q B , Σ , δ, ( q 0 , p 0 ) , { ( q, p ) : q ∈ F A ou p ∈ F B } ) tal que δ (( q, p ) , a ) = ( δ A ( q, a ) , δ B ( p, a )), para cada q ∈ Q A p ∈ Q B e a ∈ Σ reconhece ´ e A ∪ B . Portanto, A ∪ B ´ e regular.

Seja

## Exerc´ ıcios

- 1. Construa uma AFD para cada uma das linguagens abaixo.

```
(a) { w ∈ { 0 , 1 } : | w | 0 ≥ 3 ∧ | w | 1 ≥ 2 } (b) { w ∈ { 0 , 1 } : | w | 0 = 2 ∧ | w | 1 ≥ 3 } (c) { w ∈ { 0 , 1 } : | w | 0 mod 2 == 0 ∧ 1 ≤ | w | 1 ≤ 2 } (d) { w ∈ { 0 , 1 } : | w | 0 mod 2 == 0 ∧ cada 1 ´ e seguido por pelo menos 2 zeros. } (e) { w ∈ { 0 , 1 } : | w | 0 mod 2 == 1 ∧ w termina com 1 } (f) { w ∈ { 0 , 1 } : | w | mod 2 == 0 ∧ | w | 1 mod 2 == 1 } (g) { w ∈ { 0 , 1 } : ∃ x ∈ { 0 , 1 } ∗ ( w = 1 x 0) } (h) { w ∈ { 0 , 1 } : | w | 1 ≥ 3 }
```

<!-- formula-not-decoded -->

para cada q ∈ Q A . O AFD ( Q A × 2 Q B , Σ , δ, ( q 0 , X ( q 0 )) , { ( q, S ) : S ∩ F B = ∅} ) tal que

̸

<!-- formula-not-decoded -->

para cada q ∈ Q A , S ⊆ Q B e a ∈ Σ reconhece a linguagem A · B . Portanto, A · B ´ e regular.

Seja

̸

<!-- formula-not-decoded -->

̸

OAFD(2 Q A , Σ , δ, { q 0 } , { S : S ⊆ Q A e S ∩ F A = ∅} ) tal que δ ( S, a ) = ( ∪ q ∈ S δ A ( q, a )) ∪ Y ( ∪ q ∈ S δ A ( q, a )) para cada q ∈ Q A S ⊆ Q A e a ∈ Σ, reconhece A + . Usando o Lema 1 segue que A ∗ = A + ∪ { ϵ } ´ e regular.

□

- (i) { w ∈ { 0 , 1 } : ∃ x, y ∈ { 0 , 1 } ∗ ( w = x 0101 y ) } (j) { w ∈ { 0 , 1 } : | w | ≥ 3 ∧ w 3 = 0 }
- 2. Descreva um diagrama de estados e implemente um AFD M tal que L ( M ) seja o conjunto de cadeias x ∈ { 0 , 1 } ∗ que n˜ ao terminam por 00 onde | x | 0 ´ e par e | x | 1 ´ e um m´ ultiplo de 3.
- 3. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { a, b, c } ∗ : todo b em x ´ e imediatamente seguido por um c } .

- 4. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { a, b } ∗ : x tem dois b 's consecutivos e x n˜ ao tem dois a 's consecutivos } .

- 5. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { a, b } ∗ : x n˜ ao tem dois a 's e nem dois b 's consecutivos } .

- 6. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { a, b, c } ∗ : x come¸ ca e termina com s´ ımbolos distintos } .

- 7. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { 0 , 1 , . . . , 9 } ∗ : a soma dos s´ ımbolos de x ´ e divis´ ıvel por 7 } .

- 8. Especifique e implemente um AFD que aceite exatamente a linguagem consistindo de todas as cadeias x sobre { 0 , 1 } tais que a cadeia x interpretada como um n´ umero bin´ ario seja um m´ ultiplo de 3. Por exemplo, x = 0, x = 000, x = 11, x = 110, x = 001111 s˜ ao cadeias da referida linguagem, enquanto x = 10 e x = 001000 n˜ ao s˜ ao.
- 9. Especifique e implemente um AFD que aceite a linguagem consistindo de todas as cadeias x sobre { 0 , 1 , 2 } tais que a cadeia x interpretada como um n´ umero na base 3 seja um m´ ultiplo de 7.

## 10. Sejam

<!-- formula-not-decoded -->

- o AFD M 3 definido como segue:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

onde

e seja

<!-- formula-not-decoded -->

- a fun¸ c˜ ao de transi¸ c˜ ao definida por

<!-- formula-not-decoded -->

- O AFD M 3 ´ e denominado o produto de M 1 e M 2 . Calcule o AFD produto M 3 dos AFDs M 1 e M 2 dados pelas tabelas abaixo:

|           | a b             |                 | a           | b           |
|-----------|-----------------|-----------------|-------------|-------------|
| q 0 q 1 F | q 0 q 1 q 1 q 0 | → q 0 q 1 q 2 F | q 1 q 2 q 0 | q 2 q 0 q 1 |
| M 1       |                 | M 2             |             |             |

## 11. Seja

<!-- formula-not-decoded -->

um AFD qualquer. Considere o AFD M = ( Q, Σ , δ, q 0 , Q -F ). Ent˜ ao, mostre que L ( M ) = Σ ∗ -L ( M ).

- 12. Dado qualquer conjunto X , para quaisquer subconjuntos A e B de X , mostre que A ⊆ B se, e somente se, A ∩ B = ∅ , onde B ´ e o complemento de B em rela¸ c˜ ao a X .
- 13. Dados dois AFDs, M 1 e M 2 , escreva um algoritmo para decidir se L ( M 1 ) ⊆ L ( M 2 ). Dica: considere o AFD produto .

- 14. Seja M = ( Q, Σ , δ, q 0 , F ) um AFD. Forne¸ ca uma condi¸ c˜ ao suficiente em M para que ϵ ∈ L ( M ). A sua condi¸ c˜ ao ´ e tamb´ em necess´ aria? Justifique sua resposta.
- 15. Seja M = ( Q, Σ , δ, q 0 , F ) um AFD qualquer. Especifique e implemente um outro AFD M ′ , tal que L ( M ′ ) = L ( M ) -{ ϵ } .
- 16. Prove que se L ´ e uma linguagem regular, ent˜ ao L R ´ e uma linguagem regular.
- 17. Mostre que se A e B s˜ ao linguagens regulares, ent˜ ao A ∩ B ´ e regular.
- 18. Mostre que se A ´ e regular, ent˜ ao A ´ e regular.
- 19. Seja A e B linguagens tais que A ´ e regular e B ´ e regular. Mostre que A ∪ ( A · B ) ´ e regular.

## Minimiza¸ c˜ ao de Estados

## Considera¸ c˜ oes iniciais

Considere o AFD da figura abaixo.

<!-- image -->

Note que os estados q 3 , q 4 e q 5 poderiam ser 'fundidos' em um ´ unico estado, pois eles s˜ ao todos estados finais e, uma vez que o AFD entre em um deles, ele n˜ ao pode mais sair. Feito isto, note agora que o estado q 6 n˜ ao pode ser alcan¸ cado, de modo que a sua presen¸ ca n˜ ao influencia a aceita¸ c˜ ao de qualquer cadeia o que significa que ele pode ser exclu´ ıdo. Portanto, o AFD ilustrado ´ e equivalente ao AFD

<!-- image -->

Ent˜ ao, dada uma linguagem regular A , uma quest˜ ao interessante (na verdade importante) ´ e como podemos encontrar um AFD M tal que L ( M ) = A e M tenha o menor n´ umero de estados entre todos os AFDs que reconhecem A ? Este processo ´ e denominado minimiza¸ c˜ ao de estados e consiste de duas etapas:

- 1. eliminar estados inating´ ıveis ; isto ´ e, eliminar os estados q ∈ Q para os quais n˜ ao existe x ∈ Σ ∗ tal que ∆( x ) = q ;
- 2. fundir estados ' equivalentes '.

A etapa de elimina¸ c˜ ao de estados inating´ ıveis n˜ ao altera a linguagem reconhecida pelo AFD e pode ser efetuada por um algoritmo simples baseado em uma busca em profundidade no 'grafo' correspondente ao diagrama de transi¸ c˜ ao do AFD. Portanto, vamos assumir que esta etapa tenha sido realizada. Para o etapa 2, n´ os precisamos definir claramente o que significa estado equivalente e como n´ os podemos fundir dois deles em um s´ o. Para tal, vamos primeiro dar uma olhada na s´ erie de exemplos dada a seguir.

Exemplo 5. Considere os dois AFDs abaixo:

<!-- image -->

Ambos reconhecem a mesma linguagem { a, b } . O AFD com 4 estados entra em estados distintos dependendo do primeiro s´ ımbolo lido, mas n˜ ao h´ a raz˜ ao nenhuma para que os estados destinos sejam distintos. Eles s˜ ao 'equivalentes' e podem ser fundidos em um s´ o estado, dando origem ao AFD com 3 estados.

## Exemplo 6. Considere os dois AFDs abaixo:

<!-- image -->

Ambos reconhecem a mesma linguagem, { x : | x | = 1 ∨ | x | ≥ 3 } . No AFD com mais estados, os estados q 3 e q 4 s˜ ao equivalentes, pois ambos possuem transi¸ c˜ oes para o estado q 5 para todos os s´ ımbolos de entrada. Logo, n˜ ao h´ a raz˜ ao para eles serem distintos. Uma vez que q 3 e q 4 s˜ ao fundidos, n´ os tamb´ em podemos fundir q 1 e q 2 pela mesma raz˜ ao, dando origem ao AFD com menos estados.

Exemplo 7. Considere os dois AFDs a seguir. Ambos reconhecem a mesma linguagem:

<!-- formula-not-decoded -->

Os estados q 1 e q 2 s˜ ao equivalente e podem ser fundidos; similarmente q 3 , q 4 e q 5 tamb´ em s˜ ao equivalentes e tamb´ em podem ser fundidos em um ´ unico estado, dando origem ao AFD com menos estados.

<!-- image -->

Exemplo 8. Os dois AFDs a seguir reconhecem a mesma linguagem:

{ a n : ( n -1) ´ e um m´ ultiplo de 3 } .

No AFD com mais estados, os estados q 1 e q 4 s˜ ao equivalentes e podem ser fundidos, dando origem ao AFD com menos estados.

<!-- image -->

## O AFD m´ ınimal

Como sabemos em geral quando dois estados podem ser fundidos em um s´ o sem mudar a linguagem reconhecida pelo AFD original? Como n´ os sabemos quando n˜ ao podemos mais fundir estados de um dado AFD?

Considerando que todos os estados do AFD M s˜ ao ating´ ıveis, considere dois estados: p e q , tais que δ ( p, ϵ ) ∈ F e δ ( q, ϵ ) ̸∈ F . Ser´ a que podemos fundir p e q em um ´ unico estado? Como δ ( p, ϵ ) = F e δ ( q, ϵ ) ̸∈ F , temos que p ∈ F e q ̸∈ F , o que implica que p = ∆( x ) e q = ∆( y ), ou seja, x ∈ L ( M ) e y ̸∈ L ( M ). Fundir os estados e considerar que o estado resultante est´ a em F ´ e considerar que y ∈ L ( M ) o que ´ e uma contradi¸ c˜ ao; e considerar que o estado resultante n˜ ao est´ a em F ´ e considerar que x ̸∈ L ( M ) o que tamb´ em ´ e contradi¸ c˜ ao. Logo, n˜ ao podemos fundir um estado de aceita¸ c˜ ao com um de n˜ ao aceita¸ c˜ ao. A seguir vamos mostrar quando p e q podem ser fundidos.

Primeiro, vamos definir uma rela¸ c˜ ao em Q , denotada por ∼ , como segue:

<!-- formula-not-decoded -->

e dizemos que p e q s˜ ao equivalentes . N˜ ao ´ e dif´ ıcil verificar que a rela¸ c˜ ao ∼ ´ e de fato uma rela¸ c˜ ao de equivalˆ encia, isto ´ e, possui as propriedades reflexiva ( p ∼ p para todo p ∈ Q ); sim´ etrica ( p ∼ q → q ∼ p para todo p, q ∈ Q ); e transitiva

( p ∼ q e q ∼ r → p ∼ r para todo p, q, r ∈ Q ). Logo ∼ particiona Q em classes de equivalˆ encia :

<!-- formula-not-decoded -->

N´ os agora definimos um AFD, M min , chamado AFD m´ ınimal de M , tal que os estados de M min correspondem ` as classes de equivalˆ encia de ∼ :

Seja

onde

- · Q ′ = { [ p ] : p ∈ Q } ,
- · δ ′ ([ p ] , a ) = [ δ ( p, a )] , ∀ [ p ] ∈ Q,a ∈ Σ,
- · s ′ = [ s ],
- · F ′ = { [ p ] : p ∈ F } .

O lema a seguir mostra que a fun¸ c˜ ao δ ′ est´ a bem definida .

Lema 2. Sejam p, q ∈ Q e a ∈ Σ . Se p ∼ q , ent˜ ao δ ( p, a ) ∼ δ ( q, a ) .

Prova . Seja x ∈ Σ ∗ e suponha que p ∼ q . Segue que ∀ x (∆( p, ax ) ∈ F ↔ ∆( q, ax ) ∈ F ). Como ∆( p, ax ) = ∆( δ ( p, a ) , x ) e ∆( q, ax ) = ∆( δ ( q, a ) , x ), segue que ∀ x (∆( δ ( p, a ) , x ) ∈ F ↔ ∆( δ ( q, a ) , x ) ∈ F ). Segue da defini¸ c˜ ao que δ ( p, a ) ∼ δ ( q, a ). □

O Lema 2 mostra que [ p ] = [ q ], ent˜ ao [ δ ( p, a )] = [ δ ( q, a )] o que significa que a fun¸ c˜ ao δ ′ est´ a bem definida. O conjunto F ′ tamb´ em est´ a bem definido e, portanto, segue claramente da defini¸ c˜ ao de F ′ que

Os seguintes resultados provam que L ( M min ) = L ( M ):

<!-- formula-not-decoded -->

Lema 4. Para toda cadeia x ∈ Σ ∗ , ∆ ′ ([ p ] , x ) = [∆( p, x )] .

<!-- formula-not-decoded -->

Prova . Indu¸ c˜ ao em n = | x | .

Suponha que n = 0. Nesse caso x = ϵ , o que implica que

<!-- formula-not-decoded -->

Suponha agora que n &gt; 0. Logo, x ∈ Σ n . Como n &gt; 0, n´ os podemos escrever x = ya , para algum y ∈ Σ n -1 e algum a ∈ Σ. Ent˜ ao,

<!-- formula-not-decoded -->

□

□

N´ os acabamos de provar que M min ´ e equivalente a M . Agora, ´ e natural nos perguntarmos se M min ´ e o 'menor' AFD equivalente a M que podemos construir removendo estados inating´ ıveis e fundindo estados equivalentes. A resposta ´ e sim. Para provar

Teorema 2. L ( M min ) = L ( M ) .

Prova . Para qualquer x ∈ Σ ∗ ,

<!-- formula-not-decoded -->

este fato, vamos usar a constru¸ c˜ ao do AFD m´ ınimal em M min para tentar fundir dois estados quaisquer de M min , dando origem a um AFD 'menor'.

Seja

<!-- formula-not-decoded -->

A rela¸ c˜ ao acima ´ e a mesma que ∼ , mas ela ´ e definida no conjunto de estados Q ′ do AFD m´ ınimal M min . Agora,

<!-- formula-not-decoded -->

Logo, quaisquer dois estados equivalentes de M min s˜ ao de fato iguais, e a rela¸ c˜ ao ∼ em Q ′ nada mais ´ e do que a rela¸ c˜ ao identidade =. Isto significa que M min ´ e o menor AFD que se pode construir atrav´ es da remo¸ c˜ ao de estados inating´ ıveis e da fundi¸ c˜ ao de estados equivalentes de M .

## Um Algoritmo para Minimiza¸ c˜ ao de Estados

Agora, n´ os estudaremos um algoritmo para descobrir os pares de estados equivalentes de um dado AFD M . Tal algoritmo ´ e denominado algoritmo de minimiza¸ c˜ ao de estados e nos permite construir o AFD minimal M min , que reconhece L ( M ). O algoritmo assume que n˜ ao h´ a estados inating´ ıveis em M . Isto n˜ ao chega a ser uma restri¸ c˜ ao, pois n´ os podemos remover tais estados usando um simples algoritmo como mencionado antes.

A opera¸ c˜ ao b´ asica do algoritmo ´ e marcar pares { p, q } (n˜ ao ordenados) de estados de M t˜ ao logo esse algoritmo descubra que p e q n˜ ao s˜ ao equivalentes. Dois estados p, q s˜ ao equivalentes se vale que ∆( p, x ) ´ e um estado final se e somente se ∆( q, x ) ´ e um estado final para todo x ∈ Σ ∗ . Se p e q s˜ ao equivalentes escrevemos p ∼ q .

Os passos do algoritmo s˜ ao os seguintes:

- 1. construa uma tabela tal que cada entrada da tabela corresponde a um par n˜ ao ordenado { p, q } de estados de M . Todos os pares est˜ ao inicialmente desmarcados. A informa¸ c˜ ao se um par de estados est´ a marcado ou n˜ ao ´ e armazenada na entrada da tabela correspondente ao par;
- 2. marque { p, q } se p ∈ F e q ̸∈ F ou vice-versa;
- 3. repita o seguinte procedimento at´ e que ele n˜ ao marque mais nenhum par de estados: se existir um par { p, q } desmarcado tal que { δ ( p, a ) , δ ( q, a ) } est´ a marcado para algum a ∈ Σ, ent˜ ao marque { p, q } .

Quando o algoritmo terminar, n´ os temos que p ∼ q se, e somente se, { p, q } n˜ ao est´ a marcado. Logo, os estados equivalentes entre si que n˜ ao est˜ ao marcados devem ser devem ser fundidos para gerar os estados de M min .

Exemplo 9. Vamos aplicar o algoritmo de minimiza¸ c˜ ao acima ao AFD M ,

<!-- formula-not-decoded -->

tal que Q = { q 0 , q 1 , q 2 , q 3 , q 4 , q 5 } , Σ = { a, b } , s = q 0 , F = { q 1 , q 2 , q 5 } e δ ´ e dada pela tabela a seguir:

| δ   | a   | b   |
|-----|-----|-----|
| q 0 | q 1 | q 2 |
| q 1 | q 3 | q 4 |
| q 2 | q 4 | q 3 |
| q 3 | q 5 | q 5 |
| q 4 | q 5 | q 5 |
| q 5 | q 5 | q 5 |

- O diagrama de transi¸ c˜ ao de M ´ e mostrado a seguir:

<!-- image -->

Primeiramente assinalamos os pares de estado pq tais que p ∈ F e q = F .

<!-- image -->

Depois marcamos q 5 q 1 e q 5 q 2 pois δ ( q 5 , a ) = q 5 ̸∼ q 4 = δ ( q 2 , a ) = δ ( q 2 , a ) .

<!-- image -->

Depois marcamos q 0 q 3 e q 0 q 4 pois δ ( q 0 , a ) = q 1 ̸∼ q 5 = δ ( q 3 , a ) = δ ( q 4 , a ) .

̸

<!-- image -->

Agora n˜ ao marcamos mais nada

<!-- formula-not-decoded -->

e o algoritmo temina fazendo fundindo os estados q 1 q 2 ; e fundindo os estados q 3 q 4 O diagrama de estados resultante ´ e:

<!-- image -->

.

## Referˆ encias Bibliogr´ aficas