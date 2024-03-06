import numpy as np

alfabeto_normal = "abcdefghijklmnopqrstuvwxyzçáâãàéêíóôõú,.;:!?- "

def para_one_hot(msg:str):
    '''
    Para codificar mensagens como uma matriz usando one-hot encoding
    '''
    msg = msg.lower()
    one_hot = np.zeros((len(alfabeto_normal), len(msg)))

    for i in range(len(msg)):
        one_hot[alfabeto_normal.index(msg[i]), i] = 1
    return one_hot

def para_string(M:np.array):
    '''
    Da matriz para letrinha.
    Para converter mensagens da representação one-hot encoding para uma string legível.
    '''
    msg = ""
    for i in range(M.shape[1]):
        msg += alfabeto_normal[np.argmax(M[:, i])] #argmax retorna o indice do maior valor e uso para encontrar a letra correspondente
    return msg

def cifrar(msg:str, P:np.array):
    '''
    Uma função que aplica uma cifra simples em uma mensagem recebida como entrada e retorna a mensagem cifrada. `P` é a matriz de permutação que realiza a cifra.
    '''
    msg = msg.lower()
    one_hot = para_one_hot(msg)

    one_hot_cifrada = P @ one_hot
    msg_cifrada = para_string(one_hot_cifrada)
    
    return msg_cifrada

def de_cifrar(msg:str, P:np.array):
    '''
    Uma função que recupera uma mensagem cifrada, recebida como entrada, e retorna a mensagem original. `P` é a matriz de permutação que realiza a cifra.
    '''
    msg = msg.lower()
    one_hot = para_one_hot(msg)

    P_inv = np.linalg.inv(P)
    one_hot_decifrada = P_inv @ one_hot
    msg_decifrada = para_string(one_hot_decifrada)
    
    return msg_decifrada

def enigma(msg:str, P:np.array, E:np.array):
    '''
    Uma função que faz a cifra enigma na mensagem de entrada usando o cifrador `P` e o cifrador auxiliar `E`, ambos representados como matrizes de permutação.
    '''
    enigma = ""
    for letra in msg:
        letra = letra.lower()
        one_hot = para_one_hot(letra)

        P = E @ P
        one_hot_enigma = P @ one_hot
        letra = para_string(one_hot_enigma)
        enigma += letra
        
    return enigma

def de_enigma(msg:str, P:np.array, E:np.array):
    '''
    Uma função que recupera uma mensagem cifrada como enigma assumindo que ela foi cifrada com o usando o cifrador `P` e o cifrador auxiliar `E`, ambos representados como matrizes de permutação.
    '''
    msg_decifrada = ""
    for letra in msg:
        letra = letra.lower()
        one_hot = para_one_hot(letra)

        P = E @ P
        P_inv = np.linalg.inv(P)

        one_hot_decifrada = P_inv @ one_hot
        letra = para_string(one_hot_decifrada)
        msg_decifrada += letra
    
    return msg_decifrada
