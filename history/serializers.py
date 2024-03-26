from rest_framework import serializers

from .models import History


class HistorySerializers(serializers.ModelSerializer):
    """历史记录模型序列化器"""

    class Meta:
        model = History
        fields = '__all__'
