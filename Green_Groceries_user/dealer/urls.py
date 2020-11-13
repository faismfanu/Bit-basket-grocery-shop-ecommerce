from django.urls import path
from . import views
from gguser import settings

urlpatterns = [
    path('',views.dealerlogin,name = 'dealerlogin'),
    path('dealer_dashboard',views.dealer_dashboard,name = 'dealer_dashboard'),
    path('dealer_products',views.dealer_products,name = 'dealer_products'),
    path('dealer_orders',views.dealer_orders,name = 'dealer_orders'),
    path('dealer_orderhistory',views.dealer_orderhistory,name = 'dealer_orderhistory'),
    
    path('add_products',views.add_products,name = 'add_products'),
    path('delete_product/<int:id>',views.delete_product,name = 'delete_product'),
    path('dealerlogout',views.dealerlogout,name = 'dealerlogout'),
    
]