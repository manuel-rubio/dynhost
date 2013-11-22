# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains, CURRENCIES, DomainCheckForm, DomainTransferForm, NICform, NIC, Contracts
from mail.models import Redirect, RedirectDynHost, Mailbox
from web.models import RedirectDynHost as RedirectWebDynHost, Hosting
from database.models import Databases, Users as DBUsers
from dynamic.models import Domains as Dynamic
from ftp.models import Users as FTPUsers
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.db import IntegrityError, models
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse
from sys import stderr
from dynhost import settings
from ovh import soapi

@login_required(login_url='/')
def index(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    mensaje = None
    form = PasswordChangeForm(request.user)
    nic_data = cuenta.nic_data
    nic = nic_data if nic_data else NIC()
    nic_form = NICform(instance=nic)
    nic_focus = False
    if request.method == 'POST':
        if request.POST['form'] == 'password':
            form = PasswordChangeForm(request.user, data=request.POST)
            if form.is_valid():
                form.save()
                mensaje = 'Clave cambiada con éxito.'
        elif request.POST['form'] == 'nic':
            nic = NIC()
            nic_form = NICform(request.POST, instance=nic)
            if nic_form.is_valid():
                nic_form.save()
                if nic_data:
                    nic_data.removed = True
                    nic_data.save()
                nic.nic = soapi.nic_create(
                    nic.name, nic.firstname, settings.OVH_USERS_PASS, nic.email,
                    nic.phone, '', nic.address, nic.city, nic.area,
                    nic.zipCode, nic.country, nic.language, nic.legalForm,
                    nic.organization, nic.legalName, nic.legalNumber, settings.IVA)
                nic.save()
                cuenta.nic_data_id = nic.id
                cuenta.save()
                mensaje = 'NIC actualizado con éxito.'
            else:
                print >>stderr, nic_form._errors
                nic_focus = True
    currency = '&euro;'
    for (k,val) in CURRENCIES:
        if k == cuenta.currency:
            currency = val 
            break
    return render_to_response('billing_home.html', {
        'cuenta': cuenta,
        'nic_form': nic_form,
        'nic_new': False if cuenta.nic_data else True,
        'nic_focus': 'client' in request.GET,
        'form': form,
        'dominios': Domains.objects.filter(accounts__id = cuenta.id).count(),
        'dynhosts': Dynamic.objects.filter(user_id = request.user.id).count(),
        'redirects': Redirect.objects.filter(domain__accounts__id = cuenta.id).count(),
        'redirects_mail_dynhost': RedirectDynHost.objects.filter(dynamic__user_id = request.user.id).count(),
        'mailboxes': Mailbox.objects.filter(domain__accounts__id = cuenta.id).count(),
        'databases': Databases.objects.filter(accounts__id = cuenta.id).count(),
        'dbusers': DBUsers.objects.filter(accounts__id = cuenta.id).count(),
        'redirects_web': Hosting.objects.filter(record__domain__accounts__id=cuenta.id, type='R').count(),
        'hosting': Hosting.objects.filter(record__domain__accounts__id=cuenta.id, type='H').count(),
        'redirects_web_dynhost': RedirectWebDynHost.objects.filter(dynamic__user_id = request.user.id).count(),
        'ftp': FTPUsers.objects.filter(accounts__id = cuenta.id).count(),
        'mensaje': mensaje,
        'currency': currency,
        'paymonth': Contracts.objects.filter(accounts__id = cuenta.id).aggregate(models.Sum('price')),
        'contracts': Contracts.objects.filter(accounts__id = cuenta.id),
        'contract_focus': 'contract' in request.GET
    }, context_instance=RequestContext(request))

def pricing(request):
    cuenta = None
    form = None
    if request.user.is_authenticated():
        cuenta = Accounts.objects.get(user = request.user.id)
    else:
        form = AuthenticationForm(request.POST)
    return render_to_response('billing_pricing.html', {
        'cuenta': cuenta,
        'form': form,
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def purchase(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    if cuenta.nic_data.nic == '':
        return redirect(reverse('billing.views.index') + '?client')
    if request.method == 'POST':
        # check domain availability
        domain = Domains()
        domain.accounts_id = cuenta.id
        domain.status = 'N'
        domain.expires = date.today() + relativedelta(years=1)
        form = DomainCheckForm(request.POST, instance=domain)
        error = False
        if form.is_valid():
            try:
                form.save()
                soapi.buy_domain(domain.domain, cuenta.nic_data.nic)
            except IntegrityError:
                form._errors['domain'] = ['El dominio ya existe como zona.']
                error = True
            if not error:
                contract = Contracts()
                contract.price = settings.DOMAIN_PRICE
                contract.accounts_id = cuenta.id
                contract.concept = domain.domain
                contract.save()
                return redirect(reverse('billing.views.payment', args=(domain.id,)))
    else:
        form = DomainCheckForm()
    return render_to_response('billing_purchase_domain.html', {
        'cuenta': cuenta,
        'form': form
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def payment(request, contract_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        contract = Contracts.objects.get(pk = contract_id)
        if contract.accounts_id != cuenta.id:
            return redirect(reverse('billing.views.index'))
    except Contracts.DoesNotExist:
        return redirect(reverse('billing.views.index'))

    currency = '&euro;'
    for (k,val) in CURRENCIES:
        if k == cuenta.currency:
            currency = val 
            break
    return render_to_response('billing_payment.html', {
        'cuenta': cuenta,
        'contract': contract,
        'currency': currency
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def transfer(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    if cuenta.nic_data.nic == '':
        return redirect(reverse('billing.views.index') + '?client')
    if request.method == 'POST':
        # check domain availability
        domain = Domains()
        domain.accounts_id = cuenta.id
        domain.status = 'T'
        domain.expires = date.today() + relativedelta(years=1)
        form = DomainTransferForm(request.POST, instance=domain)
        error = False
        if form.is_valid():
            try:
                form.save()
                soapi.buy_domain(domain.domain, cuenta.nic_data.nic)
            except IntegrityError:
                form._errors['domain'] = ['El dominio ya existe como zona.']
                error = True
            if not error:
                contract = Contracts()
                contract.price = settings.DOMAIN_PRICE
                contract.accounts_id = cuenta.id
                contract.concept = domain.domain
                contract.save()
                return redirect(reverse('billing.views.payment', args=(domain.id,)))
    else:
        form = DomainTransferForm()
    return render_to_response('billing_transfer_domain.html', {
        'cuenta': cuenta,
        'form': form
    }, context_instance=RequestContext(request))
