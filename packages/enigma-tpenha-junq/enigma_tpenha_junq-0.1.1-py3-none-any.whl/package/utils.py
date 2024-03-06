import numpy as np
import string


alfabeto = list(string.ascii_letters)
alfabeto.append(" ")
alfabeto.append("!")
alfabeto.append("?")
alfabeto.append(".")
alfabeto.append(",")
alfabeto.append(":")

tamanho = len(alfabeto)

# Criando a matriz identidade usando a função np.eye() do numpy
matriz_identidade = np.eye(tamanho)

# Convertendo a matriz identidade em uma lista de listas
matriz_identidade_lista = matriz_identidade.tolist()