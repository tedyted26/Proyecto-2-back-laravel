from bs4 import BeautifulSoup
from urllib import request as rq
from Noticia import Noticia
import Guardado as save

import ssl

def getLaVanguardiaNews(categoria:str, num_pags = 1):
    noticias = []
    urlbase = "https://stories.lavanguardia.com/search?q="
    url = urlbase + categoria + "&author=&category=&section=&startDate=&endDate=&sort="
    html = None
    print(url)
    print("pillando enlaces")

    # ver que hacer con los resultados de la busqueda que no llevan a ninguna parte
    try:
        html = rq.urlopen(url, context=ssl.SSLContext()).read()
        print("conexion realizada")
    except:
        print("Pagina no encontrada")

    if html != None:
        resultados = []
        soup = BeautifulSoup(html, 'html.parser')
        # recoger todos los <article class="result"
        resultados.extend(soup.find_all(class_="result"))
        print("recogiendo articulos")

        # para paginación
        # pagina 1: https://stories.lavanguardia.com/search?q=salamanca
        # pagina 2: https://stories.lavanguardia.com/search?q=salamanca&author=&category=&section=&startDate=&endDate=&sort=&page=2
        # no funciona si uso el enlace de la pag 2 para la 1

        filters = "&page="
        page = 2
        while page < num_pags:
            print("paginando: ", page)
            url_pag = url + filters + str(page)
            html_pag = None

            # esto es por si tiene menos paginas de las que queremos pillar
            try:
                html_pag = rq.urlopen(url_pag, context=ssl.SSLContext()).read()
            except:
                page = num_pags

            if html_pag != None:
                soup_pag = BeautifulSoup(html_pag, 'html.parser')
                resultados.extend(soup_pag.find_all(class_="result"))
                page = page + 1

        

        # dentro de las noticia
        for article in resultados:
            url_art = article.find("a")["href"]
            html_art = rq.urlopen(url_art, context=ssl.SSLContext()).read()
            soup_art = BeautifulSoup(html_art, 'html.parser')

            titulo = soup_art.find(class_="title").text

            subtitulos = soup_art.find_all(class_="epigraph")
            subtitulo = ""
            for sub in subtitulos:
                subtitulo = subtitulo + sub.text

            # FIXME a lo que tienen los demas
            fecha = soup_art.find("time")["datetime"]

            texto_entero = soup_art.find(class_="article-modules").find_all("p")
            texto = ""
            for p in texto_entero:
                texto = texto + p.text

            noticias.append(Noticia(titulo, subtitulo, fecha, url_art, categoria, "La Vanguardia", [], texto))
    return noticias 
