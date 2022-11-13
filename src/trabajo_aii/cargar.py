'''
Created on 11 mar. 2019

@author: Dani Moreno, Francisco Jesus Belmonte


                 <------------------------------------------------------------------------------>
                 < El fin de este fichero es generar un archivo ".csv" que contenga multitud    >
                 < de noticias correspondientes a una gran variedad de categorías, extraídas    >
                 < del diario digital "OKDiario".                                               >
                 <------------------------------------------------------------------------------>
                
'''

# encoding:utf-8
import urllib.request
import os
from bs4 import BeautifulSoup

urlPortada = "https://okdiario.com/"
ficheroPortada = "ficherosSecciones/ficheroPortada"


def abrir_url(url, file):
    try: 
        urllib.request.urlretrieve(url, file)
        return file
    except: 
        print("Error al conectarse a la pagina " + url)
        return None


seccionesTotales = []
temasTotales = []


def cargar_datos_inicial(url, file, seccVistas):
    
    if os.path.isfile(file):
        reload = input("Existe el registro " + file + ", desea recargarlo? (Introduzca 'S' para recargar)\n")
        if reload == "S":
            print("Se esta recargando la informacion...")
            abrir_url(url, file)
            print("Informacion cargada correctamente")
    else:
        abrir_url(url, file)

    archivo = open(file, "r", encoding="utf-8")
    soup = BeautifulSoup(archivo, 'html.parser')
    
    secc = soup.find("ul", {"class":"okdiario-secciones-menu-navegacion-ul"})
    tem = soup.findAll("h2", {"class":"article-title"})
    
    for s in secc:
        nombreSeccion = s.a.contents[0].encode("utf-8")
        enlaceSeccion = s.a["href"]
        if not enlaceSeccion.startswith("https://okdiario.com/"):
            enlaceSeccion = "https://okdiario.com/" + enlaceSeccion
           
        if (nombreSeccion not in seccVistas) & (nombreSeccion != "Mercados") & (nombreSeccion != "Actualidad") & (nombreSeccion != "Famosos") & (nombreSeccion != "Casa Real") & (nombreSeccion != "Estilo") & (nombreSeccion != "OKDIARIO") & (nombreSeccion != "Diario Madridista") & (nombreSeccion != "Look"):
            seccionesTotales.append((nombreSeccion, enlaceSeccion))
            seccVistas.append(nombreSeccion)
            print("Seccion visitada: " + nombreSeccion)
            cargar_datos_inicial(enlaceSeccion, "ficherosSecciones/ficheroSeccion" + nombreSeccion, seccVistas)
        
    for t in tem:
        temasTotales.append(t.contents[0])
        
    return (seccionesTotales, temasTotales)


def cargar_datos_existente(file, seccVistas):
    archivo = open(file, "r", encoding="utf-8")
    soup = BeautifulSoup(archivo, 'html.parser')
    
    secc = soup.find("ul", {"class":"okdiario-secciones-menu-navegacion-ul"})
    
    for s in secc:
        nombreSeccion = s.a.contents[0]
        enlaceSeccion = s.a["href"]
        if not enlaceSeccion.startswith("https://okdiario.com/"):
            enlaceSeccion = "https://okdiario.com/" + enlaceSeccion
           
        if (nombreSeccion not in seccVistas) & (nombreSeccion != "Mercados") & (nombreSeccion != "Actualidad") & (nombreSeccion != "Famosos") & (nombreSeccion != "Casa Real") & (nombreSeccion != "Estilo") & (nombreSeccion != "OKDIARIO") & (nombreSeccion != "Diario Madridista") & (nombreSeccion != "Look") & (nombreSeccion != "V�deos"):
            nombreFichero = "ficherosSecciones/ficheroSeccion" + nombreSeccion
            seccionesTotales.append((nombreSeccion, enlaceSeccion, nombreFichero))
            seccVistas.append(nombreSeccion)
            cargar_datos_existente(nombreFichero, seccVistas)


def cargar_temas_secciones():
    print("Cargando los temas de todas las secciones...")
    s = 0
    for (secc, _, fich) in seccionesTotales:
        print("\nSeccion " + secc + " (" + str(s) + "/" + str(seccionesTotales.__len__()) + ")\n-------------------")
        s = s + 1
        archivo = open(fich, "r", encoding="utf-8")
        soup = BeautifulSoup(archivo, 'html.parser')
        temas = soup.findAll("article")
        
        i = 0
        for t in temas:
            if i % 10 == 0:
                print("Tema " + str(i) + " de " + str(temas.__len__()))
            i = i + 1
            enlaceTema = t.find("a")["href"]
            titulo = t.header.h2.contents[0]
            descr = t.find("p", {"class":"article-lead"})
            if descr.contents != []:
                descr = descr.contents[0]
            else:
                descr = ""
            autor = t.find("li", {"class":"article-author"}).span.contents[0]
            pag = urllib.request.urlopen(enlaceTema)
            soup = BeautifulSoup(pag, 'html.parser')
            cuerpo = soup.find("div", {"class":"entry-content"}).findAll("p")
            contenido = []
            for parrafo in cuerpo:     
                texto = parrafo.get_text() + "\n"
                contenido.append(texto)
            
            temasTotales.append((secc, titulo, autor, descr, enlaceTema, contenido))

            
def cargar_datos():
    print("Cargando datos...")
    # cargar_datos_inicial(urlPortada, ficheroPortada, [])
    cargar_datos_existente(ficheroPortada, [])
    cargar_temas_secciones()
    print("Carga de datos finalizada")
    print("Generando archivo CSV")
    generarCSV()
    print("Carga de datos finalizada")

    
# -*- coding: utf-8 -*-    
import csv


def generarCSV():
    with open('okdiario.csv', 'w') as csvFile:
        fieldnames = ['secc', 'titulo', 'autor', 'descr', 'enlaceTema', 'contenido']
        writer = csv.DictWriter(csvFile, delimiter=";", fieldnames=fieldnames)
        writer.writeheader()
        for tupla in temasTotales:
            try:
                diccionario = {fieldnames[i]:(tupla[i]) for i in range(len(fieldnames))}
                writer.writerow(diccionario)
            except:
                print("##########\nException catch:\n" + str(tupla) + "\n##########")
    csvFile.close()


if __name__ == '__main__':
    i = 0
    with open('okdiario.csv') as csvFile:
        fieldnames = ['secc', 'titulo', 'autor', 'descr', 'enlaceTema', 'contenido']
        reader = csv.DictReader(csvFile, delimiter=";", fieldnames=fieldnames)
        for row in reader:
            print("fila: " + str(i))
            print("########################")
            print("seccion: " + row['secc'])
            print("titulo: " + row['titulo'])
            print("autor: " + row['autor'])
            print("descripcion: " + row['descr'])
            print("enlace: " + row['enlaceTema'])
            print("contenido: " + row['contenido'])
            i = i + 1
        print("fila: " + str(i))
    csvFile.close()
