from django.contrib import admin
from django.urls import path, include, re_path
# 获取文件的视图
from users.views import FileView

urlpatterns = [
    path("admin/", admin.site.urls),
    # 获取图片资源接口
    re_path(r'file/image/(.+?)/', FileView.as_view()),
    # 用户模块接口
    path('api/user/', include('users.urls')),
    # 商品模块接口
    path('api/goods/', include('goods.urls')),
    # 购物车模块接口
    path('api/cart/', include('cart.urls'))

]
