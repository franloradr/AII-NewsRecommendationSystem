# -*- coding: utf-8 -*-    
from main.models import Noticia
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC
import os

def get_schema():
    return Schema(pk=NUMERIC(stored=True),
                  seccion=TEXT(stored=True), 
                  titulo=TEXT(stored=True),
                  autor=TEXT(stored=True),
                  descripcion=TEXT(stored=True),
                  link=TEXT(stored=True),
                  contenido=TEXT(stored=True)
                  )

def crea_index(dirindex):
    
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    if not len(os.listdir(dirindex))==0:
        sn='s' 
    else:
        sn='s' 
    if sn == 's':
            ix = create_in(dirindex, schema=get_schema())
            return ix

def populateIndexer():
    dirpath = os.getcwd() + "\\trabajo_aii\\main\\Index"
    ix = crea_index(dirpath)
    writer = ix.writer()
    """ Based on actual BBDD previous loaded, not CSV """
    for noticia in Noticia.objects.all():
        try:
            writer.add_document(pk=noticia.pk,
                                seccion=noticia.seccion.nombreSeccion,
                                titulo=noticia.titulo,
                                autor=noticia.autor.nombreAutor,
                                descripcion=noticia.descripcion,
                                link=noticia.link,
                                contenido=noticia.contenido)
        except:
            print("Exception catch during insert in Schema")
    writer.commit()

if __name__ == '__main__':
    populateIndexer()
