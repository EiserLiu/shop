from django.contrib import admin
from django.urls import path, include, re_path
# 获取文件的视图
from users.views import FileView

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r'file/image/(.+?)/',FileView.as_view()),
    path('api/user/', include('users.urls')),

]
