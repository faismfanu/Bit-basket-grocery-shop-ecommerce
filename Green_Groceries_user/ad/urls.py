from django.urls import path
from . import views
from gguser import settings


urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),

    path('adminpanel',views.adminpanel,name = 'adminpanel'),
    path('dealers',views.dealers,name = 'dealers'),
    path('base',views.base,name = 'base'),
    path('adddealer',views.adddealer,name = 'adddealer'),
    path('admin_catogeries',views.admin_catogeries,name = 'admin_catogeries'),
    path('delete_catogery/<int:id>',views.delete_catogery,name = 'delete_catogery'),

    path('add_catogeries',views.add_catogeries,name = 'add_catogeries'),
    path('addorder',views.addorder,name = 'addorder'),
    path('edit_dealer/<int:id>/<int:user_id>',views.edit_dealer,name = 'edit_dealer'),
    path('delete_dealer/<int:id>/<int:user_id>',views.delete_dealer,name = 'delete_dealer'),
    path('adminlogout',views.adminlogout,name = 'adminlogout'),


]