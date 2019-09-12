from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'housemanage'
urlpatterns = [
    path('addhouse/', views.addhouse, name='addhouse'),
    path('showhouse/<int:id>/', views.showhouse),
    path('deletehouse/', views.deletehouse, name='deletehouse'),
    path('changehouse/', views.changehouse, name='changehouse'),
    path('/', views.index, name='home'),
    path('', views.index),
]
