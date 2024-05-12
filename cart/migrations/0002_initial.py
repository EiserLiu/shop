# Generated by Django 5.0.3 on 2024-05-12 11:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cart", "0001_initial"),
        ("goods", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="goods",
            field=models.ForeignKey(
                help_text="商品ID",
                on_delete=django.db.models.deletion.CASCADE,
                to="goods.goods",
                verbose_name="商品ID",
            ),
        ),
    ]
