from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard.html'),
    path('log/<str:d>/', views.log, name='log.html'),
    path('lattest_data/', views.lattest_data),
    path('log_data/<str:d>/', views.log_data),
]
