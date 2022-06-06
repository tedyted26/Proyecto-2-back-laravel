from bs4 import BeautifulSoup
from urllib import request as rq
import time

import bisect

def getPueblosEspana():

    urlbase = "https://www.todopueblos.com/"

    req = rq.Request(urlbase, headers={'User-Agent': 'Mozilla/5.0'})
    html = rq.urlopen(req, timeout=10).read()
    soup = BeautifulSoup(html, 'html.parser')

    resultados = soup.findAll("table")[2]
    links = resultados.findAll("a")

    listaPueb = []
    ppp = ""

    for i in links:
        listaPueb.append( i.text.replace("Pueblos de ",""))
    listaPueb.sort()
    for i in listaPueb:
        t = "\""+i+"\","
        ppp += t
    print(ppp)
    pueblos = []
    '''
    for i in links:
        url_busq = urlbase + i["href"][1:]
        print("Inicio con url_busq: ", url_busq)
        reqTemp = rq.Request(url_busq, headers={'User-Agent': 'Mozilla/5.0'})
        print("REQ ", url_busq)
        try:
            htmlTemp = rq.urlopen(reqTemp, timeout=10).read()
        except:
            print("reintentar")
            htmlTemp = rq.urlopen(reqTemp, timeout=10).read()
        print("HTML ", url_busq)
        soupTemp = BeautifulSoup(htmlTemp, 'html.parser')
        print("fin busqueda: ", url_busq)
        tabla = soupTemp.findAll("table", attrs={"bgcolor": "#FEFCE6"})[2]
        
        pueblosTemp = tabla.text.split("\n")
        print("Introducion ordenada: ", url_busq)
        for p in pueblosTemp:
            if p != "" and p != " ":
                bisect.insort(pueblos, p)
        print("fin")
    

    print(len(pueblos))
    txt = "\n".join(pueblos)
    f = open("pueblos_espana.txt", "w")
    f.write(txt)
    '''

getPueblosEspana()

