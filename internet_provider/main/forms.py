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
    description = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Tariff
        fields = ['name', 'price', 'speed', 'limit', 'description']


class CreateCustomerForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone']


class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['customer', 'address', 'tariff', 'static_ip']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tariff'].queryset = Tariff.objects.filter(active=True)


class DeactivateTariffForm(forms.Form):
    tariff = forms.ModelChoiceField(
        queryset=Tariff.objects.filter(active=True))


class TopUpBalanceForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2)


class SwitchTariffForm(forms.Form):
    new_tariff = forms.ModelChoiceField(queryset=Tariff.objects.filter(active=True))