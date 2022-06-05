# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:48:32 2022

@author: Yago
"""
import os
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%d-%m-%Y.%Hh%Mm")
#from pathlib import Path


def guardarNoticias( listaN: list, ruta):
    fechaAnterior = ""
    for n in listaN:
        try:
            nuevaFecha = str(n.fecha)
            
            if(current_time != fechaAnterior):
                noticiasDiarias = 1
            else:
                noticiasDiarias = noticiasDiarias + 1
                
            nombreArchivo = n.categoria + "." + current_time + "." + str(noticiasDiarias).zfill(3) + ".txt"
            #print(nombreArchivo)

            s = "\n#####\n"
            texto = f"{n.url}{s}" \
                    f"{n.periodico}{s}" \
                    f"{n.categoria}{s}" \
                    f"{n.fecha}{s}" \
                    f"{n.titulo}{s}" \
                    f"{n.subtitulo}{s}" \
                    f"{n.texto}{s}" \
                    f"{n.tags}" \
                # Path(ruta).mkdir(parents=True, exist_ok=True)
            cd = os.getcwd() + "/python-codes/noticias-scrapeadas" + "/"+n.periodico

            if not os.path.exists(cd):
                os.mkdir(cd)
            cd2 = cd + ruta

            if not os.path.exists(cd2):
                os.mkdir(cd2)
            f = open(os.path.join(cd2, nombreArchivo), "w", encoding="utf-8")
            f.write(texto)
            f.close()
            fechaAnterior = current_time
        except Exception as e:
            print(e)

def pasarNoticiasATexto( listaN: list):
    noticiasTexto = []
    for n in listaN:
        s = "\n#####\n"
        texto = f"{n.url}{s}" \
                f"{n.periodico}{s}" \
                f"{n.categoria}{s}" \
                f"{n.fecha}{s}" \
                f"{n.titulo}{s}" \
                f"{n.subtitulo}{s}" \
                f"{n.texto}{s}" \
                f"{n.tags}"
        noticiasTexto.append(texto)
    return noticiasTexto
