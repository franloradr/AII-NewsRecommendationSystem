# Generated by Django 2.1.7 on 2019-06-08 11:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190606_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreAutor', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Ocupacion',
            fields=[
                ('nombreOcupacion', models.TextField(unique=True, verbose_name='Ocupacion')),
                ('ocupacionId', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaPuntuacion', models.DateField(blank=True, null=True)),
                ('puntuacion', models.PositiveSmallIntegerField(help_text='Introduzca su puntuación del 1 al 5', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Puntuación')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idUsuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(help_text='Introduzca su nombre', verbose_name='Nombre')),
                ('apellidos', models.TextField(help_text='Introduzca sus apellidos', verbose_name='Apellidos')),
                ('edad', models.PositiveSmallIntegerField(help_text='Debe introducir una edad', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Edad')),
                ('sexo', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], help_text='Debe introducir una edad', max_length=1, verbose_name='Sexo')),
                ('codigoPostal', models.CharField(max_length=5, verbose_name='Codigo Postal')),
                ('ocupacion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Ocupacion')),
            ],
        ),
        migrations.RemoveField(
            model_name='film',
            name='genres',
        ),
        migrations.RemoveField(
            model_name='film',
            name='ratings',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='film',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userinformation',
            name='occupation',
        ),
        migrations.AlterField(
            model_name='noticia',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Autor'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='link',
            field=models.URLField(validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='nombreSeccion',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.DeleteModel(
            name='Film',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Occupation',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='UserInformation',
        ),
        migrations.AddField(
            model_name='puntuacion',
            name='noticia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Noticia'),
        ),
        migrations.AddField(
            model_name='puntuacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Usuario'),
        ),
        migrations.AddField(
            model_name='noticia',
            name='ratings',
            field=models.ManyToManyField(through='main.Puntuacion', to='main.Usuario'),
        ),
    ]
