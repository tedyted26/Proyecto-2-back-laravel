#External Imports

import re
import requests
from bs4 import BeautifulSoup
from urllib import request as rq
import ssl
import bs4
#import json

#Internal Imports
from Noticia import Noticia
from Guardado import guardarNoticias




def scraper_la_sexta_bs4(busqueda, count_pages):
    lista_noticias = []
    url_base = "https://www.lasexta.com/"
    url_odio = f"temas/{busqueda}-"
    url = url_base + url_odio + str(count_pages)
    urls = []
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        articulos = soup.findAll("article")
        for articulo in articulos: 
                urls.append(articulo.find("a")["href"])
                #print("#################")
                #print("Articulo")
                #print(articulo)
        print("\n#######################")
        print("Aca comienzan cada noticia desde la URL.\n")
        print("Parrafos:")
        conjuntoParrafos = []

        for url in urls:
            try:
                
                htmlTemp = rq.urlopen(url, context=ssl.SSLContext()).read()
                soupPag = BeautifulSoup(htmlTemp, 'html.parser')
                h1 = soupPag.find('h1', {'class':'title-new'})
                title = h1.get_text()
                #print(title)
                subtitle =soupPag.find('sumary', {'class':'entradilla'})
                entradilla = subtitle.get_text()
            
                p_s = soupPag.find('div',{'class':'articleBody'})
                parrafo_completo = ""
                fecha = ""
                for element in p_s:
                    if type(element) == bs4.element.Tag:
                        #print(element.name)
                        if element.name =="p":
                            parrafo_completo += str(element.text).strip()
                    else:
                        pass
                
                tags = soupPag.find('ul',{'class':'listado-categorias'})
                
                listado_categorias_list = tags.get_text().strip().split("\n")
                
                fecha = []
                fecha_articulo = soupPag.findAll("span", {"class":'article-dates__day'})
                for date in fecha_articulo:
                    fecha.append(date.text)
                n = Noticia(title, entradilla, fecha, url, busqueda, "LaSexta", listado_categorias_list, parrafo_completo)
                lista_noticias.append(n)
            except Exception as e:
                print("Error aca" + str(e))     
    except:
        pass
    return lista_noticias


if __name__ == "__main__":
    import Guardado

    busqueda = "valencia"
    lista = scraper_la_sexta_bs4("Madrid", 2)
    Guardado.guardarNoticias(lista, ("/"+busqueda))
