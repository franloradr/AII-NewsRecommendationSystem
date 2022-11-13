from main.forms import TermsForm
from django.shortcuts import render, get_object_or_404

from main.models import Noticia, Usuario, Seccion, Autor, DictSection, DictAuthor
from django.contrib.auth.models import User

from main.populate import populateDatabase
from main.populateIndex import populateIndexer

from whoosh.index import open_dir
import os
from whoosh import qparser
from whoosh.qparser import MultifieldParser
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.template import loader
from math import log

#  CONJUNTO DE VISTAS

@login_required(login_url="/accounts/login")
def index(request):
    return render(request, 'index.html')


@login_required(login_url="/accounts/login")
def populateDB(request):
    populateDatabase() 
    return render(request, 'populate.html')


@login_required(login_url="/accounts/login")
def populateIndex(request):
    populateIndexer()
    return render(request, 'populateIndex.html')


@login_required(login_url="/accounts/login")
def searcher(request):
    if request.method == 'GET':
        form = TermsForm(request.GET, request.FILES)
        if form.is_valid():
            terms = form.cleaned_data['terms']
            dirpath = os.getcwd() + "\\trabajo_aii\\main\\Index"
            ix = open_dir(dirpath)
            try:
                searcher = ix.searcher()
            except:
                populateIndexer()
                searcher = ix.searcher()
            query = terms
            mparser = MultifieldParser(["seccion", "titulo", "autor", "descripcion", "link", "contenido"],
                                       schema=ix.schema,
                                       group=qparser.OrGroup).parse(query)
            results = searcher.search(mparser)
            items = []
            for r in results:
                items.append({'seccion':r['seccion'],
                              'titulo':r['titulo'],
                              'autor':r['autor'],
                              'descripcion':r['descripcion'],
                              'noticiaId':r['pk'],
                              'link':r['link'],
                              'contenido':r['contenido']})
            searcher.close()
            return render(request, 'news_matched.html', {'lista':items})
    form = TermsForm()
    return render(request, 'search_new.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            usuario = Usuario.objects.create(idUsuario=user.pk, user=user)
            for seccion in Seccion.objects.all():
                DictSection.objects.create(user=usuario, key=seccion.nombreSeccion, value=1)
            for autor in Autor.objects.all():
                DictAuthor.objects.create(user=usuario, key=autor.nombreAutor, value=1)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url="/accounts/login")
def detallesNoticia(request, noticiaId):
    template = loader.get_template('noticia.html')
    noticia = get_object_or_404(Noticia, pk=noticiaId)
    print("Entrando!")
    current_user = request.user
    
    usuario = Usuario.objects.get(idUsuario=current_user.pk)
    
    """ Cuidado aquí, si se trata de una nueva noticia cuya sección y autor no existían antes
        el usuario no tendrá la sección y el autor en su diccionario de preferencias """
    
    try:
        obj = DictSection.objects.get(user=usuario, key=noticia.seccion.nombreSeccion)
    except:
        print("No existe dicha seccion")
        obj = DictSection.objects.create(user=usuario, key=noticia.seccion.nombreSeccion, value=1)
    obj.value = obj.value + 1
    obj.save()
    
    try:
        obj = DictAuthor.objects.get(user=usuario, key=noticia.autor.nombreAutor)
    except:
        print("No existe dicho autor")
        obj = DictAuthor.objects.create(user=usuario, key=noticia.autor.nombreAutor, value=1)
    obj.value = obj.value + 1
    obj.save()
    
    context = {
        'noticia': Noticia.objects.get(noticiaId=noticiaId)
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/accounts/login")
def CBRecommendationSystem(request):
    """ [(new1, weight), (new2, weight), ...]"""
    weighted_news = []
    
    """ 70% de peso la sección, 30% de peso el autor """
    suma_secciones = 0
    suma_autores = 0
    
    """ recuperamos el usuario actual loggeado 
        al que vamos a recomendarle alguna noticia """
    current_user = Usuario.objects.get(idUsuario=request.user.pk)
    
    """ recuperamos las preferencias del usuario actual """
    prefs = {'seccion':{}, 'autor':{}, 'palabras':{}}
    for seccion in Seccion.objects.all():
        try:
            value = DictSection.objects.get(user=current_user, key=seccion.nombreSeccion).value
        except:
            # Con suavizado de laplace, todos habrán visitado al menos 1 vez cada seccion
            obj = DictSection.objects.create(user=current_user, key=seccion.nombreSeccion, value=1)
            value = obj.value
        prefs['seccion'][seccion.nombreSeccion] = value
        suma_secciones = suma_secciones + value
        
    for autor in Autor.objects.all():
        try:
            value = DictAuthor.objects.get(user=current_user, key=autor.nombreAutor).value
        except:
            # Con suavizado de laplace, todos habrán visitado al menos 1 vez cada autor
            obj = DictAuthor.objects.create(user=current_user, key=autor.nombreAutor, value=1)
            value = obj.value
        prefs['autor'][autor.nombreAutor] = value
        suma_autores = suma_autores + value
    
    for noticia in Noticia.objects.all():        
        normal = prefs['seccion'][noticia.seccion.nombreSeccion] / suma_secciones
            
        section_weight = 70/100*normal
        """ log-version to avoid underflow """
        #section_weight = log(70 / 100 + normal)
                   
        normal = prefs['autor'][noticia.autor.nombreAutor] / suma_autores
            
        author_weight = 30/100*normal
        """ log-version to avoid underflow """
        #author_weight = log(30 / 100 + normal)
            
        weighted_news.append((noticia, section_weight + author_weight))
    
    """ Ordenamos para tener las noticias con más peso las primeras """
    weighted_news = sorted(weighted_news, key=lambda x: x[1], reverse=True)

    """ recomienda 3 """
    return render(request, 'news_recommended.html', {'lista':[new[0] for new in weighted_news[:3]]})