from rest_framework import permissions


class CollectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 登录的账号是否是管理员
        if request.user.is_superuser:
            return True
        # 如果不是管理,则判断操作对象和登录对象是不是一个用户
        return obj.user == request.user
