# Generated by Django 2.0 on 2018-11-10 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0012_auto_20181109_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuenta',
            name='codigo_cuenta',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='cuentahija',
            name='codigo_cuenta',
            field=models.IntegerField(blank=True),
        ),
    ]
