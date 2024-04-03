from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.documentation import include_docs_urls

# 获取文件的视图
from users.views import FileView

schema_view = get_schema_view(
    openapi.Info(
        title="商城项目接口文档",
        default_version="v1.0.0",
        description="商城项目,原本是b2b,越做越像b2c",
        contact=openapi.Contact(email="1071519731@qq.com"),
        url=""
    ),
    public=True,
)

urlpatterns = [
    # 接口文档
    path('docs/', include_docs_urls(title='商城项目接口文档')),
    # 自动生成的 Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    # 后台
    path("admin/", admin.site.urls),
    # 获取图片资源接口
    re_path(r'file/image/(.+?)/', FileView.as_view()),
    # 用户模块接口
    path('api/user/', include('users.urls')),
    # 商品模块接口
    path('api/goods/', include('goods.urls')),
    # 购物车模块接口
    path('api/cart/', include('cart.urls')),
    # 订单模块接口
    path('api/order/', include('order.urls')),
]
