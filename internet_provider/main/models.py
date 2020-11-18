from django.db import models


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    balance = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class PaymentHistory(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    income_expense = models.DecimalField(max_digits=5, decimal_places=2)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.customer.name} {self.time} - {self.income_expense}"


class Tariff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    speed = models.IntegerField()
    limit = models.BigIntegerField()
    description = models.CharField(max_length=100, default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return {
            'name': self.name,
            'price': self.price,
            'speed': self.speed,
            'limit': self.limit,
            'description': self.description,
            'active': self.active
        }


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer,  on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    static_ip = models.BooleanField(default=False)
    traffic = models.BigIntegerField(default=0)

    def __str__(self):
        return self.address

    def get_fields():
        return ['address', 'tariff', 'static_ip', 'traffic']
