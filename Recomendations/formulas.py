import pandas as pd
import numpy as np

def calcula_percentual_indefinido(dataframe, coluna ):
    indefinidos = dataframe.loc[pd.isna(dataframe[coluna]), coluna].shape[0]
    #total = dataframe.idade.shape[0]
    total = dataframe[coluna].shape[0]

    return (indefinidos/total)* 100

def one_hot(categorias, valor):
# Transforma as categorias num conjunto para eliminar duplicatas,
# depois transforma em lista para obter índice
    categorias = list(set(categorias))
    #print("Categorias: ")
    #print(categorias)
# Obtém o índice do elemento atual
    indice = categorias.index(valor)
    #print("Indice ")
    #print(indice)
# Cria um vetor com o número de coordenadas igual ao número de categorias
    #print("Vetor")
    vetor = np.zeros(len(categorias))
# Modifica o índice correspondente a classe para 1.0 no vetor de categorias
    vetor[indice] = 1
# devolve o vetor one-hot resultante
    return vetor


def vetorizar(classe_social, sexo, idade, parentes, dependentes, tarifa, embarque):
    return classe_social.tolist() + sexo.tolist() + [idade] + [parentes] + \
     [dependentes] + [tarifa] + embarque.tolist()