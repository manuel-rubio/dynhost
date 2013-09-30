# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import *
from dns.models import *
from django.core.urlresolvers import reverse
from datetime import datetime

@login_required(login_url='/')
def index(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    servicios = Domains.objects.filter(accounts = cuenta)
    usados = servicios.count()
    return render_to_response('dns_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_dns - usados,
        'total': cuenta.limit_dns,
        'tipo': 'Zonas'
    }, context_instance=RequestContext(request))
    
def new_soa(domain):
    soa = Records()
    soa.type = 'SOA'
    soa.domain = domain
    soa.serial = datetime.now().strftime('%Y%m%d%H')
    soa.refresh = 10800
    soa.expire = 604800
    soa.retry = 3600
    soa.minimum = 38400
    soa.host = '@'
    soa.data = 'ovh.bosqueviejo.net.'
    soa.email = domain.accounts.user.email
    return soa
    
@login_required(login_url='/')
def new(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = Domains.objects.filter(accounts = cuenta).count()
    if usados >= cuenta.limit_dns:
        return redirect(reverse('dns.views.domains.index'))
    domain = Domains()
    domain.accounts = cuenta
    soa = new_soa(domain) # inicializamos registro SOA
    if request.method == 'POST':
        dom_form = DomainsForm(request.POST, instance=domain, auto_id=False)
        soa_form = SoaRecordForm(request.POST, instance=soa, auto_id=False)
        if dom_form.is_valid() and soa_form.is_valid():
            dom_form.save()
            soa.domain = domain
            soa_form.save()
            return redirect(reverse('dns.views.domains.index'))
    else:
        soa = new_soa(domain)
        dom_form = DomainsForm(instance=domain, auto_id=False)
        soa_form = SoaRecordForm(instance=soa, auto_id=False)
    return render_to_response('dns_domains_edit.html', {
        'cuenta': cuenta,
        'dom_form': dom_form,
        'soa_form': soa_form,
        'usados': usados,
        'disponibles': cuenta.limit_dns - usados,
        'total': cuenta.limit_dns,
        'tipo': 'Zonas',
        'nuevo': True
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, dom_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = Domains.objects.filter(accounts = cuenta).count()
    try:
        domain = Domains.objects.get(pk=dom_id)
        if domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        soa = Records.objects.filter(type='SOA').filter(domain__id=domain.id)
        if request.method == 'POST':
            soa = new_soa(domain) if len(soa) == 0 else soa[0]
            dom_form = DomainsForm(request.POST, instance=domain, auto_id=False)
            soa_form = SoaRecordForm(request.POST, instance=soa, auto_id=False)
            if dom_form.is_valid() and soa_form.is_valid():
                dom_form.save()
                soa.domain = domain
                soa_form.save()
                return redirect(reverse('dns.views.domains.index'))
        else:
            soa = new_soa(domain) if len(soa) == 0 else soa[0]
            dom_form = DomainsForm(instance=domain, auto_id=False)
            soa_form = SoaRecordForm(instance=soa, auto_id=False)
        return render_to_response('dns_domains_edit.html', {
            'cuenta': cuenta,
            'dom_form': dom_form,
            'soa_form': soa_form,
            'usados': usados,
            'disponibles': cuenta.limit_dns - usados,
            'total': cuenta.limit_dns,
            'registros': Records.objects.filter(domain__id=domain.id).exclude(type='SOA').exclude(type='NS'),
            'dom_id': domain.id,
            'tipo': 'Zonas'
        }, context_instance=RequestContext(request))
    except Domains.DoesNotExist:
        return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def delete(request, dom_id):
    try:
        cuenta = Accounts.objects.get(user = request.user.id)
        domain = Domains.objects.get(pk=dom_id)
        registros = Records.objects.filter(domain__id=domain.id)
        if domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        if len(registros)>0:
            for registro in registros:
                registro.delete()
        domain.delete()
    except Domains.DoesNotExist:
        pass
    return redirect(reverse('dns.views.domains.index'))
