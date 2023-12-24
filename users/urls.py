from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import LoginView, RegisterView, UserView, AddrView

urlpatterns = [
    # 登录
    path('login/', LoginView.as_view()),
    # 注册
    path('register/', RegisterView.as_view()),
    # 刷新token
    path('token/refresh/', TokenRefreshView.as_view()),
    # 校验token
    path('token/verify/', TokenVerifyView.as_view()),
    # 获取单个用户信息的路由
    path('users/<int:pk>/', UserView.as_view({'get': 'retrieve'})),
    # 上传用户头像的路由
    path('<int:pk>/avatar/upload/', UserView.as_view({
        "post": "upload_avatar"
    })),
    # 添加地址和获取地址列表的路由
    path('address/',AddrView.as_view({
        "post": "create",
        "get": "list",
    })),
    # 修改收货地址和删除收货地址
    path('address/<int:pk>/',AddrView.as_view({
        "put": "update",
        "delete": "destroy",
    })),
    # 设置默认收货地址
    path('address/<int:pk>/default/', AddrView.as_view({
        "put": "set_default_addr",
    })),
]
