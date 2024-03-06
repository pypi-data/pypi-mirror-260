import numpy as np

def para_one_hot(msg):
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    alfabeto_matriz = np.eye(26, dtype=int)

    indices = []
    msg_matriz = []

    for i in range(len(msg)):
        if msg[i] not in alfabeto:
            return "Alguns dos caracteres da mensagem não estão no alfabeto. Por favor, insira apenas letras minúsculas.", False
        for j in range(len(alfabeto)):
            if msg[i] == alfabeto[j]:
                indices.append(j)

   
    for indice in indices:
        coluna = []
        for linha in alfabeto_matriz:
            coluna.append(linha[indice])
        msg_matriz.append(coluna)
 

    msg_matriz = np.array(msg_matriz)
    msg_matriz = msg_matriz.transpose()

    # if len(msg_matriz) ==0:
    #     return "Alguns dos caracteres da mensagem não estão no alfabeto. Por favor, insira apenas letras minúsculas."
    
    return msg_matriz, True


def para_string(M):
   
    string = ''
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'

    for tamanho in range(len(M[0])):
        for letra in range(len(M)):
            if M[letra][tamanho] == 1:
                string += alfabeto[letra]
                
    return string

def cifrar(msg, P):
    msg_matriz, validacao = para_one_hot(msg)
    matriz_cifrada = np.dot(P, msg_matriz)
    msg_cifrada = para_string(matriz_cifrada)

    return msg_cifrada


def de_cifrar(msg, P):

    P_inversa = np.linalg.inv(P)
    msg_matriz, validacao = para_one_hot(msg)
    matriz_decifrada = np.dot(P_inversa, msg_matriz)
    msg_original = para_string(matriz_decifrada)

    return msg_original

def enigma(msg, P, E):

    msg_matriz, validacao = para_one_hot(msg)
    msg_cifrada = msg_matriz

    for j in range(len(msg_matriz[0])):
        n_msg = np.dot(P, msg_cifrada)
        for i in range (len(msg_matriz)):
            msg_cifrada[i][j] = n_msg[i][j]
        P = np.dot(P, E)

    msg_cifrada = para_string(msg_cifrada)

    return msg_cifrada

def de_enigma(msg, P, E):
    
    P_inv = np.linalg.inv(P)
    E_inv = np.linalg.inv(E)
  
    msg_matriz, validacao = para_one_hot(msg)
    msg_decifrada = msg_matriz

    for j in range(len(msg_matriz[0])):

        n_msg = np.dot(P_inv, msg_decifrada)
        for i in range(len(msg_matriz)):
            msg_decifrada[i][j] = n_msg[i][j]
        P_inv = np.dot(P_inv, E_inv)

    msg_original = para_string(msg_decifrada)

    return msg_original

