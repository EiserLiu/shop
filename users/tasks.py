from celery import shared_task

from common.aliyun_message import AliyunSMS


@shared_task
def send_code(mobile, code):
    # 发送短信验证码
    result = AliyunSMS().send(mobile=mobile, code=str(code))
    return result
