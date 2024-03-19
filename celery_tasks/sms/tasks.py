import random
import re

import redis
from rest_framework import status
from rest_framework.response import Response

from celery_tasks.main import app
from common.aliyun_message import AliyunSMS



@app.task
def send_code(mobile):
    # 验证手机号码格式是否正确(正则表达式)
    res = re.match(r"^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$", mobile)
    if not res:
        return Response({'error': '无效的手机号码'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    # 随机生成一个6位数的验证码
    code = get_random_code()
    # 发送短信验证码
    result = AliyunSMS().send(mobile=mobile, code=code)
    if result['code'] == 'OK':
        # 将短信验证码入库
        conn = redis.Redis(connection_pool=POOL)
        conn.setex(name=mobile, time=60 * 5, value=code)
        key = conn.get(name=mobile)
        result['key'] = key
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_random_code():
    # 随机生成一个6位数的验证码
    # code2 = ''.join([random.choice(range(10)) for i in range(6)])
    code = ''
    for i in range(6):
        # 随机生成0-9之间的一个数据
        n = random.choice(range(10))
        code += str(n)
    return code
