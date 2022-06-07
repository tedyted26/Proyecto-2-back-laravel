# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import request as rq
import ssl
import datetime as dt
import re
from selenium import webdriver
import os

from Noticia import Noticia
import Guardado

def get20MinutosNews(categoria):
    
    listaNoticias = []
    listaLinks = []
    try:
        for paginas in range(1,2):
            
            print(f"20Minutos: Pagina {paginas}")
            
            urlBase = "https://www.20minutos.es/busqueda/"
            urlIntermedio = "/?q="
            urlCola = "&sort_field=&category=&publishedAt%5Bfrom%5D=&publishedAt%5Buntil%5D="

            mainUrl = urlBase + str(paginas) + urlIntermedio + categoria + urlCola
            print(mainUrl)

            html = rq.urlopen(mainUrl, context=ssl.SSLContext()).read()
            soup = BeautifulSoup(html, 'html.parser')
            articulos = soup.findAll("article")
            
            for a in articulos:
                link = a.find("a")["href"]
                listaLinks.append(link)
            
        for link in listaLinks:
            try:
                url = link
                htmlTemp = rq.urlopen(url, context=ssl.SSLContext()).read()
                soupPag = BeautifulSoup(htmlTemp, 'html.parser')

                titulo = soupPag.find("div", class_="title").text
                subtitulo = soupPag.find("div", class_="article-intro").text
                fecha = soupPag.find(class_="article-date").text
                tags = [t.text.strip() for t in soupPag.findAll(class_="tag")]
                textoTmp = soupPag.find(class_="article-text").text
                texto = re.sub("\s+", " ", textoTmp)

                date_regEx = re.compile(r'(\d+.\d+.\d+\s*-\s*\d*:\d*)')
                fecha = dt.datetime.strptime(date_regEx.search(fecha).group(), '%d.%m.%Y - %H:%M')

                n = Noticia(titulo, subtitulo, fecha, url, categoria, "20Minutos", tags, texto)
                listaNoticias.append(n)
            except Exception as e:
                print(e)
    except:
        pass
    
    return listaNoticias

def getElMundoNews(categoria):
    
    listaNoticias = []
    listaLinks = []
    try:
        #print(os.getcwd() + "\chromedriver.exe")
        PATH = os.getcwd() + "\python-codes\chromedriver.exe"
        print(PATH)
        for pagina in range(0,1):
            
            print(f"El Mundo: Pagina {pagina}")
            
            driver = webdriver.Chrome(PATH)
            driver.get(f"https://ariadna.elmundo.es/buscador/archivo.html?q={categoria}&t=1&i={pagina}1&n=10&fd=0&td=0&w=70&s=1&no_acd=1")
            s = driver.page_source
            driver.quit()
            
            soup = BeautifulSoup(s, 'html.parser')
            articulos = soup.findAll("h3")
            
            for a in articulos:
                    link = a.find("a")["href"]
                    listaLinks.append(link)
                    
        for link in listaLinks:
            try:
                url = link
                htmlTemp = rq.urlopen(url, context=ssl.SSLContext()).read()
                soupPag = BeautifulSoup(htmlTemp, 'html.parser')

                divCuerpo = soupPag.find("div", class_="ue-l-article__body ue-c-article__body")
                titulo = soupPag.find(class_="ue-c-article__headline js-headline").text
                subtitulo = soupPag.find(class_="ue-c-article__standfirst").text
                fecha = soupPag.find(class_="ue-c-article__publishdate").find("time")["datetime"]
                textoNoticia = ""
                for p in divCuerpo.find_all("p"):
                    textoNoticia += " "+p.text
                tags = []
                for tag in soupPag.findAll(class_="ue-c-article__tags-item"):
                    tags.append(tag.text)

                date_regEx = re.compile(r'(\d+-\d+-\d+T\d*:\d*:\d*)')
                fecha = dt.datetime.strptime(date_regEx.search(fecha).group(), '%Y-%m-%dT%H:%M:%S')
                n = Noticia(titulo,subtitulo,fecha, url, categoria,"El Mundo", tags, textoNoticia)
                listaNoticias.append(n)
            except Exception as e:
                print(e)
    except:
        pass
            
    return listaNoticias

'''
def getElPaisNews(categoria):
    listaNoticias = []
    return listaNoticias
'''
    
'''
def elPais():
    
    busqueda = "aluche"
    
    noticias = getElPaisNews(busqueda)
    #Guardado.guardarNoticias(noticias, ("/"+busqueda))
'''
    
'''
print(noticias[1].periodico)
print(noticias[1].fecha)
print("\n")
print(noticias[1].titulo)
print("\n")
print(noticias[1].subtitulo)
print("\n")
print(noticias[1].texto)
'''
    
'''
mainUrl = "https://elpais.com/buscador/?q="
buscar = "barajas"
urlBuscador = mainUrl + buscar
'''