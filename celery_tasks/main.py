from celery import Celery
import os

# 创建celery实例对象
app = Celery("shop")

# 把celery和django进行组合, 识别和加载django的配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "../shop/settings")

# 通过APP对象加载配置
app.config_from_object('celery_tasks.config')

# 加载任务
# 参数必须是一个列表.每个任务都是任务的路径名称
app.autodiscover_tasks([
    "celery_tasks.sms",
])
