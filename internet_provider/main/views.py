from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Customer, Service, Tariff
from .forms import CreateCustomerForm, CreateServiceForm, CreateTariffForm, DeactivateTariffForm, LoginForm
from django.core import serializers
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


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


@login_required
def dashboard(request):
    if request.user.groups.filter(name='Worker').exists():
        return render(request, 'main/dashboard_worker.html', {
            'create_tariff_form': CreateTariffForm(auto_id=False), 'create_customer_form': CreateCustomerForm(auto_id=False),
            'create_service_form': CreateServiceForm(auto_id=False), 'deactivate_tariff_form': DeactivateTariffForm(auto_id=False)})
    else:
        return render(request, 'main/dashboard_customer.html', {})


@login_required
def get_customers(request):
    if request.user.groups.filter(name='Worker').exists():
        if request.is_ajax and request.method == 'GET':
            customers = Customer.objects.all()
            return JsonResponse(serializers.serialize("json", customers), safe=False, status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=403)


@login_required
def get_customer(request):
    if request.user.groups.filter(name='Worker').exists():
        if request.is_ajax and request.method == 'GET':
            try:
                customer = Customer.objects.values(
                    'id', 'name', 'address', 'phone', 'email', 'balance').get(id=request.GET.get('id', None))
                return JsonResponse(customer, safe=False, status=200)
            except Customer.DoesNotExist:
                return JsonResponse(status=400)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=403)


@login_required
def get_customer_services(request):
    if request.user.groups.filter(name='Worker').exists():
        if request.is_ajax and request.method == 'GET':
            services = Service.objects.prefetch_related('tariff').filter(
                customer_id=request.GET.get('customer_id', None)).only(*Service.get_fields())
            return JsonResponse(serializers.serialize("json", services, use_natural_foreign_keys=True), safe=False, status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=403)


@ login_required
def create_customer(request):
    if request.user.groups.filter(name='Worker').exists():
        form = CreateCustomerForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=400)
        form.save()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@ login_required
def create_tariff(request):
    if request.user.groups.filter(name='Worker').exists():
        form = CreateTariffForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=400)
        form.save()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@ login_required
def create_service(request):
    if request.user.groups.filter(name='Worker').exists():
        form = CreateServiceForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=400)
        form.save()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)


@ login_required
def create_payment(request):
    if request.user.groups.filter(name='Worker').exists():
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=403)


@ login_required
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
