from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from goods.models import Goods, GoodsGroup, GoodsBanner, Collect
from goods.permissions import CollectPermission
from goods.serializers import GoodSerializer, GoodsGroupSerializer, GoodsBannerSerializer, CollectSerializer

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
        group_ser = GoodsGroupSerializer(group, many=True)
        # 获取商品的海报
        banner = GoodsBanner.objects.filter(status=True)
        banner_ser = GoodsBannerSerializer(banner, many=True)
        # 获取所有的推荐商品
        goods = Goods.objects.filter(recommend=True)
        goods_ser = GoodSerializer(goods, many=True)
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
