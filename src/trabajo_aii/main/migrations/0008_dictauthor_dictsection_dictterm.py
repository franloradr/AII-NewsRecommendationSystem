# Generated by Django 2.1.7 on 2019-06-10 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190610_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='DictAuthor',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('value', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='DictSection',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('value', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='DictTerm',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('value', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Usuario')),
            ],
        ),
    ]
