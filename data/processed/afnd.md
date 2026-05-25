## Autˆ omato Finito n˜ ao-Determin´ ıstico

Um AFD ´ e uma m´ aquina determin´ ıstica : a partir de um estado e um s´ ımbolo, sabemos qual ´ e o pr´ oximo estado usando uma fun¸ c˜ ao de transi¸ c˜ ao δ ( p, a ) = q : isto ´ e chamdo computa¸ c˜ ao determin´ ıstica . Um autˆ omato finito n˜ ao determin´ ıstico (AFND) ´ e uma m´ aquina n˜ ao determin´ ıstica : podemos ter zero ou mais op¸ c˜ oes para o pr´ oximo estado e, alguma vezes, muda de estado sem mesmo ler um s´ ımbolo: isto ´ e chamado computa¸ c˜ ao n˜ ao determin´ ıstica .

Exemplo 1. Antes de definir precisamente um AFND vejamos o seguinte diagrama N que aceitas cadeias terminadas em 11 e 101.

<!-- image -->

Os r´ otulos das 'setas' s˜ ao s´ ımbolos em Σ ϵ := Σ ∪{ ε } onde ε ̸∈ Σ e representa uma transi¸ c˜ ao que pode ocorrer sem a leitura de um s´ ımbolo. Setas que tem somente ϵ como r´ otulo s˜ ao ditas transi¸ c˜ oes vazias .

Essa m´ aquina permite diferentes op¸ c˜ oes para uma computa¸ c˜ ao. Por exemplo, suponha que usamos N para computar a cadeia 010110 . Temos diferentes possibilidades para a sua computa¸ c˜ ao conforme podemos observar no diagrama a seguir.

<!-- image -->

Nesse modelo, ao se processar uma cadeia x , o AFND aceita x se existe uma computa¸ c˜ ao que processa toda a cadeia x alcan¸ cando um estado de aceita¸ c˜ ao.

Como exemplo, considere a linguagem

<!-- formula-not-decoded -->

A figura a seguir mostra um AFND N que aceita exatamente as cadeias de A . Note que N possui o estado inicial q 0 . Este autˆ omato n˜ ao ´ e determin´ ıstico, pois h´ a duas transi¸ c˜ oes a partir de q 0 para o s´ ımbolo 1 e n˜ ao h´ a nenhuma transi¸ c˜ ao a partir de q 5 . Este AFND reconhece a linguagem A , pois para qualquer cadeia x cuja quinta letra ´ e 1, h´ a uma sequencia de transi¸ c˜ oes a partir de q 0 at´ e q 5 . Nenhuma outra cadeia ´ e aceita.

<!-- image -->

## Defini¸ c˜ ao formal

Para um s´ ımbolo ε ̸∈ Σ, seja Σ ε = Σ ∪{ ε } . Um autˆ omato finito n˜ ao determin´ ıstico (AFND) ´ e uma qu´ ıntupla

<!-- formula-not-decoded -->

onde

- · Q : conjunto finito de estados ;
- · Σ: conjunto finito de s´ ımbolos -alfabeto de entrada ;
- · δ : Q × Σ ε → 2 Q : fun¸ c˜ ao de transi¸ c˜ ao ;
- · q 0 ∈ Q ´ e o estado inicial ;
- · F ⊆ Q : estados finais ou de aceita¸ c˜ ao .

Seja N = ( Q, Σ , δ, q 0 , F ) um AFND x uma cadeia sobre Σ e p, q ∈ Q . Um elemento do conjunto p ∈ ∆( q, x ) se podemos escrever x = x 1 x 2 . . . x m onde x i ∈ Σ ε e existe uma sequˆ encia de estados r 0 , r 1 , . . . , r m em Q com

- 1. r 0 = q e
- 2. r i ∈ δ ( r i -1 , x i ) para cada i = 1 , 2 , . . . , m .

̸

Escrevemos simplesmente ∆( x ) em vez de ∆( q, x ) se q ´ e o estado inicial. Dizemos que N aceita x se ∆( x ) ∩ F = ∅ ; caso contr´ ario dizemos que N rejeita x . Alinguagem de todas as cadeias aceitas por N ´ e denotada por L ( N ); e dizemos que N reconhece a linguagem L ( N ). Escrevemos N ( x ) = aceita se x ∈ L ( N ) e N ( x ) = rejeita caso contr´ ario.

## Exemplo

Note que, exceto pela fun¸ c˜ ao de transi¸ c˜ ao, a defini¸ c˜ ao de AFD ´ e a mesma de um AFND. A diferen¸ ca na fun¸ c˜ ao de transi¸ c˜ ao tornam muito diferentes essas m´ aquinas.

Como exemplo, considere novamente o AFND

Nesse caso,

- · Q = { q 0 , q 1 , q 2 , q 3 } ;
- · Σ = { 0 , 1 } ;

•

- · q 0 ´ e o estado inicial;
- · F = { q 3 } .

## Equivalˆ encia entre AFD e AFND

Mostrar a equivalˆ encia entre AFD e AFND corresponde a mostrar que tudo o que pode ser computado por um AFD tamb´ em pode ser computado por um AFND e vice-versa. Para mostrar essa equivalˆ encia vamos construir, a partir de um AFD M , um AFND que reconhece L ( M ) e depois vamos construir, a partir de um AFND N , um AFD que reconhece L ( N ). Antes por´ em vamos fazer a seguinte defini¸ c˜ ao para lidar com as transi¸ c˜ oes vazias.

Seja q um estado de um AFND ( Q, Σ , δ, q 0 , F ) Definimos

<!-- formula-not-decoded -->

Ou seja, E ( q ) corresponde aos estados que podem ser atingidos a partir de q (inclusive) viajando-se ao longo de zero ou mais transi¸ c˜ oes vazias.

Teorema 1. Seja A uma linguagem. Existe um AFD que reconhece A se e somente se existe um AFND que reconhece A .

<!-- image -->

Prova . Mostrar que se existe um AFD que reconhece A , ent˜ ao existe um AFND que reconhece A ´ e imediato, pois h´ a uma maneira trivial de transformar um AFD em um AFND.

Suponha ent˜ ao que existe um AFND N = ( Q, Σ ϵ , δ, q 0 , F ) que reconhece a linguagem A . Verifique que o AFD ( Q ′ , Σ , δ ′ , q ′ 0 , F ′ ) tal que

- 1. Q ′ := 2 Q ;
- 2. δ ′ ( S, a ) = ∪ p ∈ S E ( δ ( p, a )) para todo S ∈ Q ′ e a ∈ Σ;
- 3. q ′ 0 := E ( q 0 );
- 4. F ′ := { S ∈ Q ′ : S ∩ F = ∅ . } .

tamb´ em reconhece A .

□

Corol´ ario 1. Uma linguagem ´ e regular se e somente se existe um AFND que a reconhe¸ ca.

## Exerc´ ıcios

- 1. Fa¸ ca um diagrama dos AFNDs que reconhecem as linguagens a seguir. Procure tirar proveito do n˜ ao-determinismo tanto quanto poss´ ıvel:
- (a) { x ∈ { 0 , 1 } ∗ : x = 1 y 0 para algum y ∈ { 0 , 1 } ∗ } .
- (b)
- { x ∈ { 0 , 1 } ∗ : y 1 1 y 2 1 y 3 1 y 4 para y i ∈ { 0 , 1 } ∗ } .
- (c)
- (d)
- { x ∈ { 0 , 1 } ∗ : y 1 0101 y 2 para y i ∈ { 0 , 1 } ∗ } .
- { x ∈ { 0 , 1 } ∗ : | x | ≥ 3 e seu terceiro s´ ımbolo ´ e 0 . } .
- (e) { x ∈ { 0 , 1 } ∗ : | x | mod 2 = 0 e x = 0 y para algum y ∈ { 0 , 1 } ∗ ; ou x ∈ { 0 , 1 } ∗ : | x | mod 2 = 1 e x = 1 y para algum y ∈ { 0 , 1 } ∗ } .
- (f) { x ∈ { 0 , 1 } ∗ : x cont´ em a subcadeia 110 } .
- (g) { ϵ, 0 } ;
- (h) { x ∈ { 0 , 1 } ∗ : | x | 0 } .

̸

- (i) ∅ .
- (j) Todas as cadeias em { 0 , 1 } ∗ , exceto a cadeia vazia.
- (k) O conjunto de cadeias sobre o alfabeto { 0 , 1 , . . . , 9 } tal que o ´ ultimo d´ ıgito da cadeia tenha pelo menos outra ocorrˆ encia na cadeia.
- (l) O conjunto de cadeias sobre o alfabeto { 0 , 1 , 2 , 3 , 4 } tal que o ´ ultimo d´ ıgito da cadeia n˜ ao tenha outra ocorrˆ encia na cadeia.
- (m) O conjunto de cadeias sobre o alfabeto { 0 , 1 } tal que, em qualquer cadeia, n˜ ao h´ a dois 0's separados por um n´ umero de posi¸ c˜ oes que seja m´ ultiplo de 4. Observe que 0 ´ e um m´ ultiplo de 4.
- 2. Mostre um diagrama de transi¸ c˜ ao de um AFND

<!-- formula-not-decoded -->

tal que Q possui exatamente quatro estados e que L ( N ) ´ e igual ` a linguagem

<!-- formula-not-decoded -->

definida sobre o alfabeto { 0 , 1 } .

- 3. Seja A ⊆ { a, b, c } ∗ a linguagem consistindo de todas as cadeias x sobre { a, b, c } que possuem um n´ umero ´ ımpar de a 's ou um n´ umero ´ ımpar de b 's ou um n´ umero ´ ımpar de c 's; isto ´ e,

<!-- formula-not-decoded -->

Ent˜ ao,

- (a) Especifique um AFND N com no m´ aximo 7 estados tal que A = L ( N ).
- (b) Vocˆ e consegue especificar um AFD D com 7 estados ou menos tal que A = L ( D )? Em caso afirmativo, especifique D . Caso contr´ ario, explique (informalmente) porque tal AFD n˜ ao existe.
- 4. Seja Σ = { a 1 , . . . , a n } um alfabeto com n letras, para algum n ∈ Z e n ≥ 1. Ent˜ ao considere a linguagem A n que consiste de todas as cadeias sobre Σ que possuem um n´ umero´ ımpar de letras a i , para algum i ∈ { 1 , . . . , n } . Isto ´ e, para cada i ∈ { 1 , . . . , n } , se A i n ´ e a linguagem de todas as cadeias sobre Σ com um n´ umero ´ ımpar de letras a i , ent˜ ao A n = A 1 n ∪ A 2 n ∪ · · · A n n = ⋃ n i =1 A i n .
- (a) Especifique um AFND N com 2 n ou 2 n +1 estados tal que L ( N ) = A n .

- (b) Mostre que h´ a um AFD M com 2 n estados tal que L ( M ) = A n .
- (c) Mostre que qualquer AFD M tal que L ( M ) = A n possui pelo menos 2 n estados.
- 5. Considere a seguinte afirma¸ c˜ ao: Seja N um AFND que possui n estados e que n˜ ao existe AFND com menos estados que reconhece L ( N ) . Ent˜ ao, um AFD que reconhece L ( N ) deve possui pelo menos log n estados. Essa afirma¸ c˜ ao ´ e correta? Justifique sua resposta.
- 6. Mostre que para qualquer linguagem regular A , existe um AFND com um ´ unico estado de aceita¸ c˜ ao que reconhece A .

## Referˆ encias Bibliogr´ aficas