## Autômato Finito não-Determinístico

Um AFD é uma máquina determinística : a partir de um estado e um símbolo, sabemos qual é o próximo estado usando uma função de transição δ ( p, a ) = q : isto é chamdo computação determinística . Um autômato finito não determinístico (AFND) é uma máquina não determinística : podemos ter zero ou mais opções para o próximo estado e, alguma vezes, muda de estado sem mesmo ler um símbolo: isto é chamado computação não determinística .

Exemplo 1. Antes de definir precisamente um AFND vejamos o seguinte diagrama N que aceitas cadeias terminadas em 11 e 101.

<!-- image -->

Os rótulos das 'setas' são símbolos em Σ ϵ := Σ ∪{ ε } onde ε ̸∈ Σ e representa uma transição que pode ocorrer sem a leitura de um símbolo. Setas que tem somente ϵ como rótulo são ditas transições vazias .

Essa máquina permite diferentes opções para uma computação. Por exemplo, suponha que usamos N para computar a cadeia 010110 . Temos diferentes possibilidades para a sua computação conforme podemos observar no diagrama a seguir.

<!-- image -->

Nesse modelo, ao se processar uma cadeia x , o AFND aceita x se existe uma computação que processa toda a cadeia x alcançando um estado de aceitação.

Como exemplo, considere a linguagem

A figura a seguir mostra um AFND N que aceita exatamente as cadeias de A . Note que N possui o estado inicial q 0 . Este autômato não é determinístico, pois há duas transições a partir de q 0 para o símbolo 1 e não há nenhuma transição a partir de q 5 . Este AFND reconhece a linguagem A , pois para qualquer cadeia x cuja quinta letra é 1, há uma sequencia de transições a partir de q 0 até q 5 . Nenhuma outra cadeia é aceita.

<!-- image -->

## Definição formal

Para um símbolo ε ̸∈ Σ, seja Σ ε = Σ ∪{ ε } . Um autômato finito não determinístico (AFND) é uma quíntupla

onde

- · Q : conjunto finito de estados ;
- · Σ: conjunto finito de símbolos -alfabeto de entrada ;
- · δ : Q × Σ ε → 2 Q : função de transição ;
- · q 0 ∈ Q é o estado inicial ;
- · F ⊆ Q : estados finais ou de aceitação .

Seja N = ( Q, Σ , δ, q 0 , F ) um AFND x uma cadeia sobre Σ e p, q ∈ Q . Um elemento do conjunto p ∈ ∆( q, x ) se podemos escrever x = x 1 x 2 . . . x m onde x i ∈ Σ ε e existe uma sequência de estados r 0 , r 1 , . . . , r m em Q com

- 1. r 0 = q e
- 2. r i ∈ δ ( r i -1 , x i ) para cada i = 1 , 2 , . . . , m .

̸

Escrevemos simplesmente ∆( x ) em vez de ∆( q, x ) se q é o estado inicial. Dizemos que N aceita x se ∆( x ) ∩ F = ∅ ; caso contrário dizemos que N rejeita x . Alinguagem de todas as cadeias aceitas por N é denotada por L ( N ); e dizemos que N reconhece a linguagem L ( N ). Escrevemos N ( x ) = aceita se x ∈ L ( N ) e N ( x ) = rejeita caso contrário.

## Exemplo

Note que, exceto pela função de transição, a definição de AFD é a mesma de um AFND. A diferença na função de transição tornam muito diferentes essas máquinas.

Como exemplo, considere novamente o AFND

Nesse caso,

- · Q = { q 0 , q 1 , q 2 , q 3 } ;
- · Σ = { 0 , 1 } ;

•

- · q 0 é o estado inicial;
- · F = { q 3 } .

## Equivalência entre AFD e AFND

Mostrar a equivalência entre AFD e AFND corresponde a mostrar que tudo o que pode ser computado por um AFD também pode ser computado por um AFND e vice-versa. Para mostrar essa equivalência vamos construir, a partir de um AFD M , um AFND que reconhece L ( M ) e depois vamos construir, a partir de um AFND N , um AFD que reconhece L ( N ). Antes porém vamos fazer a seguinte definição para lidar com as transições vazias.

Seja q um estado de um AFND ( Q, Σ , δ, q 0 , F ) Definimos

Ou seja, E ( q ) corresponde aos estados que podem ser atingidos a partir de q (inclusive) viajando-se ao longo de zero ou mais transições vazias.

Teorema 1. Seja A uma linguagem. Existe um AFD que reconhece A se e somente se existe um AFND que reconhece A .

<!-- image -->

Prova . Mostrar que se existe um AFD que reconhece A , então existe um AFND que reconhece A é imediato, pois há uma maneira trivial de transformar um AFD em um AFND.

Suponha então que existe um AFND N = ( Q, Σ ϵ , δ, q 0 , F ) que reconhece a linguagem A . Verifique que o AFD ( Q ′ , Σ , δ ′ , q ′ 0 , F ′ ) tal que

- 1. Q ′ := 2 Q ;
- 2. δ ′ ( S, a ) = ∪ p ∈ S E ( δ ( p, a )) para todo S ∈ Q ′ e a ∈ Σ;
- 3. q ′ 0 := E ( q 0 );
- 4. F ′ := { S ∈ Q ′ : S ∩ F = ∅ . } .

também reconhece A .

□

Corolário 1. Uma linguagem é regular se e somente se existe um AFND que a reconheça.

## Exercícios

- 1. Faça um diagrama dos AFNDs que reconhecem as linguagens a seguir. Procure tirar proveito do não-determinismo tanto quanto possível:
- (a) { x ∈ { 0 , 1 } ∗ : x = 1 y 0 para algum y ∈ { 0 , 1 } ∗ } .
- (b)
- { x ∈ { 0 , 1 } ∗ : y 1 1 y 2 1 y 3 1 y 4 para y i ∈ { 0 , 1 } ∗ } .
- (c)
- (d)
- { x ∈ { 0 , 1 } ∗ : y 1 0101 y 2 para y i ∈ { 0 , 1 } ∗ } .
- { x ∈ { 0 , 1 } ∗ : | x | ≥ 3 e seu terceiro símbolo é 0 . } .
- (e) { x ∈ { 0 , 1 } ∗ : | x | mod 2 = 0 e x = 0 y para algum y ∈ { 0 , 1 } ∗ ; ou x ∈ { 0 , 1 } ∗ : | x | mod 2 = 1 e x = 1 y para algum y ∈ { 0 , 1 } ∗ } .
- (f) { x ∈ { 0 , 1 } ∗ : x contém a subcadeia 110 } .
- (g) { ϵ, 0 } ;
- (h) { x ∈ { 0 , 1 } ∗ : | x | 0 } .

̸

- (i) ∅ .
- (j) Todas as cadeias em { 0 , 1 } ∗ , exceto a cadeia vazia.
- (k) O conjunto de cadeias sobre o alfabeto { 0 , 1 , . . . , 9 } tal que o último dígito da cadeia tenha pelo menos outra ocorrência na cadeia.
- (l) O conjunto de cadeias sobre o alfabeto { 0 , 1 , 2 , 3 , 4 } tal que o último dígito da cadeia não tenha outra ocorrência na cadeia.
- (m) O conjunto de cadeias sobre o alfabeto { 0 , 1 } tal que, em qualquer cadeia, não há dois 0's separados por um número de posições que seja múltiplo de 4. Observe que 0 é um múltiplo de 4.
- 2. Mostre um diagrama de transição de um AFND

tal que Q possui exatamente quatro estados e que L ( N ) é igual à linguagem

definida sobre o alfabeto { 0 , 1 } .

- 3. Seja A ⊆ { a, b, c } ∗ a linguagem consistindo de todas as cadeias x sobre { a, b, c } que possuem um número ímpar de a 's ou um número ímpar de b 's ou um número ímpar de c 's; isto é,

Então,

- (a) Especifique um AFND N com no máximo 7 estados tal que A = L ( N ).
- (b) Você consegue especificar um AFD D com 7 estados ou menos tal que A = L ( D )? Em caso afirmativo, especifique D . Caso contrário, explique (informalmente) porque tal AFD não existe.
- 4. Seja Σ = { a 1 , . . . , a n } um alfabeto com n letras, para algum n ∈ Z e n ≥ 1. Então considere a linguagem A n que consiste de todas as cadeias sobre Σ que possuem um númeroímpar de letras a i , para algum i ∈ { 1 , . . . , n } . Isto é, para cada i ∈ { 1 , . . . , n } , se A i n é a linguagem de todas as cadeias sobre Σ com um número ímpar de letras a i , então A n = A 1 n ∪ A 2 n ∪ · · · A n n = ⋃ n i =1 A i n .
- (a) Especifique um AFND N com 2 n ou 2 n +1 estados tal que L ( N ) = A n .

- (b) Mostre que há um AFD M com 2 n estados tal que L ( M ) = A n .
- (c) Mostre que qualquer AFD M tal que L ( M ) = A n possui pelo menos 2 n estados.
- 5. Considere a seguinte afirmação: Seja N um AFND que possui n estados e que não existe AFND com menos estados que reconhece L ( N ) . Então, um AFD que reconhece L ( N ) deve possui pelo menos log n estados. Essa afirmação é correta? Justifique sua resposta.
- 6. Mostre que para qualquer linguagem regular A , existe um AFND com um único estado de aceitação que reconhece A .

## Referências Bibliográficas