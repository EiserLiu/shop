from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from goods.models import Goods
from goods.permissions import CollectPermission
from .models import Order
from .serializers import OrderSerializers


class OrderView(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    permission_classes = [IsAuthenticated, CollectPermission]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            instance = super().create(request, *args, **kwargs)
            good_id = request.data.get('goods')
            number = request.data.get('number')
            good = Goods.objects.select_for_update().get(id=good_id)
            if good.stock >= number:
                good.stock -= number
                good.sales += number
                good.save()
                return instance
            else:
                return Response({"error": "库存不足"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_status(self, request, *args, **kwargs):
        try:
            order_id = request.data.get('id')
            if not order_id:
                return Response({"error": "订单ID未提供"}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.get(id=order_id)
            order.status = not order.status  # 切换状态
            order.save()  # 保存更改
            return Response({"message": "状态修改成功"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "订单不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)