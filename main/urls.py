from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('tariffs', views.tariffs),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('get_customers', views.get_customers),
    path('get_customer', views.get_customer),
    path('get_customer_services', views.get_customer_services),
    path('get_service', views.get_service),
    path('create_customer', views.create_customer),
    path('create_tariff', views.create_tariff),
    path('create_service', views.create_service),
    path('create_payment', views.create_payment),
    path('deactivate_tariff', views.deactivate_tariff),
    path('top_up_balance', views.top_up_balance),
    path('pay_for_tariff', views.pay_for_tariff),
    path('switch_tariff', views.switch_tariff),
    path('get_payment_history', views.get_payment_history),
]
