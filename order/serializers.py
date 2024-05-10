from rest_framework import serializers

from order.models import Order
from shop.enums import OrderStatus


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_status(self, value):
        if value not in [status.value for status in OrderStatus]:
            raise serializers.ValidationError("Invalid order status")
        return value
