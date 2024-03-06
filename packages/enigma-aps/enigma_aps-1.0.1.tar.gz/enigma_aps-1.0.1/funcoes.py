import numpy as np

def para_one_hot(msg: str):
    # Definir o alfabeto incluindo o espaço em branco
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    num_chars = len(alphabet)
    
    # Criar um dicionário para mapear letras para índices
    char_to_index = {char: i for i, char in enumerate(alphabet)}
    
    # Inicializar a matriz one-hot
    one_hot_matrix = np.zeros((num_chars, len(msg)), dtype=int)
    
    # Preencher a matriz one-hot
    for i, char in enumerate(msg):
        if char.upper() in alphabet:
            one_hot_matrix[char_to_index[char.upper()], i] = 1
    
    # Retornar a matriz one-hot
    return one_hot_matrix

def para_string(one_hot: np.array):
    # Definir o alfabeto incluindo o espaço em branco
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '

    # String para armazenar o resultado
    result = ''
    
    # Iterar sobre as colunas da matriz one-hot
    for col in range(one_hot.shape[1]):
        # Encontrar o índice do valor 1 na coluna atual
        char_index = np.argmax(one_hot[:, col])
        # Adicionar a letra correspondente ao resultado
        result += alphabet[char_index]

    # Retornar a string minúscula
    return result.lower()

def cifrar(msg: str, P: np.array):
    # Obter a matriz one-hot da mensagem
    one_hot_msg = para_one_hot(msg)
    
    # Multiplicar a matriz one-hot pela matriz de permutação
    cifrado = P @ one_hot_msg
    
    # Retornar a string cifrada
    return para_string(cifrado)

# Função para decifrar uma mensagem
def de_cifrar(msg: str, P: np.array):
    # Obter a matriz one-hot da mensagem
    one_hot_msg = para_one_hot(msg)
    
    # Calcular a matriz inversa da matriz de permutação
    P_inv = np.linalg.inv(P)
    
    # Multiplicar a matriz one-hot pela matriz inversa da permutação
    decifrado = P_inv @ one_hot_msg
    
    # Retornar a string decifrada
    return para_string(decifrado)

# Função para cifrar uma mensagem usando a enigma
def enigma(msg: str, P: np.array, E: np.array):
    # Inicializar a mensagem cifrada
    ciphered_msg = ''
    
    # Iterar sobre cada caractere da mensagem
    for i, char in enumerate(msg):
        # Para a primeira letra, cifrar usando apenas a matriz P atual
        if i == 0:
            # Transformar o caractere em uma matriz one-hot
            one_hot_char = para_one_hot(char)
            
            # Multiplicar a matriz one-hot pela matriz de permutação atual (P)
            ciphered_char = P @ one_hot_char
            
            # Transformar a matriz cifrada de volta em string
            ciphered_char_str = para_string(ciphered_char)
        else:
            # Para as letras subsequentes, atualizar a matriz de permutação (P) multiplicando pela matriz E
            P = P @ E
            
            # Transformar o caractere em uma matriz one-hot
            one_hot_char = para_one_hot(char)
            
            # Multiplicar a matriz one-hot pela nova matriz de permutação (P)
            ciphered_char = P @ one_hot_char
            
            # Transformar a matriz cifrada de volta em string
            ciphered_char_str = para_string(ciphered_char)
        
        # Adicionar o caractere cifrado à mensagem cifrada
        ciphered_msg += ciphered_char_str
        
    # Retornar a mensagem cifrada
    return ciphered_msg

# Função para decifrar uma mensagem usando a enigma
def de_enigma(msg: str, P: np.array, E: np.array):
    # Inicializar a mensagem decifrada
    deciphered_msg = ''
    
    # Iterar sobre cada caractere da mensagem
    for i, char in enumerate(msg):
        # Para a primeira letra, decifrar usando apenas a matriz P atual
        if i == 0:
            # Transformar o caractere em uma matriz one-hot
            one_hot_char = para_one_hot(char)
            
            # Calcular a matriz inversa da matriz de permutação atual (P)
            P_inv = np.linalg.inv(P)
            
            # Multiplicar a matriz one-hot pela matriz inversa da permutação atual (P)
            deciphered_char = P_inv @ one_hot_char
            
            # Transformar a matriz decifrada de volta em string
            deciphered_char_str = para_string(deciphered_char)
        else:
            # Para as letras subsequentes, atualizar a matriz de permutação (P) multiplicando pela matriz E
            P = P @ E
            
            # Calcular a matriz inversa da matriz de permutação atual (P)
            P_inv = np.linalg.inv(P)
            
            # Transformar o caractere em uma matriz one-hot
            one_hot_char = para_one_hot(char)
            
            # Multiplicar a matriz one-hot pela matriz inversa da permutação atual (P)
            deciphered_char = P_inv @ one_hot_char
            
            # Transformar a matriz decifrada de volta em string
            deciphered_char_str = para_string(deciphered_char)
        
        # Adicionar o caractere decifrado à mensagem decifrada
        deciphered_msg += deciphered_char_str
        
    # Retornar a mensagem decifrada
    return deciphered_msg
