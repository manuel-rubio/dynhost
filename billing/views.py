# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains, CURRENCIES, DomainCheckForm, NICform, NIC, NICformUpdate
from mail.models import Redirect, RedirectDynHost, Mailbox
from web.models import RedirectDynHost as RedirectWebDynHost, Hosting
from database.models import Databases, Users as DBUsers
from dynamic.models import Domains as Dynamic
from ftp.models import Users as FTPUsers
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.db import IntegrityError
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
    if not cuenta.nic_data:
        nic = NIC()
        if request.method == 'POST' and request.POST['form'] == 'nic':
            nic_form = NICform(request.POST, instance=nic)
        else:
            nic_form = NICform(instance=nic)
    else:
        nic = cuenta.nic_data
        if request.method == 'POST' and request.POST['form'] == 'nic':
            nic_form = NICformUpdate(request.POST, instance=nic)
        else:
            nic_form = NICformUpdate(instance=nic)
    nic_focus = False
    if request.method == 'POST':
        if request.POST['form'] == 'password':
            form = PasswordChangeForm(request.user, data=request.POST)
            if form.is_valid():
                form.save()
                mensaje = 'Clave cambiada con éxito.'
        elif request.POST['form'] == 'nic':
            if nic_form.is_valid():
                nic_form.save()
                if not nic.nic:
                    nic.nic = soapi.nic_create(
                        nic.name, nic.firstname, settings.OVH_USERS_PASS, nic.email,
                        nic.phone, '', nic.address, nic.city, nic.area,
                        nic.zipCode, nic.country, nic.language, nic.legalForm,
                        nic.organization, nic.legalName, nic.legalNumber, settings.IVA)
                    nic.save()
                else:
                    print >>stderr, soapi.nic_update(
                        nic.nic, nic.name, nic.firstname, nic.email, nic.legalForm,
                        nic.legalName, nic.legalNumber, nic.organization, settings.IVA)

                cuenta.nic_data_id = nic.id
                cuenta.save()
                mensaje = 'NIC actualizado con éxito.'
            else:
                print >>stderr, nic_form._errors
                nic_focus = True
    for (k,val) in CURRENCIES:
        if k == cuenta.currency:
            currency = val 
            break
    else:
        currency = '&euro;'
    if 'client' in request.GET:
        nic_focus = True
    return render_to_response('billing_home.html', {
        'cuenta': cuenta,
        'nic_form': nic_form,
        'nic_new': False if cuenta.nic_data else True,
        'nic_focus': nic_focus,
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
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('billing.views.payment', domain.id))
            except IntegrityError:
                form._errors['domain'] = ['El dominio ya existe como zona.']
    else:
        form = DomainCheckForm()
    return render_to_response('billing_purchase_domain.html', {
        'cuenta': cuenta,
        'form': form
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def payment(request, dom_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        domain = Domains.objects.get(pk = dom_id)
        if domain.accounts_id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
    except Domains.DoesNotExist:
        return redirect(reverse('dns.views.domains.index'))
    return render_to_response('billing_payment_domain.html', {
        'cuenta': cuenta,
        'domain': domain
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def transfer(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    return render_to_response('billing_buy_domain.html', {
        'cuenta': cuenta,

    }, context_instance=RequestContext(request))
