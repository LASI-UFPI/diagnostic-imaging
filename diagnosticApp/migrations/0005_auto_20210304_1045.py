# Generated by Django 3.1.7 on 2021-03-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosticApp', '0004_auto_20210303_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='diagnostic',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Diagnóstico'),
        ),
    ]