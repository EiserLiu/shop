import base64
import io
import re
import asyncio

import numpy as np
from PIL import Image
from asgiref.sync import async_to_sync
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from goods.models import Goods, GoodsGroup, GoodsBanner, Collect, Detail
from goods.permissions import CollectPermission
from goods.serializers import GoodSerializer, GoodsGroupSerializer, GoodsBannerSerializer, CollectSerializer, \
    DetailSerializer, GoodImagesSerializer

"""
商品模块前台接口
1、商城首页：
    返回商品的分类
    返回商品的海报
    返回推荐的商品列表(分页)
2、展示商品的详情信息
3、分类获取商品列表  
    支持分类获取(过滤参数:)
    获取推荐的商品
    根据商品的销量排序、根据价格排序
4、收藏商品(取消)
"""


class IndexView(APIView):
    """商城首页接口"""

    def get(self, request):
        # 获取商品分类信息
        group = GoodsGroup.objects.filter(status=True)
        # 序列化如果有图片字段,返回数据需要补全完整的图片获取域名,需要在序列化时传入请求对象
        group_ser = GoodsGroupSerializer(group, many=True, context={'request': request})
        # 获取商品的海报
        banner = GoodsBanner.objects.filter(status=True)
        banner_ser = GoodsBannerSerializer(banner, many=True)
        # 获取所有的推荐商品
        goods = Goods.objects.filter(recommend=True)
        goods_ser = GoodSerializer(goods, many=True, context={'request': request})
        result = dict(
            group=group_ser.data,
            banner=banner_ser.data,
            goods=goods_ser.data
        )

        return Response(result)


class GoodsView(ReadOnlyModelViewSet):
    """
    商品视图集:
        商品列表接口
        获取单个商品的接口
    """
    queryset = Goods.objects.filter(is_on=True)
    serializer_class = GoodSerializer
    # 实现通过商品分类、和是否推荐进行过滤
    filterset_fields = ('group', 'recommend')
    # 实现通过价格、销量排序
    ordering_fields = ('sales', 'price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 获取商品详情
        detail = Detail.objects.get(goods=instance)
        detail_ser = DetailSerializer(detail)
        result = serializer.data
        result['detail'] = detail_ser.data
        return Response(result)


class CollectView(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    收藏商品视图集:
        create:收藏商品
        delete:取消收藏
        list:收藏列表
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    # 设置认证用户才能有权限访问
    permission_classes = [IsAuthenticated, CollectPermission]

    def create(self, request, *args, **kwargs):
        """收藏商品"""
        # 获取请求参数
        user = request.user
        params_user_id = request.data.get('user')
        # 校验请求参数中的用户ID是否为当前登录的用户
        if user.id != params_user_id:
            return Response({'error': '没有操作其他用户的权限'})
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """获取用户的收藏列表"""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GoodsGroupView(mixins.ListModelMixin, GenericViewSet):
    """商品分类视图"""
    queryset = GoodsGroup.objects.filter(status=True)
    serializer_class = GoodsGroupSerializer


class SimilarImagesView(GenericViewSet):
    """相似商品图片查询"""
    queryset = Goods.objects.filter(is_on=True)
    serializer_class = GoodImagesSerializer

    @action(detail=False, methods=['POST'])
    def similarimages(self, request):
        """
        相似商品图片查询
        ---
        request_serializer:
            name: SimilarImagesSerializer
            fields:
                - cover: 请求的图片数据，可以是InMemoryUploadedFile对象或者base64编码的字符串
        response_serializer:
            name: GoodSerializer
            many: True
        """
        req_image = request.data.get("cover")

        if not req_image:
            return Response({"error": "No image data provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            req_image_obj = self._process_image_data(req_image)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        similar_list = []
        goods_list = self.get_queryset()

        for good in goods_list:
            res_image = good.cover  # 获取商品的封面图片
            try:
                res_image_obj = self._process_image_field(res_image)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            similarity = self._compute_image_similarity(req_image_obj, res_image_obj)
            if similarity > 0.1:  # 假设相似度阈值是0.1
                similar_list.append(good)

        serializer = GoodSerializer(similar_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _process_image_data(self, image_data):
        """
        处理请求中的图片数据
        :param image_data: 请求中的图片数据，可以是InMemoryUploadedFile对象或者base64编码的字符串
        :return: PIL的Image对象
        """
        if isinstance(image_data, InMemoryUploadedFile):
            image_content = image_data.read()
        elif isinstance(image_data, str) and image_data.startswith('data:image'):
            base64_data = re.search(r'data:image[^;]+;base64,([a-zA-Z0-9+/=]+)', image_data).group(1)
            image_content = base64.b64decode(base64_data)
        else:
            raise ValueError("Invalid image data for req_image")

        return Image.open(io.BytesIO(image_content))

    def _process_image_field(self, image_field):
        """
        处理商品模型中的图片字段
        :param image_field: 商品模型中的图片字段，可能是InMemoryUploadedFile对象或者字符串
        :return: PIL的Image对象
        """
        if isinstance(image_field, ImageFieldFile):
            return Image.open(io.BytesIO(image_field.read()))
        else:
            return image_field

    def _compute_image_similarity(self, img1, img2):
        """
        计算两张图片的相似度
        :param img1: PIL的Image对象
        :param img2: PIL的Image对象
        :return: 相似度，范围是0到1
        """
        if img1.size != img2.size:
            img1 = img1.resize(img2.size)

        h1 = np.array(img1.histogram())
        h2 = np.array(img2.histogram())
        rms = np.sqrt(np.mean((h1 - h2) ** 2))
        similarity = 1 - rms / np.sqrt(np.mean(h1 ** 2) * np.mean(h2 ** 2))
        return similarity
