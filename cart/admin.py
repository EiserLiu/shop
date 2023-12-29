from django.contrib import admin
from .models import Cart


# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'number', 'is_checked']
