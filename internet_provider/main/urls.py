from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('create_customer', views.create_customer),
    path('create_tariff', views.create_tariff),
    path('create_service', views.create_service),
    path('create_payment', views.create_payment),
    path('deactivate_tariff', views.deactivate_tariff),
]
