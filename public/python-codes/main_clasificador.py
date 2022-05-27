'''

        El clasificador recibe un array o una lista de noticias en txt, las clasifica
        Por cada noticia guarda su info en la tabla de noticias
        Tambien devuelvo un diccionario de clave valor donde la clave es la url y el valor es el resultado de cada una de las noticias

    Unimos el primer diccionario y el segundo, y podemos sacar el numero total de urls analizadas, con un numero de odio y otro de no odio       

'''
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
'''
string = """[{url: https://www.abc.es/deportes/abci-cuba-no-frena-estampida-otro-atleta-escapa-nada-mas-pisar-aeropuerto-barajas-202205261028_noticia.html,titulo: Cuba no frena la estampida: otro atleta se escapa nada ms pisar el aeropuerto Barajas,subtitulo: Jenns Fernndez, 'la centella de Simpson', el gran talento de la velocidad de su pas, abandona su seleccin al llegar a  Espaa ,fecha_noticia: 2022-05-26T09:09:27Z,resultados: -1},{url: https://www.abc.es/espana/madrid/abci-linea-8-metro-reabre-este-sabado-tres-dias-antes-previsto-tras-finalizar-obras-202205241154_noticia.html,titulo: La lnea 8 de Metro reabre este sbado, tres das antes de lo previsto, tras finalizar sus obras,subtitulo: Los trabajos afectaban al tramo entre 
Colombia y Mar de Cristal, pero slo estaba cortada la estacin de Pinar del Rey,fecha_noticia: 2022-05-26T09:25:31Z,resultados: 1},{url: https://www.abc.es/economia/abci-amenaza-huelga-ryanair-sindicatos-barajan-paros-europeos-justo-antes-agosto-202205231917_noticia.html,titulo: Amenaza de huelga en Ryanair: los sindicatos barajan paros europeos justo antes de agosto,subtitulo: Los tripulantes de cabina espaoles piden mejoras salariales a la empresa en el nuevo convenio ,fecha_noticia: 2022-05-24T17:33:57Z,resultados: 1},{url: https://www.abc.es/deportes/abci-juan-espino-encara-nueva-etapa-sandford-gustaria-pelear-septiembre-octubre-202205251021_noticia.html,titulo: Juan Espino encara una nueva etapa en el Sandford MMA: Me gustara pelear en septiembre u octubre,subtitulo: El luchador grancanario se recupera de una operacin en sus codos 
con optimismo. El desembarco que prepara UFC en Pars es una fecha que baraja para su regreso. Augusto Sakai sera un rival a tener en cuenta,fecha_noticia: 2022-05-25T08:21:38Z,resultados: -1},{url: https://www.abc.es/cultura/musica/abci-misteriosa-semana-espanola-rolling-stones-202205261740_noticia.html,titulo: La misteriosa semana espaola de los Rolling Stones,subtitulo: La banda britnica ha sorprendido a todos aterrizando en Madrid seis das antes de su concierto en el Wanda Metropolitano,fecha_noticia: 2022-05-27T12:09:01Z,resultados: -1},{url: https://www.abc.es/historia/abci-grandiosa-iglesia-y-hospital-contra-peste-presidio-puerta-durante-500-anos-202010050116_noticia.html,titulo: La grandiosa iglesia y hospital contra la peste que presidi la Puerta del Sol durante 500 aos,subtitulo: Las obras de la estacin de Cercanas de la cntrica plaza madrilea sacaron a la luz los restos de la cimentacin del antiguo templo del Buen Suceso, construido en el siglo XV. Y all estuvo durante varios siglos sufriendo reformas y guerras como de la Independencia contra los franceses, hasta que tuvo que ser demolida en 1854 ,fecha_noticia: 2022-05-27T10:13:25Z,resultados: -1},{url: https://www.abc.es/espana/casa-real/abci-juan-carlos-baraja-visitar-espana-proximo-semana-202205161127_noticia.html,titulo: Juan Carlos I baraja visitar Espaa el prximo fin de semana,subtitulo: Los periodistas Carlos Herrera y Fernando nega han desvelado este lunes los planes del padre del Rey,fecha_noticia: 2022-05-17T09:21:19Z,resultados: -1},{url: https://www.abc.es/historia/abci-infierno-division-azul-campos-concentracion-sovieticos-durante-segunda-guerra-mundial-202012130049_noticia.html,titulo: De Mosc a Odessa: el martirio de la Divisin Azul en los campos de concentracin de Stalin,subtitulo: Morir en el campo de batalla no era el peor destino para los divisionarios espaoles; muchos acabaron sus das en las temibles prisiones soviticas, aunque, en la actualidad, se desconoce el nmero exacto,fecha_noticia: 2022-05-27T10:10:00Z,resultados: 1},{url: https://www.abc.es/play/television/eurovision/abci-chanel-bano-masas-llegada-espana-202205152038_noticia.html,titulo: Chanel se da un bao de masas en su llegada a Espaa,subtitulo: La artista ofrece un concierto en la Plaza Mayor, que se puede ver en RTVE Play,fecha_noticia: 2022-05-15T19:37:58Z,resultados: -1},{url: https://www.abc.es/ultimas-noticias/abci-noticia-ultima-hora-viernes-27-05-2022-cultura-202205270600_noticia.html,titulo: Las ltimas noticias de hoy de actualidad y la ltima hora de cultura del viernes, 27 de mayo del 2022,subtitulo: Repasa las ltimas noticias del da 27 de mayo del 2022.  Averige la ltima hora de los sucesos que ocurren en cultura de ABC.es. El conciso resumen del da en 6 noticias de actualidad para estar informado.,fecha_noticia: 2022-05-27T04:00:36Z,resultados: -1}][{url: https://www.abc.es/deportes/abci-cuba-no-frena-estampida-otro-atleta-escapa-nada-mas-pisar-aeropuerto-barajas-202205261028_noticia.html,titulo: Cuba no frena la estampida: otro atleta se escapa nada ms pisar el aeropuerto Barajas,subtitulo: Jenns Fernndez, 'la centella de Simpson', el gran talento de la velocidad de su pas, abandona su seleccin al llegar a  Espaa ,fecha_noticia: 2022-05-26T09:09:27Z,resultados: -1},{url: https://www.abc.es/espana/madrid/abci-linea-8-metro-reabre-este-sabado-tres-dias-antes-previsto-tras-finalizar-obras-202205241154_noticia.html,titulo: La lnea 8 de Metro reabre este sbado, tres das antes de lo previsto, tras finalizar sus obras,subtitulo: Los trabajos afectaban al tramo entre Colombia y Mar de Cristal, pero slo estaba cortada la estacin de Pinar del Rey,fecha_noticia: 2022-05-26T09:25:31Z,resultados: 1},{url: https://www.abc.es/economia/abci-amenaza-huelga-ryanair-sindicatos-barajan-paros-europeos-justo-antes-agosto-202205231917_noticia.html,titulo: Amenaza de huelga en Ryanair: los sindicatos barajan paros europeos justo antes de agosto,subtitulo: Los tripulantes de cabina espaoles piden mejoras salariales a la empresa en el nuevo convenio ,fecha_noticia: 2022-05-24T17:33:57Z,resultados: 1},{url: https://www.abc.es/deportes/abci-juan-espino-encara-nueva-etapa-sandford-gustaria-pelear-septiembre-octubre-202205251021_noticia.html,titulo: Juan Espino encara una nueva etapa en el Sandford MMA: Me gustara pelear en septiembre u octubre,subtitulo: El luchador grancanario se recupera de una operacin en sus codos con optimismo. El desembarco que prepara UFC en Pars es una fecha que baraja para su regreso. Augusto Sakai sera un rival a tener en cuenta,fecha_noticia: 2022-05-25T08:21:38Z,resultados: -1},{url: https://www.abc.es/cultura/musica/abci-misteriosa-semana-espanola-rolling-stones-202205261740_noticia.html,titulo: La misteriosa semana espaola de los Rolling Stones,subtitulo: La banda britnica ha sorprendido a todos aterrizando en Madrid seis das antes de su concierto en el Wanda Metropolitano,fecha_noticia: 2022-05-27T12:09:01Z,resultados: -1},{url: https://www.abc.es/historia/abci-grandiosa-iglesia-y-hospital-contra-peste-presidio-puerta-durante-500-anos-202010050116_noticia.html,titulo: La grandiosa iglesia y hospital contra la peste que presidi la Puerta del Sol durante 500 aos,subtitulo: Las obras de la estacin de Cercanas de la cntrica plaza madrilea sacaron a la luz los restos de la cimentacin del antiguo templo del Buen Suceso, construido en el siglo XV. Y all estuvo durante varios siglos sufriendo reformas y guerras como de la Independencia contra los franceses, hasta que tuvo que ser demolida en 1854 ,fecha_noticia: 2022-05-27T10:13:25Z,resultados: -1},{url: https://www.abc.es/espana/casa-real/abci-juan-carlos-baraja-visitar-espana-proximo-semana-202205161127_noticia.html,titulo: Juan Carlos I baraja visitar Espaa el prximo fin de semana,subtitulo: Los periodistas Carlos Herrera y Fernando nega han desvelado este lunes los planes del padre del Rey,fecha_noticia: 2022-05-17T09:21:19Z,resultados: -1},{url: https://www.abc.es/historia/abci-infierno-division-azul-campos-concentracion-sovieticos-durante-segunda-guerra-mundial-202012130049_noticia.html,titulo: De Mosc a Odessa: el martirio de la Divisin Azul en los campos de concentracin de Stalin,subtitulo: Morir en el campo de batalla no era el peor destino para los divisionarios espaoles; muchos acabaron sus das en las temibles prisiones soviticas, aunque, en la actualidad, se desconoce el nmero exacto,fecha_noticia: 2022-05-27T10:10:00Z,resultados: 1},{url: https://www.abc.es/play/television/eurovision/abci-chanel-bano-masas-llegada-espana-202205152038_noticia.html,titulo: Chanel se da un bao de masas en su llegada a Espaa,subtitulo: La artista ofrece un concierto en la Plaza Mayor, que se puede ver en RTVE Play,fecha_noticia: 2022-05-15T19:37:58Z,resultados: -1},{url: https://www.abc.es/ultimas-noticias/abci-noticia-ultima-hora-viernes-27-05-2022-cultura-202205270600_noticia.html,titulo: Las ltimas noticias de hoy de actualidad y la ltima hora de cultura del viernes, 27 de mayo del 2022,subtitulo: Repasa las ltimas noticias del da 27 de mayo del 2022.  Averige la ltima hora de los sucesos que ocurren en cultura de ABC.es. El conciso resumen del da en 6 noticias de actualidad para estar informado.,fecha_noticia: 2022-05-27T04:00:36Z,resultados: -1}]"""
string2 = "[{url: texto//de//prueba/:)),texto: nada que ver}]"
print(string2)



