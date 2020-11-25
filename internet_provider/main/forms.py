from .models import Customer, Service, Tariff
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    username = forms.CharField(label='Логiн')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CreateTariffForm(forms.ModelForm):
    description = forms.CharField(label='Опис', required=False, widget=forms.Textarea)

    class Meta:
        model = Tariff
        fields = ['name', 'price', 'speed', 'limit', 'description']
        labels = {'name': 'Назва', 'price': 'Цiна', 'speed': 'Швидкicть', 'limit': 'Лiмiт', 'description': 'Опис'}


class CreateCustomerForm(forms.ModelForm):
    username = forms.CharField(label='Iм\'я користувача')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone']
        labels = {'name': 'Iм\'я', 'address': 'Адреса', 'phone': 'Телефон'}


class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['customer', 'address', 'tariff', 'static_ip']
        labels = {'customer': 'Користувач', 'address': 'Адреса', 'tariff': 'Тариф', 'static_ip': 'Статичний IP'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tariff'].queryset = Tariff.objects.filter(active=True)


class DeactivateTariffForm(forms.Form):
    tariff = forms.ModelChoiceField(label='Тариф',
        queryset=Tariff.objects.filter(active=True))


class TopUpBalanceForm(forms.Form):
    amount = forms.DecimalField(label='Сума', decimal_places=2, min_value=1)


class SwitchTariffForm(forms.Form):
    new_tariff = forms.ModelChoiceField(label='Новий тариф', queryset=Tariff.objects.filter(active=True))