import redis
from celery import shared_task
from django.conf import settings

from common.aliyun_message import AliyunSMS


@shared_task
def send_code(mobile, code):
    key = mobile
    # 设置过期时间
    conn = redis.Redis(connection_pool=settings.REDIS_POOL)
    conn.setex(key, 300, code)
    print(mobile)
    print(code)
    # 发送短信验证码
    result = AliyunSMS().send(mobile=mobile, code=str(code))
    return result
