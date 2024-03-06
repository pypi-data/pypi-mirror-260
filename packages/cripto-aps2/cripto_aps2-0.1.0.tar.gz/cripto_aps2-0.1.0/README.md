# aps2-AlgLin

# Projeto: Criptografia usando enigma

## Introdução
O objetivo deste projeto é desenvolver uma biblioteca contendo funções que permitam a cifragem de mensagens usando enigmas através de uma API rest. Além disso, a biblioteca deve fornecer funcionalidades capazes de encriptar e desencriptar essas mensagens.

## Intalação 
Para rodar o jogo, siga os seguintes passos:
### 1. Baixe o Zip ou clone o repositório
- Nesse link https://github.com/giovannyjvr/aps1-AlgLin, abre a pagina github do projeto, no botão VERDE (Code),  abre a possibilidade de fazer o download por zip de todo o projeto. Portanto:
    ° Botão verde (Code)
    ° Local
    ° HTTPS
    ° Download ZIP

### Descompactando ZIP
- Clique com o botão direito no arquivo.
- Clique em "Extrair Tudo".

### Acessando Jogo
- Clique com botão direito na pasta.
- Clique em "Abrir no Terminal".
#### Instalações necessárias
- execute o seguinte comando :
  pip install -r requirements.txt

#### Jogue
- Execute o seguinte comando para acessar o jogo:
    python jogo.py


## Funções
`para_one_hot(msg : str)`
- A função para_onde_hot recebe uma mensagem no formato de string e deve retornar


## A criptografia e a de-criptografia com Enigma

A função de criptografia com Enigma recebe como argumentos: a mensagem a ser codificada, um P e um E.
P é uma matriz 128x95 uma matriz identidade permutada criada a partir da função para_one_hot que, a partir de um alfabeto ebaralhado, cria uma matriz de 128x95 pois o alfabeto utilizado possui 95 caracteres distintos.
E é uma matriz no mesmo formato da matriz P que servirá para alterar a matriz P.

### Crptografia
1. Codifica a mensagem usando a função para_one_hot, resultando em uma matriz com a mesma quantidade de linhas e colunas das matrizes E e P.
2. Para cada letra da mensagem(cada coluna da matriz da mensagem codificada), é feita uma multiplicação de matrizes da letra pela matriz P a fim de shifftar a posição do 1 ("embaralhar").
3. Adiciona a matriz resultante em um array 
4. Multiplica a matriz P pela matriz E, seguindo a mesma lógica a fim de embaralhar P também para deixar a criptografia mais complexa e volta para o passo 2



Obs: Exemplo da multiplicação por uma matriz permutada(P) a fim de shifftar outra matriz.
$$
\begin{bmatrix}
0 & 0 & 1 \\
1 & 0 & 0 \\
0 & 1 & 0 
\end{bmatrix}
\begin{bmatrix}
    1 &  1 & 0 & 0 & 0 & 0 \\
    0 &  0 & 1 & 1 & 0 & 0 \\
    0 &  0 & 0 & 0 & 1 & 1 
\end{bmatrix}
= 
\begin{bmatrix}
    0 &  0 & 0 & 0 & 1 & 1 \\
    1 &  1 & 0 & 0 & 0 & 0 \\
    0 &  0 & 1 & 1 & 0 & 0 
\end{bmatrix}
$$

### De-criptografia

A função de de-criptografia com Enigma recebe como argumentos: a mensagem criptografada, um P e um E.
1. Codifica a mensagem usando a função para_one_hot, resultando em uma matriz com a mesma quantidade de linhas e colunas das matrizes E e P.
2. Para cada letra da mensagem(cada coluna da matriz da mensagem codificada), é feita uma multiplicação da inversa da matriz P pela matriz da letra
3. Multiplica a matriz P pela matriz E para chegar na mesma matriz que codificou a próxima letra e retorna para o passo 2

Explicação da multiplicação:

$
\begin{aligned}                         
P M & = M_c \\                          
P^{-1} P M & = P^{-1} M_c \\             
I M & = P^{-1} M_c \\                   
M & = P^{-1} M_c                        
\end{aligned}
$

Multiplicar uma matriz pela sua inverso é equivalente a multiplicar pela matriz identidade. Dessa forma, podemos manipular a equação para voltar a matriz original da letra.


### Demo.py
Demo.py é o arquivo criado para testar o programa e cada função separadamente. 
execute no terminal:
python demo.py
siga as instruções da interação e teste as funções. 
