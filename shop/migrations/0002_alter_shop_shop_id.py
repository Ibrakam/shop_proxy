# Generated by Django 4.2.18 on 2025-01-23 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_id',
            field=models.IntegerField(max_length=255, unique=True),
        ),
    ]
