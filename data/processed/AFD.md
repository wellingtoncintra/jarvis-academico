## Autômato Finito Determinístico

## Definição

Um autômato finito determinístico (AFD) M é uma quíntupla

onde:

- · Q : conjunto finito de estados ;
- · Σ: conjunto finito de símbolos -alfabeto de entrada ;
- · δ : Q × Σ → Q : função de transição ;
- · q 0 ∈ Q : estado inicial ;
- · F ⊆ Q : estados finais ou de aceitação .

Seja x ∈ Σ ∗ , | x | = n . Definimos a função ∆ : Q × Σ ∗ → Q de computação de M , onde

Se p é o estado inicial podemos escrever simplesmente ∆( x ) significando ∆( p, x ).

Dizemos que:

- 1. M aceita x se ∆( x ) ∈ F . Denotamos isso por M ( x ) = aceita ;

- 2. M rejeita x se ¬ ( M ( x ) = aceita ). Denotamos isso por M ( x ) = rejeita ;
- 3. M reconhece a linguagem L ( M ) = { x ∈ Σ ∗ : M ( x ) = aceita } ;
- 4. M e N são equivalentes se L ( M ) = L ( N ). Denotamos isso por M ≡ N ;
- 5. a linguagem A ⊆ Σ ∗ é dita regular se A = L ( M ) para algum AFD M .

## Representação de um AFD

Podemos representamos um AFD neste texto usando

- 1. a definição vista na seção anterior;
- 2. uma tabela representando a função de transição;
- 3. um diagrama de transição de estados.

## Exemplo 1. Considere o AFD

onde δ ( q 0 , a ) = q 1 , δ ( q 1 , a ) = q 2 , δ ( q 2 , a ) = δ ( q 3 , a ) = q 3 , δ ( q, b ) = q para todo q ∈ Q .

Usando uma tabela como na Tabela 1, a 'seta' à esquerda de q 0 indica que q 0 é o estado inicial e o F ao lado de q 3 indica que q 3 é um estado final.

Tabela 1: Representação de um AFD por uma tabela

| | | a | b |
|------|-------|-----|-----|
| → | q 0 | q 1 | q 0 |
| M := | q 1 | q 2 | q 1 |
| | q 2 | q 3 | q 2 |
| | q 3 F | q 3 | q 3 |

Usando um diagrama de transição de estados, a seta apontando para o q 0 indica que q 0 é o estado inicial; e todo estado com círculo duplo é um estado de aceitação. A Figura 1 mostra um diagrama de estados do Exemplo 1.

Figura 1: Diagrama de transição de estados do AFD do Exemplo 1.

<!-- image -->

Exemplo 2. Descreva um AFD que reconhece a linguagem { x ∈ { 0 , 1 } ∗ : | x | é par } .

Solução:

Exemplo 3. Descreva um AFD que reconhece a linguagem

<!-- image -->

Solução:

O AFD descrito tem 5 estados q 0 , q 1 , q 2 , q 3 , q 4 , q 5 sobre o alfabeto { 0 , 1 } e função de transição dada pela tabela

| δ | 0 | 1 |
|-------|-----|-----|
| q 0 | q 1 | q 4 |
| q 1 | q 3 | q 2 |
| q 2 F | q 2 | q 2 |
| q 3 | q 3 | q 5 |
| q 4 | q 3 | q 4 |
| q 5 F | q 3 | q 4 |

Exemplo 4. Descreva um AFD que reconhece

{ x ∈ { 0 , · · · , 9 } ∗ : o número x em decimal é um múltiplo de 3 } .

## Solução:

O AFD descrito possui 3 estados q 0 q 1 , q 2 sobre o alfabeto Σ = { 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 } , e função de transição dada pela tabela

| δ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| q 0 F | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 |
| q 1 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 |
| q 2 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 | q 0 | q 1 | q 2 |

<!-- image -->

## Implementação

Um AFD pode ser visto como um formalismo reconhecedor para representar uma linguagem, ou seja, uma máquina que aceita cadeias de uma determinada linguagem. Esse mecanismo pode ser implementado por um programa de computador. A seguir mostramos um exemplo em python que devolve True se uma cadeia s é aceita pelo AFD do Exemplo 1; e devolve False caso contrário.

```
q = estadoInicial i = 0 n = len(s) while i < n: q = transicao[q][s[i]] i += 1
```

return q in estadoFinal

## Prova de que um AFD reconhece uma linguagem

Vejamos primeiramente o Exemplo 2 e provamos o seguinte invariante.

Invariante 1. Seja x ∈ Σ ∗ , n = | x | . Então,

Prova . A prova é por indução em n = | x | .

Suponha que n = 0. Nesse caso, x = ϵ . Como ∆( ϵ ) = q 0 e | ϵ | é par, temos que nesse caso vale o invariante.

Suponha então que n &gt; 0. Por hipótese de indução, temos que

Se | x | é par, | y | é ímpar o que implica, por HI que ∆( y ) = q 1 e, portanto, ∆( x ) = δ (∆( y ) , x n ) = δ ( q 1 , x n ) = q 0 ; similarmente, ∆( x ) = q 1 se | x | é ímpar. Logo, vale o invariante para n &gt; 0.

□

Desde que F = { q 0 } , segue do invariante acima mostra que M aceita somente as cadeias de comprimento par.

## Seja o AFD

<!-- image -->

Esse AFD reconhece a linguagem { x ∈ { 0 , 1 } ∗ : x começa ou termina com 01 } . Para mostrar que isto é verdade basta mostrar o seguinte invariante.

Invariante 2. Seja x ∈ { 0 , 1 } ∗ . Então,

Prova . A prova é por indução em n = | x | .

Suponha que n ≤ 2. Nesse caso, x ∈ { ϵ, 0 , 1 , 00 , 01 , 10 , 11 } . Verificamos que o invariante vale para cada valor possível para x . Portanto, vale o invariante para n ≤ 2.

Suponha então que n &gt; 2. Por hipótese de indução, temos que

̸

(Note que y = ϵ , y = 0 e y = 1 porque | y | ≥ 2.)

̸

̸

Suponha que x começa com 01. Neste caso y começa por 01 e, por HI, ∆( y ) = q 2 . Logo, ∆( x ) = δ (∆( y ) , x n ) = δ ( q 2 , x n ) = q 2 o que implica que vale o invariante quando x começa com 01. Assumimos então que x não começa com 01. E claramente y também não começa com 01. Logo, para mostrar que vale o invariante para n &gt; 2, basta mostrar que vale consideramos individualmente que: ( i ) x termina por 00 ou por 01; ( ii ) x termina por 010 ou por 011; ( iii ) x termina por 110 ou por 111, abrangendo todos os casos possíveis.

Se x termina por 00 ou por 01, temos que y termina por 0 o que implica, desde que y não começa por 01, que ∆( y ) = q 3 . Logo, se x termina por 00, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 3 , 0) = q 3 ; e se x termina por 01, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 3 , 1) = q 5 o que implica que vale o invariante se x termina por 00 ou x termina por 01.

Se x termina por 010 ou por 011, temos que y termina por 01 o que implica, desde que y não começa por 01, que ∆( y ) = q 5 . Logo, se x termina por 010, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 5 , 0) = q 3 ; e se x termina por 011, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 5 , 1) = q 4 o que implica que vale o invariante se x termina por 010 ou por 011.

Se x termina por 110 ou por 111, temos que y termina por 11 o que implica, desde que y não começa por 01, que ∆( y ) = q 4 . Logo, se x termina por 110, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 4 , 0) = q 3 ; e se x termina por 111, temos que ∆( x ) = δ (∆( y ) , x n ) = δ ( q 4 , 1) = q 4 o que implica que vale o invariante se x termina por 010 ou por 011. □

## Operações Regulares

As seguintes operações sobre linguagens são chamadas operações regulares :

- 1. União : A ∪ B = { x : x ∈ A ou x ∈ B } ;
- 2. Concatenação : A · B ( ≡ AB ) = { xy : x ∈ A e y ∈ B } ;
- 3. Estrela : A ∗ = { x 1 x 2 . . . x k : k ≥ 0 e cada x i ∈ A } .

Seja A um conjunto. Denotamos por 2 A o conjunto das partes de A , ou seja o conjunto formado por todos os subconjuntos de A . Reescrevendo,

Note que | 2 A | = 2 | A | .

Lema 1. Seja A uma linguagem regular. Então A ∪ { ϵ } também é regular.

Prova . ( Esboço ) Como A é regular, existe um AFD M ′ = ( Q, Σ , δ ′ , r 0 , F ) que reconhece A . Então, o AFD M = ( Q ∪{ q 0 } , Σ , δ, q 0 , F ∪{ q 0 } ), q 0 ̸∈ Q , tal que para todo a ∈ Σ

reconhece A ∪ { ϵ } .

□

Teorema 1. Sejam A e B linguagens regulares sobre Σ . Então A ∪ B , A · B e A ∗ são regulares.

Prova . ( Esboço ) Como A e B são regulares, existem AFDs

que reconhecem A e B respectivamente. Sem perda de generalidade assumimos Q A ∩ Q B = ∅ .

O AFD ( Q A × Q B , Σ , δ, ( q 0 , p 0 ) , { ( q, p ) : q ∈ F A ou p ∈ F B } ) tal que δ (( q, p ) , a ) = ( δ A ( q, a ) , δ B ( p, a )), para cada q ∈ Q A p ∈ Q B e a ∈ Σ reconhece é A ∪ B . Portanto, A ∪ B é regular.

Seja

## Exercícios

- 1. Construa uma AFD para cada uma das linguagens abaixo.

```
(a) { w ∈ { 0 , 1 } : | w | 0 ≥ 3 ∧ | w | 1 ≥ 2 } (b) { w ∈ { 0 , 1 } : | w | 0 = 2 ∧ | w | 1 ≥ 3 } (c) { w ∈ { 0 , 1 } : | w | 0 mod 2 == 0 ∧ 1 ≤ | w | 1 ≤ 2 } (d) { w ∈ { 0 , 1 } : | w | 0 mod 2 == 0 ∧ cada 1 é seguido por pelo menos 2 zeros. } (e) { w ∈ { 0 , 1 } : | w | 0 mod 2 == 1 ∧ w termina com 1 } (f) { w ∈ { 0 , 1 } : | w | mod 2 == 0 ∧ | w | 1 mod 2 == 1 } (g) { w ∈ { 0 , 1 } : ∃ x ∈ { 0 , 1 } ∗ ( w = 1 x 0) } (h) { w ∈ { 0 , 1 } : | w | 1 ≥ 3 }
```

para cada q ∈ Q A . O AFD ( Q A × 2 Q B , Σ , δ, ( q 0 , X ( q 0 )) , { ( q, S ) : S ∩ F B = ∅} ) tal que

̸

para cada q ∈ Q A , S ⊆ Q B e a ∈ Σ reconhece a linguagem A · B . Portanto, A · B é regular.

Seja

̸

̸

OAFD(2 Q A , Σ , δ, { q 0 } , { S : S ⊆ Q A e S ∩ F A = ∅} ) tal que δ ( S, a ) = ( ∪ q ∈ S δ A ( q, a )) ∪ Y ( ∪ q ∈ S δ A ( q, a )) para cada q ∈ Q A S ⊆ Q A e a ∈ Σ, reconhece A + . Usando o Lema 1 segue que A ∗ = A + ∪ { ϵ } é regular.

□

- (i) { w ∈ { 0 , 1 } : ∃ x, y ∈ { 0 , 1 } ∗ ( w = x 0101 y ) } (j) { w ∈ { 0 , 1 } : | w | ≥ 3 ∧ w 3 = 0 }
- 2. Descreva um diagrama de estados e implemente um AFD M tal que L ( M ) seja o conjunto de cadeias x ∈ { 0 , 1 } ∗ que não terminam por 00 onde | x | 0 é par e | x | 1 é um múltiplo de 3.
- 3. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { a, b, c } ∗ : todo b em x é imediatamente seguido por um c } .

- 4. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { a, b } ∗ : x tem dois b 's consecutivos e x não tem dois a 's consecutivos } .

- 5. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { a, b } ∗ : x não tem dois a 's e nem dois b 's consecutivos } .

- 6. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { a, b, c } ∗ : x começa e termina com símbolos distintos } .

- 7. Especifique e implemente um AFD M tal que

L ( M ) = { x ∈ { 0 , 1 , . . . , 9 } ∗ : a soma dos símbolos de x é divisível por 7 } .

- 8. Especifique e implemente um AFD que aceite exatamente a linguagem consistindo de todas as cadeias x sobre { 0 , 1 } tais que a cadeia x interpretada como um número binário seja um múltiplo de 3. Por exemplo, x = 0, x = 000, x = 11, x = 110, x = 001111 são cadeias da referida linguagem, enquanto x = 10 e x = 001000 não são.
- 9. Especifique e implemente um AFD que aceite a linguagem consistindo de todas as cadeias x sobre { 0 , 1 , 2 } tais que a cadeia x interpretada como um número na base 3 seja um múltiplo de 7.

## 10. Sejam

- o AFD M 3 definido como segue:

onde

e seja

- a função de transição definida por

- O AFD M 3 é denominado o produto de M 1 e M 2 . Calcule o AFD produto M 3 dos AFDs M 1 e M 2 dados pelas tabelas abaixo:

| | a b | | a | b |
|-----------|-----------------|-----------------|-------------|-------------|
| q 0 q 1 F | q 0 q 1 q 1 q 0 | → q 0 q 1 q 2 F | q 1 q 2 q 0 | q 2 q 0 q 1 |
| M 1 | | M 2 | | |

## 11. Seja

um AFD qualquer. Considere o AFD M = ( Q, Σ , δ, q 0 , Q -F ). Então, mostre que L ( M ) = Σ ∗ -L ( M ).

- 12. Dado qualquer conjunto X , para quaisquer subconjuntos A e B de X , mostre que A ⊆ B se, e somente se, A ∩ B = ∅ , onde B é o complemento de B em relação a X .
- 13. Dados dois AFDs, M 1 e M 2 , escreva um algoritmo para decidir se L ( M 1 ) ⊆ L ( M 2 ). Dica: considere o AFD produto .

- 14. Seja M = ( Q, Σ , δ, q 0 , F ) um AFD. Forneça uma condição suficiente em M para que ϵ ∈ L ( M ). A sua condição é também necessária? Justifique sua resposta.
- 15. Seja M = ( Q, Σ , δ, q 0 , F ) um AFD qualquer. Especifique e implemente um outro AFD M ′ , tal que L ( M ′ ) = L ( M ) -{ ϵ } .
- 16. Prove que se L é uma linguagem regular, então L R é uma linguagem regular.
- 17. Mostre que se A e B são linguagens regulares, então A ∩ B é regular.
- 18. Mostre que se A é regular, então A é regular.
- 19. Seja A e B linguagens tais que A é regular e B é regular. Mostre que A ∪ ( A · B ) é regular.

## Minimização de Estados

## Considerações iniciais

Considere o AFD da figura abaixo.

<!-- image -->

Note que os estados q 3 , q 4 e q 5 poderiam ser 'fundidos' em um único estado, pois eles são todos estados finais e, uma vez que o AFD entre em um deles, ele não pode mais sair. Feito isto, note agora que o estado q 6 não pode ser alcançado, de modo que a sua presença não influencia a aceitação de qualquer cadeia o que significa que ele pode ser excluído. Portanto, o AFD ilustrado é equivalente ao AFD

<!-- image -->

Então, dada uma linguagem regular A , uma questão interessante (na verdade importante) é como podemos encontrar um AFD M tal que L ( M ) = A e M tenha o menor número de estados entre todos os AFDs que reconhecem A ? Este processo é denominado minimização de estados e consiste de duas etapas:

- 1. eliminar estados inatingíveis ; isto é, eliminar os estados q ∈ Q para os quais não existe x ∈ Σ ∗ tal que ∆( x ) = q ;
- 2. fundir estados ' equivalentes '.

A etapa de eliminação de estados inatingíveis não altera a linguagem reconhecida pelo AFD e pode ser efetuada por um algoritmo simples baseado em uma busca em profundidade no 'grafo' correspondente ao diagrama de transição do AFD. Portanto, vamos assumir que esta etapa tenha sido realizada. Para o etapa 2, nós precisamos definir claramente o que significa estado equivalente e como nós podemos fundir dois deles em um só. Para tal, vamos primeiro dar uma olhada na série de exemplos dada a seguir.

Exemplo 5. Considere os dois AFDs abaixo:

<!-- image -->

Ambos reconhecem a mesma linguagem { a, b } . O AFD com 4 estados entra em estados distintos dependendo do primeiro símbolo lido, mas não há razão nenhuma para que os estados destinos sejam distintos. Eles são 'equivalentes' e podem ser fundidos em um só estado, dando origem ao AFD com 3 estados.

## Exemplo 6. Considere os dois AFDs abaixo:

<!-- image -->

Ambos reconhecem a mesma linguagem, { x : | x | = 1 ∨ | x | ≥ 3 } . No AFD com mais estados, os estados q 3 e q 4 são equivalentes, pois ambos possuem transições para o estado q 5 para todos os símbolos de entrada. Logo, não há razão para eles serem distintos. Uma vez que q 3 e q 4 são fundidos, nós também podemos fundir q 1 e q 2 pela mesma razão, dando origem ao AFD com menos estados.

Exemplo 7. Considere os dois AFDs a seguir. Ambos reconhecem a mesma linguagem:

Os estados q 1 e q 2 são equivalente e podem ser fundidos; similarmente q 3 , q 4 e q 5 também são equivalentes e também podem ser fundidos em um único estado, dando origem ao AFD com menos estados.

<!-- image -->

Exemplo 8. Os dois AFDs a seguir reconhecem a mesma linguagem:

{ a n : ( n -1) é um múltiplo de 3 } .

No AFD com mais estados, os estados q 1 e q 4 são equivalentes e podem ser fundidos, dando origem ao AFD com menos estados.

<!-- image -->

## O AFD mínimal

Como sabemos em geral quando dois estados podem ser fundidos em um só sem mudar a linguagem reconhecida pelo AFD original? Como nós sabemos quando não podemos mais fundir estados de um dado AFD?

Considerando que todos os estados do AFD M são atingíveis, considere dois estados: p e q , tais que δ ( p, ϵ ) ∈ F e δ ( q, ϵ ) ̸∈ F . Será que podemos fundir p e q em um único estado? Como δ ( p, ϵ ) = F e δ ( q, ϵ ) ̸∈ F , temos que p ∈ F e q ̸∈ F , o que implica que p = ∆( x ) e q = ∆( y ), ou seja, x ∈ L ( M ) e y ̸∈ L ( M ). Fundir os estados e considerar que o estado resultante está em F é considerar que y ∈ L ( M ) o que é uma contradição; e considerar que o estado resultante não está em F é considerar que x ̸∈ L ( M ) o que também é contradição. Logo, não podemos fundir um estado de aceitação com um de não aceitação. A seguir vamos mostrar quando p e q podem ser fundidos.

Primeiro, vamos definir uma relação em Q , denotada por ∼ , como segue:

e dizemos que p e q são equivalentes . Não é difícil verificar que a relação ∼ é de fato uma relação de equivalência, isto é, possui as propriedades reflexiva ( p ∼ p para todo p ∈ Q ); simétrica ( p ∼ q → q ∼ p para todo p, q ∈ Q ); e transitiva

( p ∼ q e q ∼ r → p ∼ r para todo p, q, r ∈ Q ). Logo ∼ particiona Q em classes de equivalência :

Nós agora definimos um AFD, M min , chamado AFD mínimal de M , tal que os estados de M min correspondem às classes de equivalência de ∼ :

Seja

onde

- · Q ′ = { [ p ] : p ∈ Q } ,
- · δ ′ ([ p ] , a ) = [ δ ( p, a )] , ∀ [ p ] ∈ Q,a ∈ Σ,
- · s ′ = [ s ],
- · F ′ = { [ p ] : p ∈ F } .

O lema a seguir mostra que a função δ ′ está bem definida .

Lema 2. Sejam p, q ∈ Q e a ∈ Σ . Se p ∼ q , então δ ( p, a ) ∼ δ ( q, a ) .

Prova . Seja x ∈ Σ ∗ e suponha que p ∼ q . Segue que ∀ x (∆( p, ax ) ∈ F ↔ ∆( q, ax ) ∈ F ). Como ∆( p, ax ) = ∆( δ ( p, a ) , x ) e ∆( q, ax ) = ∆( δ ( q, a ) , x ), segue que ∀ x (∆( δ ( p, a ) , x ) ∈ F ↔ ∆( δ ( q, a ) , x ) ∈ F ). Segue da definição que δ ( p, a ) ∼ δ ( q, a ). □

O Lema 2 mostra que [ p ] = [ q ], então [ δ ( p, a )] = [ δ ( q, a )] o que significa que a função δ ′ está bem definida. O conjunto F ′ também está bem definido e, portanto, segue claramente da definição de F ′ que

Os seguintes resultados provam que L ( M min ) = L ( M ):

Lema 4. Para toda cadeia x ∈ Σ ∗ , ∆ ′ ([ p ] , x ) = [∆( p, x )] .

Prova . Indução em n = | x | .

Suponha que n = 0. Nesse caso x = ϵ , o que implica que

Suponha agora que n &gt; 0. Logo, x ∈ Σ n . Como n &gt; 0, nós podemos escrever x = ya , para algum y ∈ Σ n -1 e algum a ∈ Σ. Então,

□

□

Nós acabamos de provar que M min é equivalente a M . Agora, é natural nos perguntarmos se M min é o 'menor' AFD equivalente a M que podemos construir removendo estados inatingíveis e fundindo estados equivalentes. A resposta é sim. Para provar

Teorema 2. L ( M min ) = L ( M ) .

Prova . Para qualquer x ∈ Σ ∗ ,

este fato, vamos usar a construção do AFD mínimal em M min para tentar fundir dois estados quaisquer de M min , dando origem a um AFD 'menor'.

Seja

A relação acima é a mesma que ∼ , mas ela é definida no conjunto de estados Q ′ do AFD mínimal M min . Agora,

Logo, quaisquer dois estados equivalentes de M min são de fato iguais, e a relação ∼ em Q ′ nada mais é do que a relação identidade =. Isto significa que M min é o menor AFD que se pode construir através da remoção de estados inatingíveis e da fundição de estados equivalentes de M .

## Um Algoritmo para Minimização de Estados

Agora, nós estudaremos um algoritmo para descobrir os pares de estados equivalentes de um dado AFD M . Tal algoritmo é denominado algoritmo de minimização de estados e nos permite construir o AFD minimal M min , que reconhece L ( M ). O algoritmo assume que não há estados inatingíveis em M . Isto não chega a ser uma restrição, pois nós podemos remover tais estados usando um simples algoritmo como mencionado antes.

A operação básica do algoritmo é marcar pares { p, q } (não ordenados) de estados de M tão logo esse algoritmo descubra que p e q não são equivalentes. Dois estados p, q são equivalentes se vale que ∆( p, x ) é um estado final se e somente se ∆( q, x ) é um estado final para todo x ∈ Σ ∗ . Se p e q são equivalentes escrevemos p ∼ q .

Os passos do algoritmo são os seguintes:

- 1. construa uma tabela tal que cada entrada da tabela corresponde a um par não ordenado { p, q } de estados de M . Todos os pares estão inicialmente desmarcados. A informação se um par de estados está marcado ou não é armazenada na entrada da tabela correspondente ao par;
- 2. marque { p, q } se p ∈ F e q ̸∈ F ou vice-versa;
- 3. repita o seguinte procedimento até que ele não marque mais nenhum par de estados: se existir um par { p, q } desmarcado tal que { δ ( p, a ) , δ ( q, a ) } está marcado para algum a ∈ Σ, então marque { p, q } .

Quando o algoritmo terminar, nós temos que p ∼ q se, e somente se, { p, q } não está marcado. Logo, os estados equivalentes entre si que não estão marcados devem ser devem ser fundidos para gerar os estados de M min .

Exemplo 9. Vamos aplicar o algoritmo de minimização acima ao AFD M ,

tal que Q = { q 0 , q 1 , q 2 , q 3 , q 4 , q 5 } , Σ = { a, b } , s = q 0 , F = { q 1 , q 2 , q 5 } e δ é dada pela tabela a seguir:

| δ | a | b |
|-----|-----|-----|
| q 0 | q 1 | q 2 |
| q 1 | q 3 | q 4 |
| q 2 | q 4 | q 3 |
| q 3 | q 5 | q 5 |
| q 4 | q 5 | q 5 |
| q 5 | q 5 | q 5 |

- O diagrama de transição de M é mostrado a seguir:

<!-- image -->

Primeiramente assinalamos os pares de estado pq tais que p ∈ F e q = F .

<!-- image -->

Depois marcamos q 5 q 1 e q 5 q 2 pois δ ( q 5 , a ) = q 5 ̸∼ q 4 = δ ( q 2 , a ) = δ ( q 2 , a ) .

<!-- image -->

Depois marcamos q 0 q 3 e q 0 q 4 pois δ ( q 0 , a ) = q 1 ̸∼ q 5 = δ ( q 3 , a ) = δ ( q 4 , a ) .

̸

<!-- image -->

Agora não marcamos mais nada

e o algoritmo temina fazendo fundindo os estados q 1 q 2 ; e fundindo os estados q 3 q 4 O diagrama de estados resultante é:

<!-- image -->

.

## Referências Bibliográficas