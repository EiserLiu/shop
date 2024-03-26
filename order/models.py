from common.db import BaseModel
from django.db import models


class Order(BaseModel):
    user = models.ForeignKey('users.User', help_text='用户ID', verbose_name='用户ID', on_delete=models.DO_NOTHING)
    goods = models.ForeignKey('goods.Goods', help_text='商品ID', verbose_name='商品ID', on_delete=models.DO_NOTHING)
    addr = models.ForeignKey('users.Addr', help_text='地址ID', verbose_name='地址ID', on_delete=models.DO_NOTHING)
    number = models.SmallIntegerField(help_text='商品数量', verbose_name='商品数量', default=1, blank=True)

    def __str__(self):
        return f'{self.user}在{self.addr}买了{self.goods}'

    class Meta:
        db_table = 'Order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name
