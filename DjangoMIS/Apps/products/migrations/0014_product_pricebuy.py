# Generated by Django 4.2.2 on 2023-10-15 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_rename_cantidadmaxima_rulesupply_maximumquantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='priceBuy',
            field=models.FloatField(default=0),
        ),
    ]
