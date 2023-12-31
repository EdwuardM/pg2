# Generated by Django 4.1.5 on 2023-10-08 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='last_name',
            new_name='company_name',
        ),
        migrations.AddField(
            model_name='supplier',
            name='assessment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
