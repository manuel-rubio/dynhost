# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from dynamic.models import *
from django.core.urlresolvers import reverse
from billing.models import Accounts

@login_required(login_url='/')
def index(request):
    servicios = Domains.objects.filter(user_id = request.user.id)
    empleados = servicios.count()
    cuenta = Accounts.objects.get(user = request.user.id)
    return render_to_response('dynhost_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'empleados': empleados,
        'disponibles': cuenta.limit_dynhost - empleados,
        'total': cuenta.limit_dynhost,
        'tipo': '<strong>DynHost</strong>'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    empleados = Domains.objects.filter(user_id = request.user.id).count()
    if empleados >= cuenta.limit_dynhost:
        return redirect(reverse('dynamic.views.domains.index'))
    domain = Domains()
    domain.user_id = request.user.id
    if request.method == 'POST':
        form = DomainsForm(request.POST, instance=domain, auto_id=True)
        if form.is_valid():
            form.save()
            return redirect(reverse('dynamic.views.domains.index'))
    else:
        domain.ip = request.META['REMOTE_ADDR']
        form = DomainsForm(instance=domain, auto_id=True)
    return render_to_response('dynhost_edit.html', {
        'cuenta': cuenta,
        'form': form,
        'myip': request.META['REMOTE_ADDR'],
        'empleados': empleados,
        'disponibles': cuenta.limit_dynhost - empleados,
        'total': cuenta.limit_dynhost,
        'tipo': '<strong>DynHost</strong>'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, dom_id):
    empleados = Domains.objects.filter(user_id = request.user.id).count()
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        domain = Domains.objects.get(pk=dom_id)
        if domain.user_id != request.user.id:
            return redirect(reverse('dynamic.views.domains.index'))
        if request.method == 'POST':
            form = DomainsForm(request.POST, instance=domain, auto_id=True)
            if form.is_valid():
                form.save()
                return redirect(reverse('dynamic.views.domains.index'))
        else:
            form = DomainsForm(instance=domain, auto_id=True)
        return render_to_response('dynhost_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'myip': request.META['REMOTE_ADDR'],
            'empleados': empleados,
            'disponibles': cuenta.limit_dynhost - empleados,
            'total': cuenta.limit_dynhost,
            'tipo': '<strong>DynHost</strong>'
        }, context_instance=RequestContext(request))
    except Domains.DoesNotExist:
        return redirect(reverse('dynamic.views.domains.index'))

@login_required(login_url='/')
def delete(request, dom_id):
    try:
        domain = Domains.objects.get(pk=dom_id)
        if domain.user_id != request.user.id:
            return redirect(reverse('dynamic.views.domains.index'))
        domain.delete()
    except Domains.DoesNotExist:
        pass
    return redirect(reverse('dynamic.views.domains.index'))
