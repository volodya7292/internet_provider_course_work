from .models import Customer, PaymentHistory, Service, Tariff
from django.contrib import admin

# Register your models here.
admin.site.register(Customer)
admin.site.register(PaymentHistory)
admin.site.register(Tariff)
admin.site.register(Service)