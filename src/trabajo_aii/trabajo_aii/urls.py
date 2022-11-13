#encoding:utf-8

from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from main import views

urlpatterns = [
    path('', views.index),
    path('populate', views.populateDB),
    path('populateIndex', views.populateIndex),
    path('searcher', views.searcher),
    path('admin/', admin.site.urls),
    url(r'^signup/$', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    #url(r'^noticia/(?P<noticiaId>[0-9]+)', views.detallesNoticia, name="noticia"),
    url(r'^noticia/(?P<noticiaId>\d+)', views.detallesNoticia, name="noticia"),
    url(r'^recomendacion/$', views.CBRecommendationSystem, name='recomendacion'),
]
