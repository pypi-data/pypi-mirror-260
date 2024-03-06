from package.utils import matriz_identidade, alfabeto
import numpy as np

def para_one_hot(msg):
    response = []
    for char in msg: # Percorre todos os caracteres da mensagem
        for idx, letter in enumerate(alfabeto): # Percorre todas as letras do alfabeto e compara com as da mensagem
            if letter == char: # Caso seja igual adiciona o valor da letra criptografada na resposta
                response.append(matriz_identidade[idx])
    return np.transpose(response)

def para_string(one_hot):
    response = ""
    for i in range(one_hot.shape[1]): # Percorre todas as colunas da matriz one_hot
        for idx, letter in enumerate(matriz_identidade): # Percorre todas as letras criptografadas
            if np.array_equal(letter, one_hot[:,i]): # Compara a letra criptografada com a coluna da matriz one_hot
                response += alfabeto[idx] # Caso seja igual, adiciona a letra correspondente na resposta
    return response

def permuta_cifra(P):
    return np.random.permutation(P)

def cifrar(msg, P):
    msg = para_one_hot(msg)
    x = P @ msg
    return para_string(x), P

def de_cifrar(msg, P):
    msg = para_one_hot(msg)
    P = np.linalg.inv(P)
    x = P @ msg
    return para_string(x)

def enigma(msg, P, E):
    msg = para_one_hot(msg)
    X = P
    for i in range(len(msg[0])):
        if i == 0:
            msg[:,i] = P @ msg[:,i]
        else:
            X = E @ X 
            msg[:,i] = X @ msg[:,i]
    return para_string(msg), P, E

def desenigma(msg, P, E):
    msg = para_one_hot(msg)
    X = P
    for i in range(len(msg[0])):
        if i == 0:
            msg[:,i] = np.linalg.inv(P) @ msg[:,i]
        else:
            X = E @ X 
            msg[:,i] = np.linalg.inv(X) @ msg[:,i]
    return para_string(msg)
