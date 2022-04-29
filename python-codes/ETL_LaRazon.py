# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib import request as rq
import datetime as dt
import ssl

import re

import os
from pathlib import Path

from Noticia import Noticia
import Guardado

def getLaRazonNews(categoria):
    listaNoticias = []
    listaLinks = []
    for paginas in range(1,3):
        urlBase = "https://www.larazon.es/resultados-de-busqueda/"
        mainUrl = urlBase+categoria+'/'+str(paginas)
    
        html = rq.urlopen(mainUrl, context=ssl.SSLContext()).read()
        soup = BeautifulSoup(html, 'html.parser')
    
        for a in soup.findAll('article', {'class': 'card grid--has-6-col card--is-horizontal'}):
            listaLinks.append(a.find("a")["href"])
            
        for link in listaLinks:
            try:
                url = link
                htmlTemp = rq.urlopen(url, context=ssl.SSLContext()).read()
                soupPag = BeautifulSoup(htmlTemp, 'html.parser')
                
                art = soupPag.find('article', {'class':'article-body'})
                
                for header in soupPag.findAll('article', {'class':'article-body'}):
                    for h1 in soupPag.findAll('h1'):
                        titulo = h1.get_text()
                
                for header in soupPag.findAll('article', {'class':'article-body'}):
                    for h2 in soupPag.find('h2'):
                        subtitulo = h2   
                        
                
                parrafos = art.findAll('p')
                conjuntoParrafos = []
                for x in range(len(parrafos)):
                    conjuntoParrafos.append(parrafos[x].get_text())
                texto = " ".join(conjuntoParrafos)
                
                artags = soupPag.find('div',{'class':'article__tags'})
                dd = artags.findAll('dd')
                conjuntoTags = []
                for x in range(len(dd)):
                    conjuntoTags.append(dd[x].get_text())

                fechaTmp = art.select('time')[0]['datetime']
                partes = fechaTmp.split("T")[0].split("-")
                fecha = "-".join(reversed(partes))
                
                #fecha = dt.datetime.strptime(fecha, '%d-%m-%Y')

                n = Noticia(titulo, subtitulo, fecha, url, categoria, "LaRazon", conjuntoTags, texto)
                listaNoticias.append(n)
            except Exception as e:
                print(e)   
    return listaNoticias

def laRazon():
    busqueda = "barajas"
    noticias = getLaRazonNews(busqueda)
    #guardarNoticias(noticias, ("/"+busqueda))
    Guardado.guardarNoticias(noticias, ("/"+busqueda))

laRazon()