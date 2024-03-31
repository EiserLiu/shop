import os
from celery import Celery

# 配置文件路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")

app = Celery('shop')

app.config_from_object('django.conf:settings', namespace='CELERY')

# 在以注册的APP中读取task.py文件
app.autodiscover_tasks()
