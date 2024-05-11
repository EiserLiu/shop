# Generated by Django 5.0.3 on 2024-05-11 00:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("goods", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                    "addr",
                    models.CharField(
                        help_text="收货地址", max_length=256, verbose_name="收货地址"
                    ),
                ),
                (
                    "number",
                    models.SmallIntegerField(
                        blank=True, default=1, help_text="商品数量", verbose_name="商品数量"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("待处理", "PENDING"),
                            ("处理中", "PROCESSING"),
                            ("已发货", "SHIPPED"),
                            ("已送达", "DELIVERED"),
                            ("已取消", "CANCELLED"),
                        ],
                        default="待处理",
                        help_text="订单状态",
                        max_length=8,
                        verbose_name="订单状态",
                    ),
                ),
                (
                    "goods",
                    models.ForeignKey(
                        help_text="商品ID",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="goods.goods",
                        verbose_name="商品ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单表",
                "verbose_name_plural": "订单表",
                "db_table": "Order",
            },
        ),
    ]
