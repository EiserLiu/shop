from django.urls import path

from . import views

# 购物车模块的路由配置
urlpatterns = [
    # 添加商品到购物车与查看购物车商品列表
    path('goods/', views.CartView.as_view({
        'post': 'create',
        'get': 'list'
    })),
    # 修改购物车商品状态
    path('goods/<int:pk>/checked/', views.CartView.as_view({
        'put': 'update_goods_status'
    })),
    # 修改购物车商品的数量
    path('goods/<int:pk>/', views.CartView.as_view({
        'put': 'update_goods_number'
    }))
]
