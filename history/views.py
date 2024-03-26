from django.shortcuts import render
from rest_framework.viewsets import mixins, GenericViewSet

from .models import History
from .serializers import HistorySerializers


class AddHistory(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = HistorySerializers
    queryset = History.objects.all()
