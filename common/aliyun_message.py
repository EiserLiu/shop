"""
专用测试签名/模板
签名名称:阿里云短信测试
使用场景:发送测试短信
模版名称:测试专用模板
模版Code:SMS_154950909
模版类型:验证码
模版内容:您正在使用阿里云短信测试服务，体验验证码是：${code}，如非本人操作，请忽略本短信！

"""
# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.

import json
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_util.models import RuntimeOptions


class AliyunSMS:
    # 必填，您的 AccessKey ID,
    access_key_id = "LTAI5tSpZABv5epY231sgqpL"
    # 必填，您的 AccessKey Secret,
    access_key_secret = "3ItdCrvCF0uz87PjLKNvNuTdbnfH3Q"
    endpoint = 'dysmsapi.aliyuncs.com'
    sign_name = '阿里云短信测试'
    template_code = 'SMS_154950909'

    def __init__(self):
        self.config = Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            endpoint=f'dysmsapi.aliyuncs.com'
        )

    def send(self, mobile: str, code: str):
        """
        :param mobile:手机号
        :param code: 验证码
        :return:
        """
        # 1、创建客户端
        client = Client(self.config)
        # 2、创建短信对象
        send_sms_request = SendSmsRequest(
            sign_name=self.sign_name,
            template_code=self.template_code,
            phone_numbers=mobile,
            template_param=json.dumps({"code": code})
        )
        # 3、设置运行时间选项
        runtime = RuntimeOptions()
        # 4、发送短信
        try:
            res = client.send_sms_with_options(send_sms_request, runtime)
            if res.body.code == 'OK':
                return {'code': "OK", "message": "短信发送成功"}
            else:
                return {"cede": "NO", "error": res.body.message}
        except Exception as e:
            return {'code': 'NO', 'error': '短信发送失败'}


if __name__ == '__main__':
    # AliyunSMS().send(mobile='17692275126', code='12138')
    import os

    # 获取当前工作目录的路径
    current_working_directory = os.getcwd()
    # 打印当前工作目录的路径
    print(current_working_directory)
