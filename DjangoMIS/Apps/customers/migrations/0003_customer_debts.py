# Generated by Django 4.2.2 on 2023-10-10 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_remove_customer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='debts',
            field=models.FloatField(default=0),
        ),
    ]
