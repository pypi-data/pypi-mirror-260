# APS 2 - Gustavo Cruz e Ian Desponds


# O modelo matematico:

### Matrizes de permutação (P e E):
Primeiro, nós geramos um vetor de permutação de inteiros de 0 a 25 (assumindo um alfabeto de 26 caracteres), esse vetor vai determinar como as linhas da matriz identidade vão ser misturadas para formar as matrizes de permutação. A matriz identidade de tamanho 26x26 originalmente tem a forma: 
\[
I = \begin{bmatrix}
1 & 0 & 0 & \cdots & 0 \\
0 & 1 & 0 & \cdots & 0 \\
0 & 0 & 1 & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & \cdots & 1
\end{bmatrix}
\]
(apenas uns na diagonal principal e zeros no resto)

Após a multiplicação pela o vetor permutado, a matriz identidade vai virar uma matriz de permutação, que tem a forma:
\[
P/E = \begin{bmatrix}
0 & \cdots & 1 & \cdots & 0 \\
1 & \cdots & 0 & \cdots & 0 \\
0 & \cdots & 0 & \cdots & 1 \\
\vdots & \ddots & \vdots & \ddots & \vdots \\
0 & \cdots & 0 & \cdots & 0
\end{bmatrix}
\]

### Representando a mensagem como uma matriz:
Cada letra do alfabeto eh representada por uma matriz 26x1, onde todas as linahs têm valor 0, exceto no index correspondente à letra no dicionário. Por exemplo, a letra 'A' é representada pelo vetor:
\[
A = \begin{bmatrix}
1 \\
0 \\
0 \\
\vdots \\
0
\end{bmatrix}
\]
Dessa forma, a mensagem é representada por uma matriz 26xN, onde N é o número de letras na mensagem. Cada coluna dessa matriz é a representação matricial da letra correspondente da mensagem. A mensagem "ABC", por exemplo, seria representada pela matriz:
\[
M = \begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1 \\
\vdots & \vdots & \vdots \\
0 & 0 & 0
\end{bmatrix}
\]

## Enigma:
Para encriptar a mensagem, fazemos duas transformações na matriz M:

1. Multiplicamos a matriz M pela matriz de permutação P, que mistura as linhas da matriz M.
2. Multiplicamos a matriz resultante pela matriz de permutação E, que mistura as linhas da matriz resultante da primeira transformação.

Ou seja:
\[
M_{encriptada} = E \cdot P \cdot M
\]

Isso resulta em uma matriz 26xN que representa a mensagem encriptada, já que as letras da mensagem foram misturadas pelas matrizes de permutação P e E. 

## De_enigma:
Para decriptar a mensagem, fazemos duas transformações na matriz encriptada:

1. Multiplicamos a matriz encriptada pela inversa da matriz de permutação E (no caso de uma matriz de permutação, a inversa é a transposta da matriz). Esse processo reverte a ultima transformação feita (pela matriz E) na encriptação.
2. Após a primeira operação, ficamos com a matriz resultande da multiplicação de M pela matriz de permutação P. Para reverter essa transformação, multiplicamos a matriz resultante pela inversa da matriz de permutação P

Ou seja:
\[
M_{decriptada} = P^T \cdot E^T \cdot M_{encriptada}
\]

O resultado é a matriz original M, que representa a mensagem original (escrita ainda na forma one-hot).


# Como rodar o código:

1. Copie o link do repositório e clone no diretório desejado:
```git clone``` + link do repositório
2. Para rodar a demonstração do código, execute o arquivo ```demo.py```:
```python main.py```