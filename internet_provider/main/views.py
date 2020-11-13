from django.http.response import HttpResponse, HttpResponseRedirect
from .models import Customer, Tariff
from .forms import CreateTariffForm, DeactivateTariffForm, LoginForm
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
    customers = Customer.objects.all()
    tariffs = Tariff.objects.all()

    try:
        selected_customer = Customer.objects.get(
            id=request.GET.get('customer', '1'))
    except Customer.DoesNotExist:
        selected_customer = None

    if request.user.groups.filter(name='Worker').exists():
        return render(request, 'main/dashboard_worker.html', {
            'selected_customer': selected_customer, 'customers': customers, 'tariffs': tariffs,
            'create_tariff_form': CreateTariffForm(), 'deactivate_tariff_form': DeactivateTariffForm()})
    else:
        return render(request, 'main/dashboard_customer.html', {})


@login_required
def create_customer(request):
    if request.user.groups.filter(name='Worker').exists():
        return HttpResponse(status=204)
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
        return HttpResponse(status=204)
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
            id=form.cleaned_data['tariff'].get().id).update(active=False)
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponse(status=403)
