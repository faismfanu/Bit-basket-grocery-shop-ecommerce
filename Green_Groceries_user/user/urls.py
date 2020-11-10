from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name = 'index'),
    path('login',views.login,name = 'login'),
    path('signup',views.signup,name = 'signup'),
    path('user_products/<int:id>',views.user_products,name = 'user_products'),
    path('product_view/<int:id>',views.product_view,name = 'product_view'),
    path('update_item/',views.updateItem,name = 'update_item'),
    path('process_order/',views.processOrder,name = 'process_order'),
    path('checkout/',views.checkout,name = 'checkout`'),
    path('logoutview',views.logoutview,name = 'logoutview'),
]