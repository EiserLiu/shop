from rest_framework import permissions


class CollectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 判断操作对象和登录对象是不是一个用户
        return obj.user == request.user
