# Generated by Django 5.0.1 on 2024-01-23 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name_plural': 'Корзины пользователей'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name_plural': 'Товары в корзинах пользователей'},
        ),
    ]
