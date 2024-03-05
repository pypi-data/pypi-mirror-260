import numpy as np

# Alfabeto gerado com ChatGPT
alphabet = [" ", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def para_one_hot(msg: str):
    if not msg or not isinstance(msg, str): 
        raise Exception(f"Mensagem não suportada")

    for c in msg:
        if c not in alphabet:
            raise Exception(f""""{c}" não faz parte do alfabeto disponível.""")

    res = np.array(np.zeros((27,1)))
    res[alphabet.index(msg[0])][0] = 1
    for i in range(1, len(msg)):
        temp_vect = np.array(np.zeros((27,1)))
        temp_vect[alphabet.index(msg[i])][0] = 1
        res = np.concatenate((res, temp_vect), axis=1)
    return res

def para_string(m: np.array):
    phrase = ""
    for i in range(len(m[0])):
        column = m[:, i]

        for y in range(27):
            if column[y] == 1:
                phrase += alphabet[y]
        
    return phrase

def cifrar(msg, P):
    matrix = para_one_hot(msg)
    
    return para_string(P @ matrix)

def de_cirfrar(msg, P):
    inv_P = np.linalg.inv(P)
    matrix = para_one_hot(msg)

    return para_string(inv_P @ matrix)

def enigma(msg, P, E):

    M = para_one_hot(msg)
    es =  P
    res = es @ M[:, 0].reshape(27, 1)

    for i in range(1, len(M[0])):
        es = E @ es 

        tr = es @ M[:, i].reshape(27, 1)

        res = np.concatenate((res, tr), axis=1)

    return para_string(res)

def de_enigma(msg, P, E):
    M = para_one_hot(msg)
    es = P
    res = np.linalg.inv(es) @ M[:, 0].reshape(27, 1)
    
    for i in range(1, len(M[0])):
        es = E @ es

        tr = np.linalg.inv(es) @ M[:, i].reshape(27, 1)

        res = np.concatenate((res, tr), axis=1)

    return para_string(res)

# P = np.random.permutation(np.identity(27))
# E = np.random.permutation(np.identity(27))
# enig = enigma("hello world", P, E)


# print(de_enigma(enig, P, E))

# print(enc)

#  print(de_cirfrar(enc, P))
