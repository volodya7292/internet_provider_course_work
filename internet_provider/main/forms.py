from .models import Customer, Service, Tariff
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateTariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'price', 'speed', 'limit']


class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone', 'email', 'balance']


class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['customer', 'address', 'tariff', 'static_ip', 'traffic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tariff'].queryset = Tariff.objects.filter(active=True)

class DeactivateTariffForm(forms.Form):
    tariff = forms.ModelChoiceField(queryset=Tariff.objects.filter(active=True))