from celery import shared_task, Task
from django.conf import settings
from django.core.mail import send_mail

from goods.models import Goods
from .models import Order


class SendEmailTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        # 任务成功执行
        info = f'订单状态发送成功:任务id:{task_id}'
        send_mail('celery监控任务成功', info, settings.EMAIL_HOST_USER, ['1071519731@qq.com'])

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # 任务成功执行
        info = f'订单状态发送失败:任务id:{task_id}'
        send_mail('celery监控任务成功', info, settings.EMAIL_HOST_USER, ['1071519731@qq.com'])


@shared_task(base=SendEmailTask, bind=True)
def update_stock_and_status(self, order_id, status_value):
    order = Order.objects.get(id=order_id)
    good = Goods.objects.select_for_update().get(id=order.goods_id)
    if good.stock >= order.number:
        good.stock -= order.number
        good.sales += order.number
        good.save()
        order.status = status_value
        order.save()
    else:
        raise ValueError("库存不足")


@shared_task(base=SendEmailTask, bind=True)
def send_order_status(self):
    orders = Order.objects.filter(status='待处理')
    for order in orders:
        print(order)
        send_mail(
            '您的订单状态信息',
            f'您的订单{order}待处理',
            settings.EMAIL_HOST_USER,
            [order.user.email],
            fail_silently=False,
        )
