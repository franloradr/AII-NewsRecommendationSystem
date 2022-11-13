from main.models import Seccion, Autor, Noticia, Usuario
from django.contrib.auth.models import User
from main.populateIndex import populateIndexer

# -*- coding: utf-8 -*-    
import csv

import os
 
dirpath = os.getcwd() + "\\trabajo_aii\\okdiario.csv"
foldername = os.path.basename(dirpath)


def deleteTables():
    Seccion.objects.all().delete()
    Autor.objects.all().delete()
    """ Noticia deleted due to cascade deletion from Seccion or Autor """
    Noticia.objects.all().delete()
    """ DictSection and DictAuthor deleted due to cascade deletion from Usuario
        Usuario deleted due to cascade deletion from User
        User.objects.all().delete()
    """


def populateSecciones(secc):
    try:
        s = Seccion.objects.create(nombreSeccion=secc)
        print(secc)
    except:
        """ Entonces devolvemos la referencia a la seccion """
        s = Seccion.objects.get(nombreSeccion=secc)
    return s


def populateAutores(autor):
    try:
        a = Autor.objects.create(nombreAutor=autor)
    except:
        """ Entonces devolvemos la referencia al autor """
        a = Autor.objects.get(nombreAutor=autor)
    return a


from ast import literal_eval

            
def populateNoticias():
    print("Cargando noticias...")
    with open(os.getcwd() + "\\trabajo_aii\\okdiario.csv") as csvFile:
        fieldnames = ['secc', 'titulo', 'autor', 'descr', 'enlaceTema', 'contenido']
        reader = csv.DictReader(csvFile, delimiter=";", fieldnames=fieldnames)
        for row in reader:
            try:
                
                listaContenido = literal_eval(row['contenido'])
                conten = ''.join(str(elem) for elem in listaContenido)
                Noticia.objects.create(seccion=populateSecciones(row['secc']),
                                       titulo=row['titulo'],
                                       autor=populateAutores(row['autor']),
                                       descripcion=row['descr'],
                                       link=row['enlaceTema'],
                                       contenido=conten)
            except:
                print("Excepción capturada en la linea --> " + str(row))
    csvFile.close()


def populateDatabase():
    deleteTables()
    populateNoticias()
    populateIndexer()
    print("Base de datos cargada correctamente")


if __name__ == '__main__':
    populateDatabase()
