import os
import random

import redis

from common.aliyun_message import AliyunSMS
from shop.celery import app

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=100)  # 建立连接池


@app.task
def send_code(mobile, code):
    # 发送短信验证码
    result = AliyunSMS().send(mobile=mobile, code=str(code))
    return result

