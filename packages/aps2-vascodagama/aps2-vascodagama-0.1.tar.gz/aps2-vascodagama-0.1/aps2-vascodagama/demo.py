import numpy as np

def para_one_hot(string):
    # Matriz resposta
    matriz_one_hot = []
    alfabeto = "abcdefghijklmnopqrstuvwxyz"

    # Cria um array de zeros com 26 posições
    matriz_zeros = np.zeros(26)

    # Para cada caractere na string recebida
    for caractere in string:
        # Para cada índice e letra do alfabeto
        for indice, letra in enumerate(alfabeto):
            # Se o caractere for igual a letra
            if caractere == letra:
                matriz_zeros[indice] = 1
                matriz_one_hot.append(matriz_zeros)
                matriz_zeros = np.zeros(26)

    # Retorna a matriz one-hot já transposta
    return np.array(matriz_one_hot).T


def para_string(array_p):
    # String resposta
    strDecodificada = ""
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    
    # Transpõe a matriz codificada
    matrizCodificada = array_p.T
    
    # Para cada linha da matriz
    for linha in matrizCodificada:
        # Para cada caractere da linha 
        for indice, caractere in enumerate(linha):
            if caractere == 1:
                strDecodificada += alfabeto[indice]

    return strDecodificada

def cifrar(string, array_p):
    return None

def de_cifrar(string, array_p):
    return None

def enigma(string, array_p, array_e):
    return None

def de_enigma(string, array_p, array_e):
    return None




print(para_one_hot('vasco'))       