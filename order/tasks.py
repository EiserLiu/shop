from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def send_order_status():
    # 获取所有需要发送状态的订单
    orders = Order.objects.filter(status='shipped')
    for order in orders:
        # 发送邮件通知用户
        send_mail(
            '您的订单状态信息',
            f'您的订单状态{order.id} has been shipped.',
            '1071519731@qq.com',
            [order.user.email],
            fail_silently=False,
        )
