from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator


class Seccion(models.Model):
    nombreSeccion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombreSeccion

class Autor(models.Model):
    nombreAutor = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.nombreAutor

class Usuario(models.Model):
    idUsuario = models.TextField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.idUsuario

""" Modelling Prefs Dictionary under consistency """
class DictSection(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    key = models.CharField(max_length = 50)
    value = models.IntegerField()
    
    def __str__(self):
        return str("Seccion: "+self.key+" - Frecuencia: "+str(self.value)+" - Usuario: "+str(self.user.idUsuario))
    
class DictAuthor(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    key = models.CharField(max_length = 50)
    value = models.IntegerField()
    
    def __str__(self):
        return str("Autor: "+self.key+" - Frecuencia: "+str(self.value)+" - Usuario: "+str(self.user.idUsuario))
""" Modelling Prefs Dictionary under consistency """

class Noticia(models.Model):
    noticiaId = models.AutoField(primary_key=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    """ Many to one """
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=1000)
    link = models.URLField(validators=[URLValidator()])
    contenido = models.TextField(max_length=10000)
    
    def __str__(self):
        return self.titulo