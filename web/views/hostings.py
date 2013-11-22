# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains
from dns.models import Records
from ..models import Hosting, HostingForm
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Q
import sys

def check_owner(dom_id, acc_id):
    try:
        cuenta = Domains.objects.get(pk=dom_id).accounts
        if cuenta.id != acc_id:
            return False
    except Domains.DoesNotExist:
        return False
    return True

def getForm(cuenta, dom_id, post, hosting):
    if not post:
        form = HostingForm(instance=hosting, auto_id=False)
    else:
        form = HostingForm(post, instance=hosting, auto_id=False)
    print >>sys.stderr, hosting
    form.fields['directory'].choices = tuple([ (x,x) for x in cuenta.dirs() ])
    form.fields['record'].queryset = Records.objects.filter(
        Q(domain__id=dom_id) & (
            Q(type='A') | Q(type='CNAME')
        )
    )
    return form


@login_required(login_url='/')
def index(request, dom_id, page=None):
    cuenta = Accounts.objects.get(user = request.user.id)
    if not check_owner(dom_id, cuenta.id):
        return redirect(reverse('dns.views.domains.index'))
    servicios = Hosting.objects.filter(record__domain__id=dom_id).filter(type='H')
    usados = Hosting.objects.filter(record__domain__accounts__id=cuenta.id).filter(type='H').count()
    return render_to_response('web_hosting_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_web - usados,
        'total': cuenta.limit_web,
        'dom_id': dom_id,
        'dom': Domains.objects.get(pk=dom_id).domain,
        'tipo': 'Alojamientos Web'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request, dom_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    if not check_owner(dom_id, cuenta.id):
        return redirect(reverse('dns.views.domains.index'))
    usados = Hosting.objects.filter(record__domain__accounts__id=cuenta.id).filter(type='H').count()
    hosting = Hosting()
    hosting.type = 'H'
    if request.method == 'POST':
        form = getForm(cuenta, dom_id, request.POST, hosting)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('web.views.hostings.index', args=[dom_id]))
            except IntegrityError:
                form._errors['name'] = ["El nombre o la URI ya existen para este Registro DNS."]
    else:
        form = getForm(cuenta, dom_id, request.POST, hosting)
    return render_to_response('web_hosting_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_web - usados,
        'total': cuenta.limit_web,
        'dom_id': dom_id,
        'dom': Domains.objects.get(pk=dom_id).domain,
        'tipo': 'Alojamientos Web',
        'nuevo': True,
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, hosting_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        hosting = Hosting.objects.get(pk=hosting_id)
        if hosting.record.domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        dom_id = hosting.record.domain.id
        usados = Hosting.objects.filter(record__domain__accounts__id=cuenta.id).filter(type='H').count()
        if request.method == 'POST':
            form = getForm(cuenta, dom_id, request.POST, hosting)
            if form.is_valid():
                try:
                    form.save()
                    return redirect(reverse('web.views.hostings.index', args=[dom_id]))
                except IntegrityError:
                    form._errors['name'] = ["El alojamiento ya existe."]
                    del form.cleaned_data['name']
        else:
            form = getForm(cuenta, dom_id, request.POST, hosting)
        return render_to_response('web_hosting_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_web - usados,
            'total': cuenta.limit_web,
            'dom_id': dom_id,
            'dom': hosting.record.domain.domain,
            'tipo': 'Alojamientos Web'
        }, context_instance=RequestContext(request))
    except Hosting.DoesNotExist:
        return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def delete(request, hosting_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        hosting = Hosting.objects.get(pk=hosting_id)
        if hosting.record.domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        hosting.delete()
        return redirect(reverse('web.views.hostings.index', args=[hosting.record.domain_id]))
    except Hosting.DoesNotExist:
        pass
    return redirect(reverse('dns.views.domains.index'))
