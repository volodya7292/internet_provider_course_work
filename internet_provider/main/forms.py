from .models import Tariff
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

class DeactivateTariffForm(forms.Form):
    tariff = forms.ModelMultipleChoiceField(queryset=Tariff.objects.all())