from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/system-info/', views.system_info, name='system_info'),
]

