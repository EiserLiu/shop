from django.db.models import Model
from django.db import models
class BaseModel(Model):
    """抽象模型字段:定义公共字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False,verbose_name='删除标记')

    class Meta:
        # 声明这是一个抽象模型,执行迁移文件时,不会在数据中生成表
        abstract = True
        verbose_name_plural = "公共字段表"
        db_table = 'BaseTable'
