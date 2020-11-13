from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class PaymentHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    income_expense = models.DecimalField(max_digits=5, decimal_places=2)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"{customer.name} {time} - {income_expense}"

class Tariff(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    speed = models.IntegerField()
    limit = models.BigIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    address = models.CharField(max_length=50)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    static_ip = models.BooleanField()
    limit = models.BigIntegerField()

    def __str__(self):
        return self.address