# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains
from ..models import Records, RecordsForm
from django.core.urlresolvers import reverse
import sys

@login_required(login_url='/')
def new(request, dom_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = Domains.objects.filter(accounts = cuenta).count()
    domain = Domains.objects.get(pk=dom_id)
    if not domain:
        return redirect(reverse('dns.views.domains.index'))
    record = Records()
    record.domain_id = domain.id
    if request.method == 'POST':
        form = RecordsForm(request.POST, instance=record, auto_id=False)
        if form.is_valid():
            form.save()
            return redirect(reverse('dns.views.domains.edit', args=[dom_id]))
    else:
        form = RecordsForm(instance=record, auto_id=False)
    return render_to_response('dns_records_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_dns - usados,
        'total': cuenta.limit_dns,
        'dom_id': record.domain.id,
        'dom': record.domain.domain,
        'tipo': 'Zonas'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, rec_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = Domains.objects.filter(accounts = cuenta).count()
    try:
        record = Records.objects.get(pk=rec_id)
        if record.domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        if request.method == 'POST':
            form = RecordsForm(request.POST, instance=record, auto_id=False)
            if form.is_valid():
                form.save()
                return redirect(reverse('dns.views.domains.edit', args=[record.domain.id]))
        else:
            form = RecordsForm(instance=record, auto_id=False)
        return render_to_response('dns_records_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_dns - usados,
            'total': cuenta.limit_dns,
            'dom_id': record.domain.id,
            'dom': record.domain.domain,
            'tipo': 'Zonas'
        }, context_instance=RequestContext(request))
    except Records.DoesNotExist:
        return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def delete(request, rec_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        print >>sys.stderr, rec_id
        registro = Records.objects.get(pk=rec_id)
        if registro.domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        registro.delete()
        return redirect(reverse('dns.views.domains.edit', args=[registro.domain_id]))
    except Records.DoesNotExist:
        pass
    return redirect(reverse('dns.views.domains.index'))
