from django.db import models

from common.db import BaseModel
from shop.enums import OrderStatus


class Order(BaseModel):
    user = models.ForeignKey('users.User', help_text='用户ID', verbose_name='用户ID', on_delete=models.DO_NOTHING)
    goods = models.ForeignKey('goods.Goods', help_text='商品ID', verbose_name='商品ID', on_delete=models.DO_NOTHING)
    addr = models.CharField(max_length=256, help_text='收货地址', verbose_name='收货地址')
    number = models.SmallIntegerField(help_text='商品数量', verbose_name='商品数量', default=1, blank=True)
    status = models.CharField(max_length=8, default=OrderStatus.PENDING.value, help_text='订单状态',
                              verbose_name='订单状态',
                              blank=True, choices=[(status.value, status.name) for status in OrderStatus])

    def __str__(self):
        return f'{self.user}在{self.addr}买了{self.goods}'

    class Meta:
        db_table = 'Order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name
