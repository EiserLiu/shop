import os
import re
from django.http import FileResponse
from rest_framework import status, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from shop.settings import MEDIA_ROOT
from users.models import User, Addr
from .permissions import UserPermission, AddrPermission
from .serializers import UserSerializer, AddrSerializers
from rest_framework.permissions import IsAuthenticated


# Create your views here.

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
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


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

    def set_default_addr(self,request, *args, **kwargs):
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
