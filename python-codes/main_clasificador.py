'''

        El clasificador recibe un array o una lista de noticias en txt, las clasifica
        Por cada noticia guarda su info en la tabla de noticias
        Tambien devuelvo un diccionario de clave valor donde la clave es la url y el valor es el resultado de cada una de las noticias

    Unimos el primer diccionario y el segundo, y podemos sacar el numero total de urls analizadas, con un numero de odio y otro de no odio       

'''
# -*- coding: utf-8 -*-

from queue import Empty
from Classify import Classify
import tratamientoNoticias as tn
import os
import Guardado as save
import ETL_ABC, ETL_LaRazon, ETL_LaSexta, ETL_Nacionales, ETL_Vanguardia
import sys
import re

#------------WEB SCRAPING--------------# (sugerencia, de momento no lo hacemos)

    # a cada url pillada de webscrapear primero comprobar si existe en la bbdd (ahorrar procesamiento y duplicados)

    # si existen en vez de hacer el webscraping completo coger las urls y sacar los datos de la bbdd
        # los guardamos en una lista de tuplas [Noticia, resultado]
        # cada noticia tiene que tener titulo, subtitulo, url y fecha
        # listaNoticiasConResultadoDeBBDD = []

    # para el resto de noticias que no existan, se completa el webscraping y se ejecuta el clasificador
noticiasGlobales = []
busqueda = sys.argv[1]
numPaginas = 1
jsonString = ""
busqueda = busqueda.lower()
busqueda = busqueda.replace("í", "i").replace("á", "a").replace("é", "e").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
print(busqueda)

noticiasGlobales.extend(ETL_ABC.getABCNews(busqueda,numPaginas)) #Va perfe

noticiasGlobales.extend(ETL_LaRazon.getLaRazonNews(busqueda)) #Va perfe

#noticiasGlobales.extend(ETL_LaSexta.scraper_la_sexta_bs4(busqueda)) #No va

#noticiasGlobales.extend(ETL_Nacionales.get20MinutosNews(busqueda)) #No va

noticiasGlobales.extend(ETL_Nacionales.getElMundoNews(busqueda)) #Va perfe

noticiasGlobales.extend(ETL_Vanguardia.getLaVanguardiaNews(busqueda)) #Va a medias


#-------------CLASIFICADOR-------------#
if noticiasGlobales:
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

    '''
    jsonString = '['
    for noticia, resultado in listaNoticiasConResultadoClasificador:
        jsonString += '{"url":"'+noticia.url+'","titulo":"'+noticia.titulo+'","subtitulo":"'+noticia.subtitulo+'","fecha_noticia":"'+noticia.fecha+'","resultados":"'+str(resultado) +'"},'
    jsonString = jsonString[:-1]
    jsonString = jsonString + ']'
    jsonString = jsonString.replace("'", "").replace("\n", "")
    print(jsonString)
    '''

    jsonString = '['
    for noticia, resultado in listaNoticiasConResultadoClasificador:
        titulo = re.sub(r'[^a-zA-Z0-9\s]', '', str(noticia.titulo))
        subtitulo = re.sub(r'[^a-zA-Z0-9\s]', '', str(noticia.subtitulo))
        jsonString += '{"url": "'+noticia.url +'","resultados":"'+str(resultado) +'","titulo":"'+titulo+'","subtitulo":"'+str(subtitulo)+'"},'
    jsonString = jsonString[:-1]
    jsonString = jsonString + ']'
#jsonString = '[{"resultados":"1"},{"resultados":"-1"}]'
print(jsonString)

'''
string = '[{"url":"https://www.abc.es/espana/madrid/abci-esta-llamado-tetuan-nuevo-carabanchel-arte-madrid-202206020223_noticia.html","titulo":"Est llamado Tetun a ser el nuevo Carabanchel del arte en Madrid?","subtitulo":"Con la inauguracin de la exposicin de su III Programa de Residencias para Jvenes Comisarios en este barrio del norte de la capital, una prestigiosa fundacin internacional como la Sandretto Re Rebaudengo sita Tetun en el mapa y se suma a otras iniciativas en la ciudad que transforman espacios de pasado industrial en interesantes centros artsticos","fecha_noticia":"2022-06-02T08:28:36Z","resultados":"-1"},{"url":"https://www.abc.es/espana/madrid/abci-lorenzo-perez-superbombero-carabanchel-64-medallas-202205272031_noticia.html","titulo":"Lorenzo Prez, el superbombero de Carabanchel con 64 medallas","subtitulo":"A sus 53 aos, es una leyenda en las competiciones del gremio. Las ltimas las gan en Lisboa","fecha_noticia":"2022-05-27T18:31:11Z","resultados":"1"},{"url":"https://www.abc.es/espana/madrid/abci-tres-detenidos-tras-violenta-persecucion-atracar-clinica-veterinaria-fuenlabrada-202205181025_noticia.html","titulo":"Tres detenidos tras una violenta persecucin por atracar una clnica veterinaria en Fuenlabrada","subtitulo":"Durante el cacheo superficial y el registro del vehculo, localizaron una caja de caudales con dinero en efectivo en su interior","fecha_noticia":"2022-05-18T08:25:12Z","resultados":"1"},{"url":"https://www.abc.es/espana/madrid/abci-selectividad-madrid-2022-estas-11-bibliotecas-amplian-horario-para-preparar-examenes-evau-202206040158_noticia.html","titulo":"Selectividad Madrid 2022: Estas son las 11 bibliotecas que amplan el horario para preparar los exmenes de la EvAU","subtitulo":"La Rafael Alberti, de Fuencarral-El Pardo, y la Mara Moliner, de Villaverde, permanecern operativas 24 horas todos los das","fecha_noticia":"2022-06-03T23:58:54Z","resultados":"-1"},{"url":"https://www.abc.es/espana/madrid/abci-mujer-mata-vecina-y-luego-suicida-lanzandose-desde-sexto-piso-carabanchel-202204181543_noticia.html","titulo":"Una mujer mata a su vecina y luego se suicida lanzndose desde un sexto piso en Carabanchel","subtitulo":"Al acceder la Polica Nacional al inmueble, con la ayuda de Bomberos del Ayuntamiento de Madrid, se encontraron con una mujer de 84 aos con varias heridas de arma blanca","fecha_noticia":"2022-04-18T17:45:56Z","resultados":"-1"},{"url":"https://www.abc.es/espana/madrid/abci-mas-50000-visitas-finca-vista-alegre-primer-202204210133_noticia.html","titulo":"Ms de 50.000 visitas a la Finca Vista Alegre en su primer ao","subtitulo":"Desde que se abri a los vecinos, el 1 de mayo de 2021, ha sido creciente el inters por visitar este oasis de Carabanchel ","fecha_noticia":"2022-04-20T23:33:26Z","resultados":"-1"},{"url":"https://www.abc.es/espana/madrid/abci-jubilar-san-isidro-acerca-patron-desde-carabanchel-buitrago-y-reduena-202204050120_noticia.html","titulo":"El ao jubilar de San Isidro acerca al patrn desde Carabanchel a Buitrago y Reduea","subtitulo":"El cuerpo incorrupto ser expuesto a los fieles del 21 al 29 de mayo en la Colegiata","fecha_noticia":"2022-04-05T16:20:57Z","resultados":"-1"},{"url":"https://www.abc.es/espana/madrid/abci-ensaya-carabanchel-oportunidad-todos-grupos-madrid-estaban-esperando-202202161920_noticia.html","titulo":"Ensaya Carabanchel, la oportunidad que todos los grupos de Madrid estaban esperando","subtitulo":"La iniciativa ofrece un programa subvencionado por el Ayuntamiento para la mentora y profesionalizacin musical  de bandas emergentes","fecha_noticia":"2022-02-17T16:52:33Z","resultados":"-1"},{"url":"https://www.abc.es/sociedad/abci-madrid-construira-primer-hospital-totalmente-digital-202206020916_noticia.html","titulo":"Madrid construir su primer hospital totalmente digital","subtitulo":"El grupo HM abre en la capital un nuevo centro con tecnologa de ltima generacin","fecha_noticia":"2022-06-02T07:16:52Z","resultados":"-1"},{"url":"https://www.abc.es/espana/madrid/abci-casi-cien-bandas-madrilenas-solicitan-formar-parte-proyecto-ensaya-carabanchel-202203081624_noticia.html","titulo":"Casi cien bandas madrileas solicitan formar parte del proyecto Ensaya Carabanchel","subtitulo":"Los ocho seleccionados contarn con el asesoramiento y formacin de los equipos de varios locales de ensayo en materia de sonido y produccin artstica, composicin, arreglos musicales, promocin, comunicacin y relaciones con discogrficas","fecha_noticia":"2022-03-08T15:24:43Z","resultados":"-1"}]'
#stringPrueba = "[{url: texto//de//prueba/:)),texto: nada que ver}]"
print(string)
'''





