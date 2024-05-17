from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from goods.models import Goods
from goods.permissions import CollectPermission
from users.models import User
from .models import Order
from .serializers import OrderSerializers
from shop.enums import OrderStatus
from .tasks import send_order_status, update_stock_and_status


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
            # 发送任务来更新库存和状态
            update_stock_and_status.delay(order_id=instance.id, status_value='PENDING')
            return instance
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
                # 发送任务来更新状态
                update_stock_and_status.delay(order_id, status_value)
                return Response({"message": "状态修改成功"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "订单不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class SendEmailView(APIView):
#     """发送短信验证码"""
#
#     def get(self, request):
#         orders = Order.objects.filter(status='待处理')
#         order_users = orders.values_list('user', flat=True)
#         print(orders)
#
#         for order in orders:
#             print(order)
#
#         # 遍历每个订单的用户信息
#         for user_id in order_users:
#             # 获取用户对象
#             user = User.objects.get(id=user_id)
#             # 打印用户邮箱
#             print(user.email)
#         # 发送短信验证码的异步任务
#         result = send_order_status.delay(orders)
#         # 返回任务的ID，客户端可以使用这个ID来查询任务的状态和结果
#         return Response({'message': result.get()}, status=status.HTTP_200_OK)
