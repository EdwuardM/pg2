# Generated by Django 4.2.2 on 2023-10-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_pricebuy'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.FloatField(default=0),
        ),
    ]