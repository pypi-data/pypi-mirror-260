import numpy as np

# dicionário para mapear cada letra do alfabeto para um número (0-25)
dict_ = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25} 

# criação de duas matrizes de permutação aleatórias
permutation = np.random.permutation(26)
id_matrix = np.eye(26)
P = id_matrix[permutation]  # Matriz de permutação P

permutation2 = np.random.permutation(26)
id_matrix2 = np.eye(26)
E = id_matrix2[permutation2]  # Matriz de permutação E


def para_one_hot(msg : str):
    """Converte uma mensagem de texto para a representação one-hot."""
    msg = msg.replace(" ", "")  # remove espaços
    if len(msg) == 0:
        raise ValueError("Mensagem vazia")
    msg = msg.upper() # converte para maiúsculas

    one_hot = np.zeros((26, len(msg)))  # matriz de zeros
    
    for i, letter in enumerate(msg):
        letter_index = dict_.get(letter)  # índice da letra no dicionário
        if letter_index is not None:
            one_hot[letter_index, i] = 1  # coloca 1 na posição correspondente
        else:
            raise ValueError(f"Caracter invalido: {letter}")
    return one_hot

def para_string(M : np.ndarray):
    """Converte uma matriz one-hot para a representação em texto."""
    M = np.argmax(M, axis=0)  # encontra o índice do maior valor em cada colun (no nosso caso o 1)a
    string = ''

    for index in M:
        for letter, value in dict_.items():
            if value == index:
                string += letter  # letra correspondente do dicionário
    return string

def cifrar(msg : str, P : np.ndarray):
    """Cifra uma mensagem usando uma matriz de permutação."""
    msg_one_hot = para_one_hot(msg)
    encrypted = P @ msg_one_hot
    return para_string(encrypted)

def de_cifrar(msg : str, P : np.ndarray):
    """Decifra uma mensagem usando a transposta da matriz de permutação."""
    msg_one_hot = para_one_hot(msg)
    decrypted = P.T @ msg_one_hot
    return para_string(decrypted)

def enigma(msg : str, P : np.ndarray, E : np.ndarray):
    """Cifra uma mensagem usando duas matrizes de permutação."""
    msg_one_hot = para_one_hot(msg)
    encrypted = E @ P @ msg_one_hot
    return para_string(encrypted)

def de_enigma(msg : str, P : np.ndarray, E : np.ndarray):
    """Decifra uma mensagem cifrada com duas matrizes de permutação."""
    msg_one_hot = para_one_hot(msg)
    decrypted = P.T @ E.T @ msg_one_hot
    return para_string(decrypted)
