from rest_framework import serializers

from users.models import User, Addr


class UserSerializer(serializers.ModelSerializer):
    """用户模型序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'avatar', 'last_name']


class AddrSerializers(serializers.ModelSerializer):
    """收货地址模型序列化器"""

    class Meta:
        model = Addr
        fields = '__all__'
