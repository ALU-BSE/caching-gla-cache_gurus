from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('stats/', views.user_stats, name='user_stats'),
]