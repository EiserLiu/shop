from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from cart.models import Cart
from cart.permissions import CartPermission
from cart.serializers import CartSerializer, ReadCartSerializer


class CartView(mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               GenericViewSet
               ):
    permission_classes = [IsAuthenticated, CartPermission]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_serializer_class(self):
        """实现读写操作使用不同的序列化器"""
        if self.action == 'list':
            return ReadCartSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        """添加商品到购物车"""
        # 获取用户信息
        user = request.user
        # 获取参数
        goods = request.data.get('goods')
        # request.data['user'] = user.id
        # 校验参数
        # 1、校验购物车中是否已经有该商品
        if Cart.objects.filter(user=user, goods=goods).exists():
            # 该用户已经添加过该商品到购物车,直接增加商品数量
            cart_goods = Cart.objects.get(user=user, goods=goods)
            cart_goods.number += request.data.get('number')
            cart_goods.save()
            # 对商品进行序列化
            serializer = self.get_serializer(cart_goods)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 没有商品则调用父类的create方法进行创建
            request.data['user'] = user.id
            return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """获取购物车商品列表"""
        # user = request.user
        # queryset = Cart.objects.filter(user=user)
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update_goods_status(self, request, *args, **kwargs):
        """修改商品选中状态"""
        obj = self.get_object()
        obj.is_checked = not obj.is_checked
        obj.save()
        return Response({'message': '当前状态:' + str(obj.is_checked)}, status=status.HTTP_200_OK)

    def update_goods_number(self, request, *args, **kwargs):
        """修改商品的数量"""
        # 获得参数
        number = request.data.get('number')
        obj = self.get_object()
        # 校验参数
        if not isinstance(number, int):
            return Response({'error': '参数只能为int类型且不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if number > obj.goods.stock:
            return Response({'error': '数量不能超过该商品的库存'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 判断number是否为0
        elif number <= 0:
            # 删除该商品
            obj.delete()
            return Response({'message': '删除成功'})
        else:
            # 修改商品数量
            obj.number = number
            obj.save()
            return Response({'message': '修改成功'})

