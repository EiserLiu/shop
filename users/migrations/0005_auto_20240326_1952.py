# Generated by Django 3.2 on 2024-03-26 11:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20231227_1821'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VerifCode',
        ),
        migrations.AddField(
            model_name='addr',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addr',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='删除标记'),
        ),
        migrations.AddField(
            model_name='addr',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='更新时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='area',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='area',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='删除标记'),
        ),
        migrations.AddField(
            model_name='area',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='更新时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='删除标记'),
        ),
        migrations.AddField(
            model_name='user',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='更新时间'),
            preserve_default=False,
        ),
    ]
