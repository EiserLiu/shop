from rest_framework import serializers

from order.models import Order
from users.models import User, Addr


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
