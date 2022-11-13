from django.contrib import admin
from main.models import Seccion, Autor, Noticia, Usuario, DictSection, DictAuthor

admin.site.register(Seccion)
admin.site.register(Autor)
admin.site.register(Noticia)
admin.site.register(Usuario)
admin.site.register(DictSection)
admin.site.register(DictAuthor)