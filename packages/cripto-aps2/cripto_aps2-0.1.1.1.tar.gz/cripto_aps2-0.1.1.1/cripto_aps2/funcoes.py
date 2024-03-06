import numpy as np
from random import randint
from flask import Flask, request, jsonify

super_alfabeto = "AÁÀÂÃÄBCÇDEÉÈÊËFGHIÍÌÎÏJKLMNOÓÒÔÕÖPQRSTUÚÙÛÜVWXYZ aáàâãäbcçdeéèêëfghiíìîïjklmnoóòôõöpqrstuúùûüvwxyz,.!@#$%&*?+-/][}{\|1234567890"  # Alfabeto + espaço


def verifica_mensagem (mensagem):
    super_alfabeto = "AÁÀÂÃÄBCÇDEÉÈÊËFGHIÍÌÎÏJKLMNOÓÒÔÕÖPQRSTUÚÙÛÜVWXYZ aáàâãäbcçdeéèêëfghiíìîïjklmnoóòôõöpqrstuúùûüvwxyz,.!@#$%&*?+-/][}{\|1234567890"  # Alfabeto + espaço
    for i in range(len(mensagem)):
        if mensagem[i] not in super_alfabeto:
            return False
    return True


def indice_letra(letra):
    alfabeto = "AÁÀÂÃÄBCÇDEÉÈÊËFGHIÍÌÎÏJKLMNOÓÒÔÕÖPQRSTUÚÙÛÜVWXYZ aáàâãäbcçdeéèêëfghiíìîïjklmnoóòôõöpqrstuúùûüvwxyz,.!@#$%&*?+-/][}{\|1234567890"  # Alfabeto + espaço
    if letra in alfabeto: # Verifica se a letra está no alfabeto
        return alfabeto.index(letra) # Retorna o índice da letra no alfabeto
    return None

def letra_numero(indice):
    alfabeto = "AÁÀÂÃÄBCÇDEÉÈÊËFGHIÍÌÎÏJKLMNOÓÒÔÕÖPQRSTUÚÙÛÜVWXYZ aáàâãäbcçdeéèêëfghiíìîïjklmnoóòôõöpqrstuúùûüvwxyz,.!@#$%&*?+-/][}{\|1234567890"  # Alfabeto + espaço
    letra = alfabeto[indice]   # Retorna a letra correspondente ao índice
    return letra  # Retorna a letra correspondente ao índice

def para_one_hot(msg : str):
    matriz_one_hot = np.zeros((len(msg), 128)) # Cria uma matriz de zeros com o tamanho da mensagem
    for i, letra in enumerate(msg): # Itera sobre a mensagem
        indice = indice_letra(letra) # Converte a letra para o índice correspondente
        if indice is not None: # Verifica se a letra está no alfabeto
            matriz_one_hot[i][indice] = 1 # Atribui 1 na posição correspondente ao índice da letra
    return matriz_one_hot # Retorna a matriz one-hot

def para_string(M: np.array):
    string = "" # Inicializa a string   
    for i in M:  # Itera sobre as linhas da matriz
        indice_do_1 = np.argmax(i)  # Retorna o índice do 1 na linha
        string += letra_numero(indice_do_1)  # Adiciona a letra correspondente ao índice na string
    return string  # Retorna a string

def cifrar(msg: str, P: np.array):
    matriz = para_one_hot(msg)  # Converte a mensagem para matriz one-hot
    return para_string(np.dot(matriz, P))  # Retorna a mensagem cifrada

def de_cifrar(msg:str, P:np.array):
    msg = para_one_hot(msg)
    msg = msg@np.linalg.inv(P)
    return para_string(msg)


def enigma(msg: str, P: np.array, E: np.array):
    matriz_msg = para_one_hot(msg)  # Converte a mensagem para matriz one-hot
    matriz_enigma = P  # A matriz enigma começa com a matriz P
    nova_msg = []  # Inicializa a lista para a nova mensagem
    for i in range(len(msg)):  
        letra = matriz_msg[i]  # Pega a letra correspondente na matriz
        letra_codificada = matriz_enigma@letra  # Codifica a letra com a matriz enigma
        matriz_enigma = E@matriz_enigma  # Multiplica a matriz enigma pela matriz E
        nova_msg.append(letra_codificada)  # Adiciona a letra codificada na lista
    nova_msg = np.array(nova_msg)  # Converte a lista para um array
    return para_string(nova_msg)  # Retorna a nova mensagem

def de_enigma(msg: str, P: np.array, E: np.array):
    matriz_msg = para_one_hot(msg)  # Converte a mensagem para matriz one-hot
    matriz_enigma = P  # A matriz enigma começa com a matriz P
    nova_msg = []  # Inicializa a lista para a nova mensagem
    for i in range(len(msg)):  # Itera sobre a mensagem
        letra = matriz_msg[i]  # Pega a letra correspondente na matriz
        letra_decodificada = np.linalg.inv(matriz_enigma)@letra  # Decodifica a letra com a matriz enigma
        matriz_enigma = E@matriz_enigma  # Multiplica a matriz enigma pela matriz E
        nova_msg.append(letra_decodificada)  # Adiciona a letra decodificada na lista
    nova_msg = np.array(nova_msg)  # Converte a lista para um array
    return para_string(nova_msg)  # Retorna a nova mensagem



def embaralha_alfabeto(alfabeto, seed):
    alfabeto = list(alfabeto)  # Converte o alfabeto para uma lista
    np.random.seed(seed)  # Seta a seed
    np.random.shuffle(alfabeto)  # Embaralha o alfabeto
    return ''.join(alfabeto)  # Retorna o alfabeto embaralhado
