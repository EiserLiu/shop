"""
商品序列化器
"""
from .models import Goods, GoodsBanner, GoodsGroup, Detail, Collect
from rest_framework import serializers


class GoodSerializer(serializers.ModelSerializer):
    """商品序列化器"""

    class Meta:
        model = Goods
        fields = "__all__"


class GoodsBannerSerializer(serializers.ModelSerializer):
    """商品海报序列化器"""

    class Meta:
        model = GoodsBanner
        fields = "__all__"


class GoodsGroupSerializer(serializers.ModelSerializer):
    """商品分类序列化器"""

    class Meta:
        model = GoodsGroup
        fields = "__all__"


class CollectSerializer(serializers.ModelSerializer):
    """商品收藏序列化器"""

    class Meta:
        model = Collect
        fields = "__all__"


class DetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""

    class Meta:
        model = Detail
        fields = "__all__"
