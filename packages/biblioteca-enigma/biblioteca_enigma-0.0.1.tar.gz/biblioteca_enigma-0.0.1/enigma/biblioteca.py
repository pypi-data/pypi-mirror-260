import numpy as np 

def para_one_hot(msg : str): 
    '''
    função para codificar mensagens como uma matriz usando one-hot encoding

    atributos: 
    msg: srt 
        mensagem a ser codificada em matriz

    retorna: 
    uma matriz de tamanho 28X(tamanho da mensagem), dado que o alfabeto usado para a codificação 
    contém os seguintes caracteres :'abcdefghijklmnopqrstuvwxyz @'.Se o caracter não estiver presente
    nessa lista, será substituido pelo caracter @

    '''
    if msg == '' or msg == 'Não a mensagem para ser decifrada' or msg == 'Não a mensagem para ser cifrada': 
        return np.array([[]])
    alfabeto = 'abcdefghijklmnopqrstuvwxyz @'
    tamanho = len(alfabeto)
    one_hot_i = []
    for letra in msg: 
        code = np.array([0]*tamanho)
        if letra in alfabeto: 
            idx = alfabeto.index(letra)
            code[idx] = 1 
        else : 
            code[-1] = 1
        one_hot_i.append(code)
    return np.array(one_hot_i).T

def para_string(M : np.array):
    '''
    função para converter mensagens da representação one-hot encoding para uma string legível

    atributos: 
    M: np.array
        matriz da mensagem codificada de tamanho 28X(tamanho da mensagem) para ser decodificada

    retorna: 
    uma mensagem: str da mensagem decodificada apartir do alfabeto para decodificação = 'abcdefghijklmnopqrstuvwxyz @'.
    Na codificação, caracteres não incluidos nesse alfabeto foram substituidos por @
    '''
    alfabeto = 'abcdefghijklmnopqrstuvwxyz @'
    mensagem =''
    for letra in M.T: 
        idx = np.where(letra == 1)
        idx = idx[0][0]
        mensagem+=alfabeto[idx]
    return mensagem


def cifrar(msg : str, P : np.array): 
    '''
    função que aplica uma cifra simples em uma mensagem recebida 
    como entrada e retorna a mensagem cifrada. `P` é a matriz de permutação que realiza a cifra.

    atributos:
    msg: str 
        mensagem a ser decifrada
    P: np.array
    matriz quadrada de permutação de tamanho 28x28, usada para cifrar a mensagem

    retorna : 
    uma mensagem: str decifrada apartir da decodificação one_hot e a matriz passada de permutação
    '''
    msg_one_hot = para_one_hot(msg)
    if msg_one_hot.shape == (1,0):
        return 'Não a mensagem para ser cifrada'
    cifra_em_one_hot = P @ msg_one_hot 
    msg_cifrada = para_string(cifra_em_one_hot)
    return msg_cifrada


def de_cifrar(msg : str, P : np.array): 
    '''
    função que recupera uma mensagem cifrada, recebida como entrada, e retorna a mensagem original. 
    `P` é a matriz de permutação que realiza a cifra.
    atributos:
    msg: str 
        mensagem a ser cifrada 
    P: np.array
    matriz quadrada de permutação de tamanho 28x28, devido ao tamanho do alfabeto usado

    retorna : 
    uma mensagem: str cifrada apartir da codificação one_hot e a matriz passada de permutação
    '''
    msg_one_hot = para_one_hot(msg)
    if msg_one_hot.shape == (1,0):
        return 'Não a mensagem para ser decifrada'
    one_hot_original = np.linalg.solve(P,msg_one_hot)
    msg_decifrada = para_string(one_hot_original)
    return msg_decifrada

def enigma(msg : str, P : np.array, E : np.array):
    '''
    função que faz a cifra enigma na mensagem de entrada usando o cifrador `P` 
    e o cifrador auxiliar `E`, ambos representados como matrizes de permutação.

    atributos:
    msg: str 
        mensagem a ser decifrada
    P: np.array
    matriz quadrada de permutação de tamanho 28x28, usada para cifrar a mensagem
    E: np.array
    matriz quadrada de permutação de tamanho 28x28, usada para enigmar a mensagem

    retorna : 
    uma mensagem: str em forma de enigma apartir da codificação one_hot e as matriz passadas de permutação
    ''' 
    enigmar = P
    mensagem_enigma = ''
    msg_one = para_one_hot(msg)
    if msg_one.shape == (1,0):
            return 'Não a mensagem para ser cifrada'
    for letra in msg:
        mensagem = para_one_hot(letra)
        mensagem_enigma_parte = enigmar @ mensagem  
        enigmar = E @ enigmar  
        mensagem_enigma_parte= para_string(mensagem_enigma_parte)
        mensagem_enigma+= mensagem_enigma_parte
    return mensagem_enigma

def de_enigma(msg : str, P : np.array, E : np.array): 
    '''
    função que recupera uma mensagem cifrada como enigma assumindo que ela foi cifrada com o usando 
    o cifrador `P` e o cifrador auxiliar `E`, ambos representados como matrizes de permutação.

    atributos:
    msg: str 
        mensagem a ser decifrada
    P: np.array
    matriz quadrada de permutação de tamanho 28x28, usada para cifrar a mensagem anteriormente.
    E: np.array
    matriz quadrada de permutação de tamanho 28x28, usada para enigmar a mensagem anteriormente.
 
    retorna : 
    uma mensagem: str em forma decifrada do enigma apartir da decodificação one_hot e as matriz passadas de permutação
    '''
    mensagem  = para_one_hot(msg)
    if mensagem.shape == (1,0):
        return 'Não a mensagem para ser decifrada'
    denigmar = P
    enigma_decifrado =''
    for letra in msg:
        letra_one_hot = para_one_hot(letra)
        resolucao_parte = np.linalg.solve(denigmar, letra_one_hot)
        denigmar = E @ denigmar 
        enigma_decifrado_parte = para_string(resolucao_parte)
        enigma_decifrado += enigma_decifrado_parte
    return enigma_decifrado
    
