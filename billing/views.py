# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains, CURRENCIES, DomainCheckForm, DomainTransferForm, NICform, NIC, Contracts, COUNTRIES
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
from django.contrib.auth import logout
from django.core.mail import mail_admins
from sys import stderr
from dynhost import settings
from ovh import soapi
from billing import delivery_note, invoice as billing_invoice
from django.template import Context
from django.http import HttpResponse

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
    if cuenta.nic_data == None:
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
                domain.contract_id = contract.id
                domain.save()
                return redirect(reverse('billing.views.payment', args=(contract.id,)))
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
        'currency': currency,
        'ccc': settings.CCC,
        'bank': settings.BANK
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def transfer(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    if cuenta.nic_data == None:
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
                domain.contract_id = contract.id
                domain.save()
                return redirect(reverse('billing.views.payment', args=(contract.id,)))
    else:
        form = DomainTransferForm()
    return render_to_response('billing_transfer_domain.html', {
        'cuenta': cuenta,
        'form': form
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def revoke(request, contract_id):
    try:
        contract = Contracts.objects.get(pk=contract_id)
    except Contracts.DoesNotExist:
        return redirect(reverse('billing.views.index'))
    if contract.type == 'D':
        return redirect(reverse('billing.views.index'))
    cuenta = Accounts.objects.get(user = request.user.id)
    if contract.accounts_id != cuenta.id:
        return redirect(reverse('billing.views.index'))
    if contract.paid:
        if contract.type == 'M':
            usados = Mailbox.objects.filter(domain__accounts__id = cuenta.id).count()
            if usados >= cuenta.limit_email_mailbox:
                return redirect(reverse('billing.views.index'))
            cuenta.limit_email_mailbox -= settings.PREMIUM_MAIL_QTY
            cuenta.save()
        elif contract.type == 'm':
            usados = Mailbox.objects.filter(domain__accounts__id = cuenta.id).count()
            if usados >= cuenta.limit_email_mailbox:
                return redirect(reverse('billing.views.index'))
            cuenta.limit_email_mailbox -= settings.PLUS_MAIL_QTY
            cuenta.save()
        elif contract.type == 'R':
            usados = Redirect.objects.filter(domain__accounts__id = cuenta.id).count()
            if usados >= cuenta.limit_email_redirect:
                return redirect(reverse('billing.views.index'))
            cuenta.limit_email_redirect -= settings.REDIRECT_MAIL_QTY
            cuenta.save()
        elif contract.type == 'B':
            usados = Databases.objects.filter(accounts__id = cuenta.id).count()
            if usados >= cuenta.limit_sql:
                return redirect(reverse('billing.views.index'))
            cuenta.limit_sql -= 1
            cuenta.save()
    contract.delete()
    return redirect(reverse('billing.views.index') + '?contract')

@login_required(login_url='/')
def mail_plus_purchase(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    if cuenta.nic_data == None:
        return redirect(reverse('billing.views.index') + '?client')
    contract = Contracts()
    contract.type = 'm'
    contract.quantity = settings.PLUS_MAIL_QTY
    contract.price = settings.PLUS_MAIL_PRICE
    contract.accounts_id = cuenta.id
    contract.concept = ""
    contract.save()
    return redirect(reverse('billing.views.payment', args=[contract.id]))

@login_required(login_url='/')
def mail_premium_purchase(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    if cuenta.nic_data == None:
        return redirect(reverse('billing.views.index') + '?client')
    contract = Contracts()
    contract.type = 'M'
    contract.quantity = settings.PREMIUM_MAIL_QTY
    contract.price = settings.PREMIUM_MAIL_PRICE
    contract.accounts_id = cuenta.id
    contract.concept = ""
    contract.save()
    return redirect(reverse('billing.views.payment', args=[contract.id]))

@login_required(login_url='/')
def mail_redirect_purchase(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    if cuenta.nic_data == None:
        return redirect(reverse('billing.views.index') + '?client')
    contract = Contracts()
    contract.type = 'R'
    contract.quantity = settings.REDIRECT_MAIL_QTY
    contract.price = settings.REDIRECT_MAIL_PRICE
    contract.accounts_id = cuenta.id
    contract.concept = ""
    contract.save()
    return redirect(reverse('billing.views.payment', args=[contract.id]))

@login_required(login_url='/')
def mysql_purchase(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    if cuenta.nic_data == None:
        return redirect(reverse('billing.views.index') + '?client')
    contract = Contracts()
    contract.type = 'B'
    contract.price = settings.MYSQL_DB_PRICE
    contract.accounts_id = cuenta.id
    contract.concept = ""
    contract.save()
    return redirect(reverse('billing.views.payment', args=[contract.id]))

@login_required(login_url='/')
def deregister(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    cuenta.user.is_active = False
    cuenta.user.save()
    mail_admins(
        '[DynHOST] Usuario dado de baja', 
        'El usuario ' + cuenta.user.username + ' con email ' + cuenta.user.email + ' ha causado baja.',
        fail_silently=(not settings.DEBUG))
    return logout(request)

@login_required(login_url='/')
def invoice(request, contract_id, type):
    cuenta = Accounts.objects.get(user = request.user.id)
    contract = Contracts.objects.get(pk=contract_id)
    data = {
        'company_name': settings.COMPANY_NAME,
        'company_id': settings.COMPANY_ID,
        'company_addr': settings.COMPANY_ADDR,
        'company_zip': settings.COMPANY_ZIP,
        'company_city': settings.COMPANY_CITY,
        'company_state': settings.COMPANY_STATE,
        'company_country': settings.COMPANY_COUNTRY,
        'company_phone': settings.COMPANY_PHONE,
        'company_web': settings.COMPANY_WEB,
        'company_email': settings.COMPANY_EMAIL,

        'nic_data': cuenta.nic_data,
        'cuenta': cuenta,
        'contract': contract
    }
    response = HttpResponse(content_type='application/pdf')
    if contract.invoice_id:
        #response['Content-Disposition'] = 'attachment; filename="factura_%05d.pdf"' % contract.invoice_id
        response['Content-Disposition'] = 'inline; filename="factura_%05d.pdf"' % contract.invoice_id
        billing_invoice.draw_pdf(response, data)
    else:
        #response['Content-Disposition'] = 'attachment; filename="albaran_%s.pdf"' % contract.begins.strftime('%Y%m%d')
        response['Content-Disposition'] = 'inline; filename="albaran_%s.pdf"' % contract.begins.strftime('%Y%m%d')
        delivery_note.draw_pdf(response, data)
    return response
