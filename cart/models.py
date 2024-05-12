from django.db import models

from common.db import BaseModel


class Cart(BaseModel):
    """
    购物车模型:
        保存购物车中的数据
    """
    user = models.ForeignKey('users.User', help_text='用户ID', verbose_name='用户ID', on_delete=models.CASCADE,
                             blank=True)
    goods = models.ForeignKey('goods.Goods', help_text='商品ID', verbose_name='商品ID', on_delete=models.CASCADE)
    number = models.SmallIntegerField(help_text='商品数量', verbose_name='商品数量', default=1, blank=True)
    is_checked = models.BooleanField(help_text='是否选中', verbose_name='是否选中', default=True, blank=True)

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
