import os
import random

import redis

from common.aliyun_message import AliyunSMS
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

app = Celery('shop')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=100)  # 建立连接池


@app.task
def send_code(mobile):
    # 随机生成一个6位数的验证码
    code = get_random_code()
    # 发送短信验证码
    result = AliyunSMS().send(mobile=mobile, code=code)
    return result, code


def get_random_code():
    # 随机生成一个6位数的验证码
    # code2 = ''.join([random.choice(range(10)) for i in range(6)])
    code = ''
    for i in range(6):
        # 随机生成0-9之间的一个数据
        n = random.choice(range(10))
        code += str(n)
    return code
