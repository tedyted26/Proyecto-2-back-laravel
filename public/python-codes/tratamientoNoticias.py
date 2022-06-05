import os
import re
import spacy
from copy import deepcopy
import TransformTFIDF as tfidf
from nltk.tokenize import WordPunctTokenizer
from Noticia import Noticia
import ast


import pandas as pd

import time

os.getcwd() + "/python-codes/" 

rutaListaParada = os.getcwd() + "/python-codes/" + "lista1.txt"
nlp = spacy.load('es_core_news_sm')

# Metodos de Tratamiento de ficheros
def tokenizacion(texto):
    tokens = WordPunctTokenizer().tokenize(texto)
    return tokens


def tratamientoBasico(tokens):
    listaTratada = []
    for token in tokens:
        a = re.sub(r"[^a-zA-Zá-úÁ-Ú_üÜ]", "", token)
        if a != "" and a is not None:
            a = re.match(r"[a-zA-Zá-úÁ-Ú_üÜ]+", a)
            listaTratada.append(a[0].lower())
        # listaTratada.append(re.sub(r"[^a-zA-Zá-úÁ-Ú]", "", token).lower())
    return listaTratada

def listaParada(tokens):
    listaParada = tratamientoBasico(tokenizacion(leerFichero(rutaListaParada)))
    listaDepurada = [x for x in tokens if x not in listaParada]
    return listaDepurada

def lematizacion(tokens):
    texto = ""
    for token in tokens:
        texto += token + " "
    doc = nlp(texto)
    lemmas = [tok.lemma_ for tok in doc]
    return lemmas
    
def leerNoticia(rutaFichero):
    '''Lee un archivo de noticia, devolviendo el texto al completo'''
    f = open(rutaFichero, 'r', encoding="ISO-8859-1")
    texto = f.read()
    if ";-;" in texto:
        texto = texto.replace("titulo;-;url;-;url_completa;-;autor;-;fecha;-;hora;-;subtitulo;-;texto", "")
        texto = texto.replace(";-;"," ")
    else:
        texto = re.sub("##+", " ", texto)
    return texto

def getNoticia(rutaFichero):
    #print(rutaFichero)
    f = open (rutaFichero,'r', encoding="ISO-8859-1")
    texto = f.read()
    if ";-;" in texto:
        texto = texto.replace("titulo;-;url;-;url_completa;-;autor;-;fecha;-;hora;-;subtitulo;-;texto", "")
        texto = texto.replace(";-;","####\n")
    texto = texto.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    listaTexto = texto.split(sep="#####\n")                                                                               
    noticia = Noticia(listaTexto[4],listaTexto[5],listaTexto[3],listaTexto[0],listaTexto[2],listaTexto[1],ast.literal_eval(listaTexto[7]),listaTexto[6])
    return noticia

def leerFichero(rutaFichero):
    '''Lee el fichero y devuelve el texto segun la ruta'''
    f = open (rutaFichero,'r', encoding="ISO-8859-1")
    texto = f.read()
    f.close()
    return texto

def tratarTexto(t):
    '''Aplica un tratamiento al texto, segmentandolo en una lista de palabras con la que poder
    despues añadir el texto a una matriz.'''
    # t0 = time.time()
    tokens = tokenizacion(t)
    # t1 = time.time()
    # print(f"TOKENS:{tokens}\n{t1-t0}\n")
    tBasico = tratamientoBasico(tokens)
    # t2 = time.time()
    # print(f"TRAT BASICO:{tBasico}\n{t2-t1}\n")
    t_postListaParada = listaParada(tBasico)
    # t3 = time.time()
    # print(f"LISTA:{t_postListaParada}\n{t3-t2}\n")
    lemas = lematizacion(t_postListaParada)
    # t4 = time.time()
    # print(f"LEMAS:{lemas}\n{t4-t3}\n")
    return lemas

def generarVectorDeTexto(t: str, saveWordlist: bool, file ,odio: int = 0, rutaWordList= "diccionario.txt"):
    '''Genera un vector de texto a partir del texto/string "t" proporcionado, tratandolo
    en el proceso y elminando terminos superfluos.
    Los argumentos son los siguientes:

    - t: El texto a transformar

    - saveWordlist: Este booleano determina si las nuevas palabras descubiertas deben ser añadidas
    al archivo de wordlist. Esto sirve para poder generar vectores y palabras permanentes en la matriz
    o para generar vectores temporales que puedan operar con los resultados anteriores de la matriz.

    - file: el archivo del que proviene el texto, el cual se almacena en la 2da posicion del vector

    - odio: determina si la noticia es de odio (1), no odio (-1) o desconocida (0), almacenandose
    en la 1ª posicion del vector'''
    t2 = tratarTexto(t)
    t5 = time.time()
    # tiempos = []
    wordlist = []
    vector = []
    '''Añade al vector si es de odio, no odio o desconocido y el nombre del archivo'''
    vector += [odio, file]
    # tiempos.append(time.time())
    if os.path.isfile(rutaWordList):  # Compruebo si existe el fichero
        wordlist = getWordList(rutaWordList)
        vector += [0 for i in range(len(wordlist))]
    # tiempos.append(time.time())
    # Por cada palabra de la noticia, añadimos las nuevas al diccionario y al vector
    # correspondiente a la matriz
    for token in t2:
        if token not in wordlist:
            wordlist.append(token)
            vector.append(1)
        else:
            for i, word in enumerate(wordlist):
                if word == token:
                    vector[i+2] += 1
    # tiempos.append(time.time())
    if saveWordlist:
        #TODO poner with open
        f = open(rutaWordList, "w", encoding="ISO-8859-1")
        for elemento in wordlist:
            f.write(elemento + "\n")
        f.close()
    #print(time.time() - t5)
    # tiempos.append(time.time())

    # for i in range(len(tiempos)-1):
    #     print(f"{i+1} - {i}-> {tiempos[i+1]-tiempos[i]}")
    return vector

def getWordList(rutaWordList= "diccionario.txt"):
    return leerFichero(rutaWordList).splitlines()
def generarMatriz(fichero: str):
    '''Genera y devuelve la matriz a partir del fichero seleccionado
    -fichero: ruta y nombre del archivo (ejemplo: "matriz.txt")'''
    rutaMatriz = fichero
    matriz = []
    if os.path.isfile(rutaMatriz):  # Compruebo si existe el fichero
        f = open(rutaMatriz, encoding="ISO-8859-1")
        filas = f.read().split(";\n")
        matriz = []
        for fila in filas:
            filaSp = fila.split("++")
            matriz.append([val for val in filaSp[0:2]] + [int(val) for val in filaSp[2:]])

        # matriz = [[int(val) for val in fila.split(" ")] for fila in filas]
    return matriz

def addVectorToMatriz(m, v):
    '''Devuelve una matriz, producto de la suma de una copia de la matriz proporcionada y 
    de un vector "v".
    En caso del que el vector sea mayor que el tamaño de las filas de la matriz, amplia la matriz
    añadiendo tantos "0" a la derecha como diferencia haya.'''

    if len(m) > 0:
        diffMatrizVector = len(v) - len(m[0])
        for row in m:
            row += [0 for i in range(diffMatrizVector)]

    m.append(v)
    return m
def saveMatrizToFile(m, file):
    '''Guarda la matriz en un archivo, separando los valores de cada fila con
    espacios y las filas con ";\n"'''
    f = open(file, "w", encoding="ISO-8859-1")
    for i,fila in enumerate(m):
        str_fila = [str(ele) for ele in fila]
        res = "++".join(str_fila)
        if i > 0:
            res = ";\n" + res
        f.write(res)
    f.close()


def getAllNewsUrlList(newsFolderPath):
    '''Devuelve una lista rellena de tuplas: (pathcompleto, nombre)
    Esta lista contiene todos los archivos encontrados en la carpeta proporcionada,
    la cual debe ser una carpeta en la que se almacenen las noticias'''
    r = newsFolderPath
    if ":" not in newsFolderPath:
        #r = os.getcwd() + newsFolderPath
        r = newsFolderPath
    return [(r+"/"+i, i) for i in os.listdir(r)]

def addVectoresToMatrizByFolderPath(path: str, m: list, odio: int, max_noticias = -1):
    '''Devuelve una nueva matriz con las noticias proporcionadas a traves la carpeta en la que
    se encuentran.
    
    -path: la carpeta donde se encuentran las noticias (ej:"/Noticias/NoOdio)
    -m: la matriz inicial
    -odio: Si la noticia es de odio (1), no odio (-1) o desconocida (0)"'''
    paths = getAllNewsUrlList(path)[:max_noticias]
    m1 = deepcopy(m)

    vectores = []
    for i, x in enumerate(paths):
        #print(f"Añadiendo noticia {i} de {len(paths)}")
        try:
            textoNoticia = leerNoticia(x[0])
            vectores.append(generarVectorDeTexto(textoNoticia, True, x[1], odio= odio))
        except:
            print(f"Error generando vector en archivo: {x[1]}")

    for v in vectores:
        m1 = addVectorToMatriz(m1, v)
    return m1

def transformMatrizToPandasDataFrame(matriz: list, rutaWordList= "diccionario.txt"):
    df = pd.DataFrame( matriz, columns=["odio_", "nombre_"] + getWordList(rutaWordList))
    #print(df.dtypes)
    return df

