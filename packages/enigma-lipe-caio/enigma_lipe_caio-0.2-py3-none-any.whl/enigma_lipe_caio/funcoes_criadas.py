import numpy as np
from enigma_lipe_caio.funcoes_adicionais import *

def para_one_hot(mensagem=str):

    if teste_mensagem(mensagem):
        #transformando a mensagem para poder traduzi-la
        mensagem = mensagem.lower()

        #pegando a matriz identidade do alfabeto
        matriz_identidade_todos_char, todos_carcteres = matriz_identidade_alfabeto()

        lista_index_caracteres_mensagem = []
        for caracter_mensagem in mensagem:
            for caracter in todos_carcteres:
                if caracter_mensagem == caracter:
                    index_caracter = todos_carcteres.index(caracter)
                    lista_index_caracteres_mensagem.append(index_caracter)

        mensagem_traduzida = matriz_identidade_todos_char[:,lista_index_caracteres_mensagem]

        return mensagem_traduzida

def para_string(M=np.array):

    #mensagem final
    mensagem_traduzida = ""

    #transformando o array para poder transforma-lo
    M = np.transpose(M)

    #pegando a matriz identidade do alfabeto
    matriz_identidade_todos_char, todos_carcteres = matriz_identidade_alfabeto()

    lista_index_letras_matriz = []
    index_matriz_id = 0 
    for coluna_matriz_mensagem in M:
        index_matriz_id = 0
        for coluna_matriz_id in matriz_identidade_todos_char:
            index_matriz_id += 1
            if np.all(coluna_matriz_mensagem == coluna_matriz_id):
                lista_index_letras_matriz.append(index_matriz_id-1)
                index_matriz_id = 0

    for index_letra in lista_index_letras_matriz:
        mensagem_traduzida += todos_carcteres[index_letra]

    return mensagem_traduzida

def cifrar(msg=str,P=np.array):

    if teste_mensagem(msg):
        matriz_mensagem = para_one_hot(msg)

        matriz_codificada = P@matriz_mensagem

        mensagem_codificada = para_string(matriz_codificada)

        return mensagem_codificada

def de_cifrar(msg=str,P=np.array):

    if teste_mensagem(msg):
        matriz_mensagem_codificada = para_one_hot(msg)

        inverso_P = np.linalg.inv(P)

        matriz_de_codificada =  inverso_P @ matriz_mensagem_codificada 

        mensagem_de_codificada = para_string(matriz_de_codificada)

        return mensagem_de_codificada

def enigma(msg=str,P=np.array, E=np.array):

    if teste_mensagem(msg):
        matriz_codificada = []

        matriz_mensagem = para_one_hot(msg)
        matriz_mensagem = matriz_mensagem.T

        for i in range(len(msg)):
            #primeira letra apenas multiplicar por P
            if i == 0:
                letra_codificada = P @ matriz_mensagem[i]
            else:
                letra_codificada = matriz_mensagem[i]
                #multiplicar por E a letra em especifico a quantidade de vezes que for o tamanho de i
                for j in range(i):
                    letra_codificada = E @ letra_codificada
                letra_codificada = P @ letra_codificada
            matriz_codificada.append(letra_codificada)

        matriz_codificada = np.array(matriz_codificada)

        mensagem_codificada = para_string(np.array(matriz_codificada.T))

        return mensagem_codificada 

def de_enigma(msg=str,P=np.array, E=np.array):

    if teste_mensagem(msg):
        matriz_decodificada = []

        matriz_mensagem_codificada = para_one_hot(msg)
        matriz_mensagem_codificada = matriz_mensagem_codificada.T

        inverso_P = np.linalg.inv(P)
        inverso_E = np.linalg.inv(E)

        for i in range(len(msg)):
            letra_decodificada = matriz_mensagem_codificada[i]
            if i == 0:
                letra_decodificada = inverso_P @ letra_decodificada
            else:
                letra_decodificada = inverso_P @ letra_decodificada
                for _ in range(i):
                    letra_decodificada = inverso_E @ letra_decodificada
                    
            matriz_decodificada.append(letra_decodificada)

        matriz_decodificada = np.array(matriz_decodificada).T
        mensagem_decodificada = para_string(matriz_decodificada)

        return mensagem_decodificada

