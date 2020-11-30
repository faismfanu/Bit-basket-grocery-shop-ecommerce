from django.urls import path
from . import views
from gguser import settings

urlpatterns = [
    path('',views.login_sample,name = 'login_sample'),
    path('dealer_dashboard',views.dealer_dashboard,name = 'dealer_dashboard'),
    path('dealer_products',views.dealer_products,name = 'dealer_products'),
    path('dealer_orders',views.dealer_orders,name = 'dealer_orders'),
    path('dealer_orderhistory',views.dealer_orderhistory,name = 'dealer_orderhistory'),
    path('update_order/',views.update_order,name='update_order'),
    path('add_products',views.add_products,name = 'add_products'),
    path('delete_product/<int:id>',views.delete_product,name = 'delete_product'),
    path('dealerlogout',views.dealerlogout,name = 'dealerlogout'),

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ sample checking $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    path('dashboard_sample',views.dashboard_sample,name = 'dashboard_sample'),
    path('order_sample',views.order_sample,name = 'order_sample'),
    path('product_sample',views.product_sample,name = 'product_sample'),
    path('add_product_sample',views.add_product_sample,name = 'add_product_sample'),
    path('edit_product_sample/<int:id>',views.edit_product_sample,name = 'edit_product_sample'),
    path('add_offer',views.add_offer,name = 'add_offer'),
    path('edit_offer/<int:id>',views.edit_offer,name = 'edit_offer'),
    path('offers',views.offers,name = 'offers'),
    path('delete_offer/<int:id>',views.delete_offer,name = 'delete_offer'),
    path('delete_offer_cat/<int:id>',views.delete_offer_cat,name = 'delete_offer_cat'),
    path('order_history_sample',views.order_history_sample,name = 'order_history_sample'),

    
]