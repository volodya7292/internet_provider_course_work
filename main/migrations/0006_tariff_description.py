# Generated by Django 3.1.3 on 2020-11-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20201115_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
    ]
