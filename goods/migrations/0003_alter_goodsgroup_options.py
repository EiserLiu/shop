# Generated by Django 3.2 on 2023-12-27 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20231227_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodsgroup',
            options={'verbose_name': '商品分类表', 'verbose_name_plural': '商品分类表'},
        ),
    ]
