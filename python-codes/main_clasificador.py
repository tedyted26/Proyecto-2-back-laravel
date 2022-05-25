'''

        El clasificador recibe un array o una lista de noticias en txt, las clasifica
        Por cada noticia guarda su info en la tabla de noticias
        Tambien devuelvo un diccionario de clave valor donde la clave es la url y el valor es el resultado de cada una de las noticias

    Unimos el primer diccionario y el segundo, y podemos sacar el numero total de urls analizadas, con un numero de odio y otro de no odio       

'''
from Classify import Classify
import tratamientoNoticias as tn
import os

#------------WEB SCRAPING--------------# (sugerencia, de momento no lo hacemos)

    # a cada url pillada de webscrapear primero comprobar si existe en la bbdd (ahorrar procesamiento y duplicados)

    # si existen en vez de hacer el webscraping completo coger las urls y sacar los datos de la bbdd
        # los guardamos en una lista de tuplas [Noticia, resultado]
        # cada noticia tiene que tener titulo, subtitulo, url y fecha
        # listaNoticiasConResultadoDeBBDD = []

    # para el resto de noticias que no existan, se completa el webscraping y se ejecuta el clasificador


#-------------CLASIFICADOR-------------#
classify = Classify()

currentDirectory = os.getcwd() + "/python-codes"
pathIDFList = currentDirectory + "/Modelos pre-entrenados/IDFlist.txt"
pathDiccionario = currentDirectory + "/Modelos pre-entrenados/diccionario.txt"

# FIXME cambiar directorio para que coincida con el resto de noticias scrapeadas
pathNoticiasAClasificar = currentDirectory + "/noticias-scrapeadas/ABC/violencia"
# FIXME algoritmo de prueba, se puede dejar que el admin pueda elegir entre ellos
pathModelo = currentDirectory + "/Modelos pre-entrenados/arbolTn.pickle"


modelo = classify.openModel(pathModelo)

resultados_raw = classify.classifyNews(pathNoticiasAClasificar, modelo,
                   pathIDFList, pathDiccionario)

# creamos una lista de tuplas del mismo formato que la sacada de la BBDD
listaNoticiasConResultadoClasificador = []
for noticia in resultados_raw:
    tupla = [tn.getNoticia(pathNoticiasAClasificar + '/' +noticia), resultados_raw[noticia]]
    listaNoticiasConResultadoClasificador.append(tupla)

# juntamos las dos listas (en caso de hacer lo de la sugerencia)
# listaNoticiasConResultadoGlobales = listaNoticiasConResultadoClasificador + listaNoticiasConResultadoDeBBDD

# resultados que necesitamos en el front: 
# numero de noticias de no odio
# numero de noticias de odio (no necesitamos devolverlo como variable porque se puede calcular a partir del numero de elementos de la lista)
# lista con las noticias de odio

# pasamos a JSON
jsonString = "["
for noticia, resultado in listaNoticiasConResultadoClasificador:
    jsonString += "{url: " + noticia.url.replace("\n", "") + ",titulo: " + noticia.titulo + ",subtitulo: " + noticia.subtitulo + ",fecha_noticia: " + noticia.fecha + ",resultados: " + str(resultado) + "},"
jsonString.removesuffix(",")
jsonString = jsonString + "]"

print(jsonString)

