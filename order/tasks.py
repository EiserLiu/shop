from celery import shared_task, Task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings
from shop.celery import app


class SendEmailTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        # 任务成功执行
        info = f'订单状态发送成功:任务id:{task_id}'
        send_mail('celery监控任务成功', info, settings.EMAIL_HOST_USER, ['1071519731@qq.com'])

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # 任务成功执行
        info = f'订单状态发送失败:任务id:{task_id}'
        send_mail('celery监控任务成功', info, settings.EMAIL_HOST_USER, ['1071519731@qq.com'])


@shared_task
def send_order_status():
    orders = Order.objects.filter(status='待处理')
    for order in orders:
        print(123456)
        send_mail(
            '您的订单状态信息',
            f'您的订单{order}待处理',
            settings.EMAIL_HOST_USER,
            [order.user.email],
            fail_silently=False,
        )
