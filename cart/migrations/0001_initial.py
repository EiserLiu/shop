# Generated by Django 5.0.3 on 2024-05-12 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="更新时间"),
                ),
                ("is_delete", models.BooleanField(default=False, verbose_name="删除标记")),
                (
                    "number",
                    models.SmallIntegerField(
                        blank=True, default=1, help_text="商品数量", verbose_name="商品数量"
                    ),
                ),
                (
                    "is_checked",
                    models.BooleanField(
                        blank=True, default=True, help_text="是否选中", verbose_name="是否选中"
                    ),
                ),
            ],
            options={
                "verbose_name": "购物车",
                "verbose_name_plural": "购物车",
                "db_table": "cart",
            },
        ),
    ]
