# import mongoengine
# from datetime import datetime
#
# from shop.settings import DATABASES
#
# # 使用connect()方法链接MongoDB
# # NAME 会自动映射为 settings.py 中的数据库名
# mongoengine.connect(DATABASES['mongodb']['NAME'])
#
#
# # Create your models here.
#
# # 此处继承的是 mongoengine.Document
# class History(mongoengine.Document):
#     uid = mongoengine.StringField()  # 用户ID
#     sid = mongoengine.StringField()  # 商品ID
#     shop_type = mongoengine.StringField()  # 商品类型
#     watch_time = mongoengine.DateTimeField(default=datetime.now(), required=True)
