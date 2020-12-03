from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name = 'index'),
    path('login',views.login,name = 'login'),
    path('signup',views.signup,name = 'signup'),
    path('reffral_signup/<str:reff_code>',views.reffral_signup,name = 'reffral_signup'),
    path('user_products/<int:id>',views.user_products,name = 'user_products'),
    path('product_catogery/<int:id>/<int:cat_id>',views.product_catogery,name = 'product_catogery'),
    path('product_view/<int:id>',views.product_view,name = 'product_view'),
    path('update_item/',views.updateItem,name = 'update_item'),
    path('cod/',views.cod,name = 'cod'),
    path('process_order/',views.processOrder,name = 'process_order'),
    path('order_completed/',views.order_completed,name = 'order_completed'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('dashboard_orders/',views.dashboard_orders,name = 'dashboard_orders'),
    path('dashboard_address/',views.dashboard_address,name = 'dashboard_address'),
    path('dashboard_add_address/',views.dashboard_add_address,name = 'dashboard_add_address'),
    path('dashboard_my_profile/',views.dashboard_my_profile,name = 'dashboard_my_profile'),
     path('dashboard_edit_profile/',views.dashboard_edit_profile,name = 'dashboard_edit_profile'),
    path('dashboard_address_delete/<int:id>',views.dashboard_address_delete,name = 'dashboard_address_delete'),
    path('checkout/',views.checkout,name = 'checkout`'),
    path('getshipping/',views.Getshipping.as_view()),
    path('payment/', views.payment),
    path('response/', views.response),
    path('logoutview',views.logoutview,name = 'logoutview'),
]