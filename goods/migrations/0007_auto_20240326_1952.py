# Generated by Django 3.2 on 2024-03-26 11:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_alter_collect_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='collect',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collect',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='删除标记'),
        ),
        migrations.AddField(
            model_name='collect',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='更新时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goodsgroup',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goodsgroup',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='删除标记'),
        ),
        migrations.AddField(
            model_name='goodsgroup',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='更新时间'),
            preserve_default=False,
        ),
    ]
