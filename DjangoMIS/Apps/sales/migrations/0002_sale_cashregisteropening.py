# Generated by Django 4.1.5 on 2023-10-05 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='cashRegisterOpening',
            field=models.ForeignKey(db_column='cashRegisterOpening', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sales.cashregisteropening'),
        ),
    ]
