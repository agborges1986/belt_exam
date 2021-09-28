from django.urls import path
from . import views

urlpatterns = [
    path('',views.reg_log,name='reg_log'),
    path('inicio', views.inicio),
    path('registro', views.registro),
    path('logout', views.logout,name='logout'),
    #path('registrar', views.registrar),
    #path('main',views.login,name='login'),
    path('travels',views.home,name='home'),
    path('join_trip/<int:id>',views.join_trip,name='join_trip'),
    path('travels/destination/<int:id>',views.destination_id,name='destination_id'),
    path('travels/add',views.destination_add,name='destination_add'),
    path('succes_add',views.succes_add,name='succes_add'),
]
