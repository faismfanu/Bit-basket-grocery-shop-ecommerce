from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name = 'index'),
    path('login',views.login,name = 'login'),
    path('signup',views.signup,name = 'signup'),
    path('user_products/<int:id>',views.user_products,name = 'user_products'),
    path('product_catogery/<int:id>/<int:cat_id>',views.product_catogery,name = 'product_catogery'),
    path('product_view/<int:id>',views.product_view,name = 'product_view'),
    path('update_item/',views.updateItem,name = 'update_item'),
    path('cod/',views.cod,name = 'cod'),
    path('process_order/',views.processOrder,name = 'process_order'),
    path('order_completed/',views.order_completed,name = 'order_completed'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('dashboard_orders/',views.dashboard_orders,name = 'dashboard_orders'),
    path('checkout/',views.checkout,name = 'checkout`'),
    path('payment/', views.payment),
    path('response/', views.response),
    path('logoutview',views.logoutview,name = 'logoutview'),
]