# Generated by Django 3.1.7 on 2021-03-03 20:30

import diagnosticApp.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosticApp', '0002_auto_20210303_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=stdimage.models.StdImageField(upload_to=diagnosticApp.models.get_file_path, verbose_name='Imagem'),
        ),
    ]