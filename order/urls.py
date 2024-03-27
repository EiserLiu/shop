from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.OrderView.as_view({
        'post': 'create',
        'get': 'list'
    }))
]
