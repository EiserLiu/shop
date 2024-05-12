from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from goods.models import Goods
from goods.permissions import CollectPermission
from .models import Order
from .serializers import OrderSerializers
from shop.enums import OrderStatus
from .tasks import send_order_status


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
            number: int = request.data.get('number')
            good = Goods.objects.select_for_update().get(id=good_id)
            if int(good.stock) >= int(number):
                good.stock -= int(number)
                good.sales += int(number)
                good.save()
                return instance
            else:
                return Response({"error": "库存不足"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_status(self, request, *args, **kwargs):
        status_value = request.data.get('status')
        try:
            order_id = request.data.get('id')
            if not order_id:
                return Response({"error": "订单ID未提供"}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.get(id=order_id)
            if status_value in [statu.value for statu in OrderStatus]:
                order.status = status_value
            order.save()  # 保存更改
            return Response({"message": "状态修改成功"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "订单不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendEmailView(APIView):
    """发送短信验证码"""

    def get(self, request):
        # 发送短信验证码的异步任务
        async_result = send_order_status.delay()

        # 返回任务的ID，客户端可以使用这个ID来查询任务的状态和结果
        return Response({'task_id': async_result.id}, status=status.HTTP_202_ACCEPTED)
