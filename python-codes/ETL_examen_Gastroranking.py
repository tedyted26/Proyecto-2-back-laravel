# Teodora Nikolaeva Nikolova 21955169 Checkpoint 2 PC2 2022
from bs4 import BeautifulSoup
from urllib import request as rq

import ssl

url = "https://gastroranking.es/"
html = None
print("pillando enlaces")

# ver que hacer con los resultados de la busqueda que no llevan a ninguna parte
try:
    html = rq.urlopen(url, context=ssl.SSLContext()).read()
    print("conexion realizada")
except:
    print("Pagina no encontrada")

if html != None:
    ciudades = {}
    soup = BeautifulSoup(html, 'html.parser')
    ciudades_container = soup.find(class_ = "container provinceList")
    ciudades_raw = ciudades_container.find_all("a")
    
    for i in ciudades_raw:
        ciudades[i.text] = i["href"]
        print(i.text)
    input_ciudad = input("\nELIGE UNA CIUDAD (Escribela tal cual aparece): ")

    url_2 = url.removesuffix("/") + ciudades[input_ciudad]
    html = None

    print("\n")
    try:
        html = rq.urlopen(url_2, context=ssl.SSLContext()).read()
        print("conexion realizada")
    except:
        print("Pagina no encontrada")
    
    print("\n")
    if html != None:
        poblaciones = {}
        soup = BeautifulSoup(html, 'html.parser')
        poblaciones_raw = soup.find_all(class_ = "site_map_il")

        for i in poblaciones_raw:
            texto = str(i.find("a").text)
            texto.split("(")
            poblaciones[texto] = i.find("a")["href"]
            print(texto)
        input_poblacion = input("\nELIGE UNA POBLACION (Escribela tal cual aparece): ")

        url_3 = url.removesuffix("/") + poblaciones[input_poblacion]
        print(url_3)
        html = None

        print("\n")
        try:
            html = rq.urlopen(url_3, context=ssl.SSLContext()).read()
            print("conexion realizada")
        except:
            print("Pagina no encontrada")
        print("\n")

        if html != None:
            restaurantes = {}
            media = 0
            total = 0
            soup = BeautifulSoup(html, 'html.parser')
            restaurantes_raw = soup.find_all(class_="text-left")

            '''
            
            PAGINACION
            
            '''
            filters = "&page="
            page = 2
            end = False
            while end != False:
                print("paginando: ", page)
                url_pag = url + filters + str(page)
                html_pag = None

                try:
                    html_pag = rq.urlopen(url_pag, context=ssl.SSLContext()).read()
                except:
                    end = True

                if html_pag != None:
                    soup_pag = BeautifulSoup(html_pag, 'html.parser')
                    restaurantes_raw.extend(soup.find_all(class_="text-left"))
                    page = page + 1

            '''
            
            '''

            for i in restaurantes_raw:
                texto = str(i.find("a").text).strip()
                url_relativa = i.find("a")["href"]
                restaurantes[texto] = i.find("a")["href"]
                print(texto)

                url_4 = url.removesuffix("/") + url_relativa
                html = None

                try:
                    html = rq.urlopen(url_4, context=ssl.SSLContext()).read()
                except:
                    pass

                if html != None:
                    soup = BeautifulSoup(html, 'html.parser')
                    valoraciones_container = soup.find_all(class_="fieldranking")
                    for i in valoraciones_container:
                        if i.find("label").text == "Precio":
                            media = media + float(i.find(class_="nota").text)
                            total = total + 1
                            break # para que no haya mas iteraciones una vez se ha encontrado el precio

            if media != 0 and total != 0:
                media = media/total
            print("\nLA MEDIA DE TODOS LOS RESTAURANTES DE LA ZONA ES: ", media)


            
        
