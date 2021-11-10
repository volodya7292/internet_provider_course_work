from django.contrib.auth.models import User, Group
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Customer, PaymentHistory, Service, Tariff
from .forms import CreateCustomerForm, CreateServiceForm, CreateTariffForm, DeactivateTariffForm, LoginForm, SwitchTariffForm, TopUpBalanceForm
from django.core import serializers
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
import decimal


def index(request):
    return render(request, 'main/index.html')


def tariffs(request):
    tariffs = Tariff.objects.filter(active=True)
    return render(request, 'main/tariffs.html', {'tariffs': tariffs})


def login(request):
    if request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None or not user.is_active:
            return render(request, 'main/login.html', {"form": LoginForm()})

        auth_login(request, user)
        return redirect(request.GET.get('next', '/dashboard'))
    else:
        return render(request, 'main/login.html', {'form': LoginForm()})


def logout(request):
    auth_logout(request)
    return redirect('/')


@login_required
def dashboard(request):
    if request.user.groups.filter(name='Worker').exists():
        return render(request, 'main/dashboard_worker.html', {
            'create_tariff_form': CreateTariffForm(auto_id=False), 'create_customer_form': CreateCustomerForm(auto_id=False),
            'create_service_form': CreateServiceForm(auto_id=False), 'deactivate_tariff_form': DeactivateTariffForm(auto_id=False)})
    else:
        customer = Customer.objects.get(user=request.user)
        services = Service.objects.filter(customer=customer)
        top_up_balance_form = TopUpBalanceForm()
        switch_tariff_form = SwitchTariffForm()
        return render(request, 'main/dashboard_customer.html',
                      {'customer': customer, 'services': services,
                       'top_up_balance_form': top_up_balance_form, 'switch_tariff_form': switch_tariff_form})


@login_required
def get_customers(request):
    if request.user.groups.filter(name='Worker').exists():
        if request.is_ajax and request.method == 'GET':
            customers = Customer.objects.prefetch_related('user').all()
            return JsonResponse(serializers.serialize("json", customers, use_natural_foreign_keys=True), safe=False, status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=403)


@login_required
def get_customer(request):
    if request.user.groups.filter(name='Worker').exists():
        if request.is_ajax and request.method == 'GET':
            # try:
            #     customer = Customer.objects.values(
            #         'id', 'name', 'address', 'phone', 'balance').get(id=request.GET.get('id', None))
            #     return JsonResponse(customer, safe=False, status=200)
            # except Customer.DoesNotExist:
            return JsonResponse(status=400)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=403)


@login_required
def get_customer_services(request):
    if request.user.groups.filter(name='Worker').exists():
        if request.is_ajax and request.method == 'GET':
            services = Service.objects.prefetch_related('customer', 'tariff').filter(
                customer_id=request.GET.get('customer_id', 0)).only(*Service.get_fields())
            return JsonResponse(serializers.serialize("json", services, use_natural_foreign_keys=True), safe=False, status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=403)


@login_required
def get_service(request):
    if request.user.groups.filter(name='Customer').exists():
        if request.is_ajax and request.method == 'GET':
            customer = Customer.objects.get(user=request.user)
            service = Service.objects.get(id=request.GET.get(
                'service_id', 0), customer=customer)
            return JsonResponse(serializers.serialize("json", [service, ], use_natural_foreign_keys=True), safe=False, status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=403)


@login_required
def create_customer(request):
    if request.user.groups.filter(name='Worker').exists():
        form = CreateCustomerForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=400)
        user = User.objects.create_user(
            username=form.cleaned_data['username'], password=form.cleaned_data['password'])

        Customer.objects.create(
            name=form.cleaned_data['name'], address=form.cleaned_data['address'], phone=form.cleaned_data['phone'], user=user)
        Group.objects.get(name='Customer').user_set.add(user)

        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@login_required
def create_tariff(request):
    if request.user.groups.filter(name='Worker').exists():
        form = CreateTariffForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=400)
        form.save()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@login_required
def create_service(request):
    if request.user.groups.filter(name='Worker').exists():
        form = CreateServiceForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=400)
        form.save()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@login_required
def create_payment(request):
    if request.user.groups.filter(name='Worker').exists():
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=403)


@login_required
def deactivate_tariff(request):
    if request.user.groups.filter(name='Worker').exists():
        form = DeactivateTariffForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=400)
        Tariff.objects.filter(
            id=form.cleaned_data['tariff'].id).update(active=False)
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@login_required
def top_up_balance(request):
    if request.user.groups.filter(name='Customer').exists():
        try:
            customer = Customer.objects.get(user=request.user)
            amount_decimal = decimal.Decimal(request.POST.get('amount', 0))
            customer.balance += amount_decimal
            customer.save()
            PaymentHistory.objects.create(
                customer=customer, income_expense=amount_decimal, balance=customer.balance, comment="Поповнення рахунку.")
        except Service.DoesNotExist:
            return HttpResponse(status=400)
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@login_required
def pay_for_tariff(request):
    if request.user.groups.filter(name='Customer').exists():
        try:
            customer = Customer.objects.get(user=request.user)
            price = Service.objects.get(
                id=request.POST.get('service_id', 0)).tariff.price
            if customer.balance < price:
                return JsonResponse(status=400)
            customer.balance -= price
            customer.save()
            PaymentHistory.objects.create(
                customer=customer, income_expense=-price, balance=customer.balance, comment="Списання за послуги тарифу.")
        except Service.DoesNotExist:
            pass
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@ login_required
def switch_tariff(request):
    if request.user.groups.filter(name='Customer').exists():
        try:
            form = SwitchTariffForm(request.POST)
            if not form.is_valid():
                return HttpResponse(status=400)
            service = Service.objects.get(
                id=request.POST.get('service_id', 0))
            service.tariff = form.cleaned_data['new_tariff']
            service.save()
        except Service.DoesNotExist:
            return JsonResponse(status=400)
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@ login_required
def get_payment_history(request):
    if request.user.groups.filter(name='Customer').exists():
        if request.is_ajax and request.method == 'GET':
            customer = Customer.objects.get(user=request.user)
            history = PaymentHistory.objects.filter(customer=customer)
            return JsonResponse(serializers.serialize("json", history), safe=False, status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=403)
