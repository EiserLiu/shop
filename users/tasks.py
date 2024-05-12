from celery import shared_task

from common.aliyun_message import AliyunSMS
from shop.celery import app


@app.task
def send_code(mobile, code):
    # 发送短信验证码
    result = AliyunSMS().send(mobile=mobile, code=str(code))
    return result


@shared_task
def task_test(a, b):
    return a + b
