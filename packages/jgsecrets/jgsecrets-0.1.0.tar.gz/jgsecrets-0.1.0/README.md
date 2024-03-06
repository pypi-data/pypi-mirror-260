# APS2 - Criptografia com clone digital da máquina Enigma

A ideia de enviar mensagens que não podem ser interceptadas é muito antiga. Uma das técnicas mais antigas para isso é a cifra de substituição, que consiste em trocar as letras da mensagem de entrada por outras letra do alfabeto. Essa é uma técnica simples, cujo processo para codificação e decodificação é essencialmente o mesmo.

## Como implementar a máquina Enigma?

Afim de implementar a máquina Enigma utilizamos principalmente a biblioteca `numpy` e a técnica one-hot encoding.

O primeiro passo para transformar uma mensagem em Enigma é transformar nosso texto em uma matriz. Para isso, criamos uma matriz em que cada linha representa um elemento do alfabeto e cada coluna representa um elemento do texto. 

Assim, supondo que havíamos definido nosso alfabeto como "ABCD", poderíamos representar o texto "ABBA" desta forma:

$$
M = 
\begin{bmatrix}
    1 & 0 & 0 & 1 \\
    0 & 1 & 1 & 0 \\
    0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0
\end{bmatrix}
$$

Após transformarmos o nosso texto em uma matriz, precisamos embaralha-lo. Para isso, é necessário realizar uma série de multiplicações de matrizes. Assim, vamos criar duas matrizes permutações - a matriz E e a matriz P.

$$
P =
\begin{bmatrix}
0 & 0 & 1 & 0\\
1 & 0 & 0 & 0\\
0 & 0 & 0 & 1\\
0 & 1 & 0 & 0\\
\end{bmatrix}
$$

$$
E =
\begin{bmatrix}
    1 & 0 & 0 & 0 \\
    0 & 0 & 1 & 0 \\
    0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 1\\
\end{bmatrix}
$$

As matrizes permutações devem obrigatoriamente ter tamanho quadrado - ou seja, a mesma quantidade de linhas e colunas - e seu tamanho é definido pela quantidade de linhas que há na nossa matriz texto. 

Deste modo, o primeira multiplicação que devemos realizar é a matriz E pela matriz P - encontrando uma nova matriz P.

```math
\begin{bmatrix}
    1 & 0 & 0 & 0 \\
    0 & 0 & 1 & 0 \\
    0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
0 & 0 & 1 & 0\\
1 & 0 & 0 & 0\\
0 & 0 & 0 & 1\\
0 & 1 & 0 & 0
\end{bmatrix}
= 
\begin{bmatrix}
    0 & 0 & 1 & 0 \\
    0 & 0 & 0 & 1 \\
    1 & 0 & 0 & 0\\
    0 & 1 & 0 & 0
\end{bmatrix}
```

Após este passo, vamos realizar a multiplicação da nova matriz P por nossa matriz texto. 

```math
\begin{bmatrix}
    0 & 0 & 1 & 0 \\
    0 & 0 & 0 & 1 \\
    1 & 0 & 0 & 0\\
    0 & 1 & 0 & 0
\end{bmatrix}
\begin{bmatrix}
    1 & 0 & 0 & 1 \\
    0 & 1 & 1 & 0 \\
    0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0
\end{bmatrix}
=
\begin{bmatrix}
    0 & 0 & 0 & 0 \\
    0 & 0 & 0 & 0 \\
    1 & 0 & 0 & 1 \\
    0 & 1 & 1 & 0
\end{bmatrix}
```

Logo, o último passo para ter uma mensagem transformada em Enigma é voltar a nossa matriz para texto. Assim, obteríamos como novo texto "CDDC".

Entretanto, agora que codificamos uma mensagem, precisamos ser capazes de decifrá-las também. Afim de transformar um Enigma em um texto normal precisamos seguir passos semelhantes aos anteriores, com uma pequena mudança.

Assim que recebemos um Enigma, nosso primeiro passo é transformá-lo em one-hot. O passo seguinte também se mantém o mesmo, precisamos multiplicar nossa matriz permutação E pela matriz permutação P. Desta maneira, conseguimos encontrar a nova matriz P, ou seja, a matriz responsável por embaralhar nossa matriz texto e formar o Enigma que queremos decifrar.

A partir de agora precisamos realizar um novo passo, precisamos encontrar a inversa da nova matriz P e, depois, multiplicar a inversa da nova matriz P pela matriz enigma.

O esquema abaixp evidência o porquê de realizarmos a inversão da nova matriz P. 


```math
\begin{aligned}
P_n M & = E \\
P_n^{-1} P_n M & = P_n^{-1} E \\
I M & = P_n^{-1} E \\
M & = P_n^{-1} E
\end{aligned}
```

Seguindo este raciocínio, a nova matriz P multiplicada pela matriz texto equivale a nossa matriz Enigma. Assim, se multiplicarmos ambos os lados pela inversa da nova matriz P, encontramos uma matriz identidade no lado esquerdo. 

Uma matriz identidade se trata de uma matriz que, ao se realizar uma multiplicação de uma matriz identidade por qualquer outra matriz, teremos como resultado sempre a outra matriz. Deste modo, conseguimos recuperar nossa matriz texto.

Por último precisamos transformar nossa matriz texto em uma string novamente, retornando ao texto original "ABBA".


## Como usar nossa máquina Enigma?

1. Arquivo `demo.ipynb`


## Descrição do projeto
Neste projeto, faremos uma biblioteca Python para criptografia usando Enigma

A biblioteca deve conter:
* Uma função `para_one_hot(msg : str)` para codificar mensagens como uma matriz usando one-hot encoding
* Uma função `para_string(M : np.array)` para converter mensagens da representação one-hot encoding para uma string legível
* Uma função `cifrar(msg : str, P : np.array)` que aplica uma cifra simples em uma mensagem recebida como entrada e retorna a mensagem cifrada. `P` é a matriz de permutação que realiza a cifra.
* Uma função `de_cifrar(msg : str, P : np.array)` que recupera uma mensagem cifrada, recebida como entrada, e retorna a mensagem original. `P` é a matriz de permutação que realiza a cifra.
* Uma função `enigma(msg : str, P : np.array, E : np.array)` que faz a cifra enigma na mensagem de entrada usando o cifrador `P` e o cifrador auxiliar `E`, ambos representados como matrizes de permutação.
* Uma função `de_enigma(msg : str, P : np.array, E : np.array)` que recupera uma mensagem cifrada como enigma assumindo que ela foi cifrada com o usando o cifrador `P` e o cifrador auxiliar `E`, ambos representados como matrizes de permutação.

Anotações importantes:

1. O grupo deve enviar um link para o repositório GitHub onde está localizada a biblioteca.
2. No diretório principal do repositório, deve haver um programa `demo.py`, que, quando executado, demonstra o funcionamento de cada uma das funções da biblioteca


**ENTREGAS**
* Link para o repositório onde está a biblioteca.
* No `README.md` do repositório, deve haver uma discussão sobre que equações foram implementadas para realizar a criptografia e a de-criptografia com Enigma.
* Inclua também, no próprio `README.md`, instruções sobre como rodar o `demo.py` e como usar a biblioteca.
* Também, inclua instruções sobre como executar procedimentos de teste rápidos. Serão testados: mensagens normais, mensagens com caracteres que não fazem parte do alfabeto, mensagens vazias.

**RUBRICA**

O projeto será avaliado usando a rubrica abaixo. Os níveis são cumulativos, isto é, para passar de um nível, *todos* os requisitos dele devem ser cumpridos. As rubricas foram inspiradas nos níveis da [Taxonomia de Bloom](https://cft.vanderbilt.edu/guides-sub-pages/blooms-taxonomy/).

| Nível | Descrição | [Tax. de Bloom](https://cft.vanderbilt.edu/guides-sub-pages/blooms-taxonomy/) |
| --- | --- | --- |
| F | Não entregue, entregue sem completar o `README.md`, ou entregue sem implementar a criptografia Enigma | Não fez |
| E | Entregue, mas o `README.md` não indica como instalar ou rodar o programa. | Entender (-) |
| D | Roda com alguns travamentos ou erros ou o `README.md` não descreve o modelo matemático que foi aplicado. | Entender |
| C | Funciona sem travar e o `README.md` está completo, mas falha nos casos de teste descritos na entrega. | Compreender |
| B | A biblioteca funciona bem mas o código está muito confuso e sem comentários. | Aplicar |
| A | A biblioteca obedece a todos os requisitos e o código tem uma correspondência imediata ao modelo matemático descrito no `README.md` | Analisar |
| A+ | A biblioteca funciona perfeitamente e, em adição aos requisitos pedidos, tem um programa que permite que o algoritmo seja executado como uma API REST. | Analisar |
| A++ | A biblioteca funciona perfeitamente e, em adição aos requisitos anteriores, pode ser instalada usando `pip install .`. | Analisar |


