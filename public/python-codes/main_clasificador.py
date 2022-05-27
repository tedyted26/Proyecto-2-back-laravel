'''

        El clasificador recibe un array o una lista de noticias en txt, las clasifica
        Por cada noticia guarda su info en la tabla de noticias
        Tambien devuelvo un diccionario de clave valor donde la clave es la url y el valor es el resultado de cada una de las noticias

    Unimos el primer diccionario y el segundo, y podemos sacar el numero total de urls analizadas, con un numero de odio y otro de no odio       

'''
from Classify import Classify
import tratamientoNoticias as tn
import os
import Guardado as save
import ETL_ABC, ETL_LaRazon, ETL_LaSexta, ETL_Nacionales, ETL_Vanguardia
import sys

#------------WEB SCRAPING--------------# (sugerencia, de momento no lo hacemos)

    # a cada url pillada de webscrapear primero comprobar si existe en la bbdd (ahorrar procesamiento y duplicados)

    # si existen en vez de hacer el webscraping completo coger las urls y sacar los datos de la bbdd
        # los guardamos en una lista de tuplas [Noticia, resultado]
        # cada noticia tiene que tener titulo, subtitulo, url y fecha
        # listaNoticiasConResultadoDeBBDD = []

    # para el resto de noticias que no existan, se completa el webscraping y se ejecuta el clasificador
noticiasGlobales = []
busqueda = "Barajas" #sys.argv[1]
numPaginas = 1

noticiasGlobales.extend(ETL_ABC.getABCNews(busqueda,numPaginas))

# noticiasGlobales.extend(ETL_LaRazon.getLaRazonNews(busqueda))

# noticiasGlobales.extend(ETL_LaSexta.scraper_la_sexta_bs4(busqueda, numPaginas))

# noticiasGlobales.extend(ETL_Nacionales.get20MinutosNews(busqueda))

# noticiasGlobales.extend(ETL_Nacionales.getElMundoNews(busqueda))

# noticiasGlobales.extend(ETL_Vanguardia.getLaVanguardiaNews(busqueda))


#-------------CLASIFICADOR-------------#
classify = Classify()


currentDirectory = os.getcwd() + "/python-codes"
#os.chdir("/public")

pathIDFList = currentDirectory + "/Modelos pre-entrenados/IDFlist.txt"
pathDiccionario = currentDirectory + "/Modelos pre-entrenados/diccionario.txt"

# FIXME algoritmo de prueba, se puede dejar que el admin pueda elegir entre ellos
pathModelo = currentDirectory + "/Modelos pre-entrenados/arbolTn.pickle"
#print(currentDirectory)

modelo = classify.openModel(pathModelo)


# el clasificador está modificado para que devuelva un diccionario de index y resultado
# el index es un int que corresponde a cada una de las noticias que hay en noticiasGlobales 
resultados_raw = classify.classifyNews(noticiasGlobales, modelo,
                   pathIDFList, pathDiccionario)
#print(resultados_raw)

# creamos una lista de tuplas del mismo formato que la sacada de la BBDD
listaNoticiasConResultadoClasificador = []
for noticia in resultados_raw:
    tupla = [noticiasGlobales[noticia], resultados_raw[noticia]]
    listaNoticiasConResultadoClasificador.append(tupla)

# juntamos las dos listas (en caso de hacer lo de la sugerencia)
# listaNoticiasConResultadoGlobales = listaNoticiasConResultadoClasificador + listaNoticiasConResultadoDeBBDD

# pasamos a JSON
jsonString = "["
for noticia, resultado in listaNoticiasConResultadoClasificador:
    jsonString += "{url: " + noticia.url.replace("\n", "") + ",titulo: " + noticia.titulo + ",subtitulo: " + noticia.subtitulo + ",fecha_noticia: " + noticia.fecha + ",resultados: " + str(resultado) + "},"
jsonString = jsonString[:-1]
jsonString = jsonString + "]"

print(jsonString)


