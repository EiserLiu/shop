import os
import random
import re

import redis
from django.http import FileResponse
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from common.aliyun_message import AliyunSMS
from shop.settings import MEDIA_ROOT
from users.models import User, Addr
from .permissions import UserPermission, AddrPermission
from .serializers import UserSerializer, AddrSerializers

# Create your views here.

throttle_classes = [AnonRateThrottle]
POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=100)  # 建立连接池


class RegisterView(APIView):

    def post(self, request):
        """注册"""
        # 1.接受用户的参数
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        mobil = request.data.get('mobil')
        password_confirmation = request.data.get('password_confirmation')
        # 2.用户校验
        # 校验参数是否为空
        if not all([username, password, email, password_confirmation, mobil]):
            return Response({'error': '所有参数不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校验用户名是否已注册
        if User.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校验两次密码是否一致
        if password != password_confirmation:
            return Response({'error': '两次密码不一致'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校验密码长度
        if not 6 <= len(password) <= 18:
            return Response({'error': '密码长度需要在6到18位之间'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校验邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return Response({'error': '邮箱已被其他用户注册'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 验证邮箱格式是否正确
        if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
            return Response({'邮箱格式有误!'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 验证手机号是否已经注册
        if User.objects.filter(mobile=mobil).exists():
            return Response({'error': '手机号已经被注册'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 3.创建用户
        obj = User.objects.create_user(username=username, email=email, password=password)
        res = {
            'username': username,
            'id': obj.id,
            'email': obj.email
        }
        return Response(res, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # 自定义登录成功之后返回的结果
        result = serializer.validated_data
        result['id'] = serializer.user.id
        result['username'] = serializer.user.username
        result['email'] = serializer.user.email
        result['mobile'] = serializer.user.mobile
        result['token'] = result.pop('access')
        return Response(result, status=status.HTTP_200_OK)


class UserView(GenericViewSet, mixins.RetrieveModelMixin):
    """用户相关操作视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 设置认证用户才能有权限访问
    permission_classes = [IsAuthenticated, UserPermission]

    def upload_avatar(self, request, *args, **kwargs):
        """上传用户头像"""
        avatar = request.data.get('avatar')
        # 校验是否有上传文件
        if not avatar:
            return Response({'error': '上传失败,文件不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if avatar.size > 1024 * 300:
            return Response({'error': '文件大小不能超过300kb'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 保存文件
        user = self.get_object()
        ser = self.get_serializer(user, data={'avatar': avatar}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'url': ser.data['avatar']})

    def bind_mobile(self, request, *args, **kwargs):
        """绑定手机号"""
        code = request.data.get('code')
        mobile = request.data.get('mobile')
        # 校验参数
        result = self.verif_code(code, mobile)
        if result:
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 3、校验手机号
        if User.objects.filter(mobile=mobile).exists():
            return Response({'message': '该手机号已被用户绑定'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 绑定手机号
        user = request.user
        print(user.mobile)
        print(user.id)
        print(user.username)
        user.mobile = mobile
        user.save()

        return Response({"message": "绑定手机号"}, status=status.HTTP_200_OK)

    def unbind_mobile(self, request, *args, **kwargs):
        """解绑手机号"""
        # 1、获取参数
        code = request.data.get('code')  # 获取验证码
        mobile = request.data.get('mobile')  # 获取手机号

        # 2、校验参数
        result = self.verif_code(code, mobile)
        if result:
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 3、解绑手机
        user = request.user
        print(user.mobile)
        print(user.id)
        print(user.username)
        if user.mobile == mobile:
            user.mobile = ''
            user.save()
            return Response({'massage:': '解绑手机号成功'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '当前用户绑定的不是该号码'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def update_name(self, request, *args, **kwargs):
        """修改用户昵称"""
        # 获取参数
        last_name = request.data.get('last_name')
        # 校验参数
        if not last_name:
            return Response({'error': '参数last_name为必传字段'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 修改用户名
        user = self.get_object()
        user.last_name = last_name
        user.save()
        return Response({'message': '修改昵称成功'}, status=status.HTTP_200_OK)

    def update_email(self, request, *args, **kwargs):
        """修改用户邮箱的视图"""
        # 1、获取参数
        email = request.data.get('email')
        user = self.get_object()
        # 2、校验参数
        # 参数不能为空
        if not email:
            return Response({'error': '邮箱不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校验邮箱格式
        if not re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return Response({'error': '邮箱格式不正确'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 邮箱地址和之前是否相同
        if user.email == email:
            return Response({'message': 'OK'}, status=status.HTTP_200_OK)
        # 邮箱是否已被绑定
        if User.objects.filter(email=email).exists():
            return Response({'error': '邮箱已被其他用户绑定'})
        # 3、修改邮箱
        user.email = email
        user.save()
        return Response({'message:': 'OK'})

    def update_password(self, request, *args, **kwargs):
        """修改密码视图"""
        # 1、获取参数
        user = self.get_object()
        code = request.data.get('code')
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')
        # 2、校验参数
        result = self.verif_code(code, mobile)
        if result:
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if user.mobile != mobile:
            return Response({'error': '验证码有误'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 3、校验密码
        if not password:
            return Response({'error': '密码不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if 6 >= len(password) or len(password) >= 18:
            return Response({'error': '密码长度需要在6到18位之间'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if password != password_confirmation:
            return Response({'error': '两次输入密码不一致'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 4、修改密码
        user.set_password(password)
        user.save()
        return Response({'massage': '密码修改成功'}, status=status.HTTP_200_OK)

    @staticmethod
    def verif_code(code, mobile):
        """
        :param code: 验证码
        :param mobile: 手机号
        :return: 通过返回 None，失败返回 Response
        """
        # 1、校验参数
        if not code:
            return {'error': '验证码不能为空'}
        if not mobile:
            return {'error': '手机号不能为空'}

        # 2、校验验证码
        conn = redis.Redis(connection_pool=POOL)
        key = f"verif_code:{mobile}"

        stored_code = conn.get(key)
        if stored_code is None:
            return {'error': '无效验证码'}

        stored_code = stored_code.decode('utf-8')  # 解码 bytes 为字符串
        if stored_code != code:
            return {'error': '验证码错误'}

        # 删除 Redis 中的验证码
        conn.delete(key)

        return None


class FileView(APIView):
    def get(self, request, name):
        path = MEDIA_ROOT / name
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)


class AddrView(GenericViewSet,
               mixins.ListModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               mixins.UpdateModelMixin):
    """地址管理视图集"""
    queryset = Addr.objects.all()
    serializer_class = AddrSerializers
    # 设置认证用户才能有权限访问
    permission_classes = [IsAuthenticated, AddrPermission]

    # 指定过滤字段
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 通过请求过来的用户进行过滤
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_default_addr(self, request, *args, **kwargs):
        """设置默认收货地址"""
        # 1. 获取到要设置的地址对象
        obj = self.get_object()
        obj.is_default = True
        obj.save()
        # 2. 将该地址设置默认收货地址,将用户的其他收货地址设置为非默认
        queryset = self.get_queryset().filter(user=request.user)
        for item in queryset:
            if item != obj:
                item.is_default = False
                item.save()
        return Response({"message": "设置成功"}, status=status.HTTP_200_OK)


class SendSMSView(APIView):
    """发送短信验证码"""

    def post(self, request):
        # 获取手机号码
        mobile = request.data.get('mobile')
        # 验证手机号码格式是否正确(正则表达式)
        res = re.match(r"^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$", mobile)
        if not res:
            return Response({'error': '无效的手机号码'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 随机生成一个6位数的验证码
        code = self.get_random_code()
        # 发送短信验证码
        result = AliyunSMS().send(mobile=mobile, code=code)
        if result['code'] == 'OK':
            # 将短信验证码入库
            conn = redis.Redis(connection_pool=POOL)
            conn.set(name=mobile, value=code, ex=60 * 5)

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_random_code(self):
        # 随机生成一个6位数的验证码
        # code2 = ''.join([random.choice(range(10)) for i in range(6)])
        code = ''
        for i in range(6):
            # 随机生成0-9之间的一个数据
            n = random.choice(range(10))
            code += str(n)
        return code
