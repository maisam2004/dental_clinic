# Generated by Django 3.2.25 on 2024-05-10 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_has_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='has_sizes',
        ),
    ]
