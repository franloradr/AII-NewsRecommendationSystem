# Generated by Django 2.1.7 on 2019-06-10 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190608_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='apellidos',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='codigoPostal',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='edad',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='ocupacion',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='sexo',
        ),
    ]
