# Generated by Django 4.2 on 2024-04-10 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': (('cancel_product_publication', 'Can cancel product publication'), ('change_product_description', 'Can change product description'), ('change_product_category', 'Can change product category')), 'verbose_name': 'продукт', 'verbose_name_plural': 'продукты'},
        ),
    ]