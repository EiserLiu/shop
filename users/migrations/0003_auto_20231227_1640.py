# Generated by Django 3.2 on 2023-12-27 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_user_id_addr_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addr',
            options={'verbose_name': '收货地址表', 'verbose_name_plural': '收货地址表'},
        ),
        migrations.AlterModelOptions(
            name='area',
            options={'verbose_name': '地区表', 'verbose_name_plural': '地区表'},
        ),
        migrations.AlterModelOptions(
            name='verifcode',
            options={'verbose_name': '手机验证码表', 'verbose_name_plural': '手机验证码表'},
        ),
        migrations.RenameField(
            model_name='addr',
            old_name='counnty',
            new_name='county',
        ),
    ]
