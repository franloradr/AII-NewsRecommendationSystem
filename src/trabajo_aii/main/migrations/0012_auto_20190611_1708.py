# Generated by Django 2.1.7 on 2019-06-11 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_usuario_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictauthor',
            name='id',
            field=models.AutoField(auto_created=True, default=23, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dictsection',
            name='id',
            field=models.AutoField(auto_created=True, default=24, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dictauthor',
            name='key',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='dictsection',
            name='key',
            field=models.CharField(max_length=50),
        ),
    ]
