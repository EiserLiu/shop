from django.contrib import admin
from .models import GoodsGroup, Goods, Detail, GoodsBanner, Collect


@admin.register(GoodsGroup)
class GoodsGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'price', 'stock', 'sales', 'is_on']


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['goods', 'producer', 'norms']


@admin.register(GoodsBanner)
class GoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods']
