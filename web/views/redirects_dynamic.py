# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts
from dns.models import Records
from dynamic.models import Domains as Dynamics
from ..models import RedirectDynamic, RedirectDynamicForm
from django.core.urlresolvers import reverse
from django.db import IntegrityError
import sys

def check_owner(rec_id, user_id):
    try:
        uid = Dynamics.objects.get(record__id=rec_id).user_id
        if user_id != uid:
            return False
    except Dynamics.DoesNotExist:
        return False
    return True

@login_required(login_url='/')
def index(request, rec_id, page=None):
    cuenta = Accounts.objects.get(user = request.user.id)
    if not check_owner(rec_id, request.user.id):
        return redirect(reverse('dynamic.views.domains.index'))
    servicios = RedirectDynamic.objects.filter(dynamic__record__id=rec_id)
    usados = servicios.count()
    return render_to_response('web_redirects_dynamic_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_web_redirect - usados,
        'total': cuenta.limit_web_redirect,
        'rec_id': rec_id,
        'dom': Records.objects.get(pk=rec_id).getName(),
        'tipo': 'Redirecciones Web'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request, rec_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    if not check_owner(rec_id, request.user.id):
        return redirect(reverse('dynamic.views.domains.index'))
    usados = RedirectDynamic.objects.filter(dynamic__record__id=rec_id).count()
    dynamic = Dynamics.objects.filter(record__id = rec_id)[0]
    redir = RedirectDynamic()
    redir.dynamic_id = dynamic.id
    if request.method == 'POST':
        form = RedirectDynamicForm(request.POST, instance=redir, auto_id=False)
        if form.is_valid():
            try:                
                form.save()
                return redirect(reverse('web.views.redirects_dynamic.index', args=[rec_id]))
            except IntegrityError:
                form.non_field_errors = ["El nombre o la URI ya existen para este nombre dinámico."]
    else:
        form = RedirectDynamicForm(instance=redir, auto_id=False)
    return render_to_response('web_redirects_dynamic_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,        
        'disponibles': cuenta.limit_web_redirect - usados,
        'total': cuenta.limit_web_redirect,
        'rec_id': rec_id,
        'dom': dynamic.getName(),
        'tipo': 'Redirecciones Web',
        'nuevo': True
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, redir_id):
    cuenta = Accounts.objects.get(user=request.user.id)
    try:
        redir = RedirectDynamic.objects.get(pk=redir_id)
        if redir.dynamic.user_id != cuenta.user_id:
            return redirect(reverse('dynamic.views.domains.index'))
        usados = RedirectDynamic.objects.filter(dynamic__record__id=redir.dynamic.record.id).count()
        if request.method == 'POST':
            form = RedirectDynamicForm(request.POST, instance=redir, auto_id=False)
            if form.is_valid():
                try:
                    form.save()
                    return redirect(reverse('web.views.redirects_dynamic.index', args=[redir.dynamic.record.id]))
                except IntegrityError:
                    form._errors['name'] = ["La redirección ya existe."]
                    del form.cleaned_data['name']
        else:
            form = RedirectDynamicForm(instance=redir, auto_id=False)
        return render_to_response('web_redirects_dynamic_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_web_redirect - usados,
            'total': cuenta.limit_web_redirect,
            'rec_id': redir.dynamic.record.id,
            'dom': redir.dynamic.getName(),
            'tipo': 'Redirecciones Web'
        }, context_instance=RequestContext(request))
    except RedirectDynamic.DoesNotExist:
        return redirect(reverse('dynamic.views.domains.index'))

@login_required(login_url='/')
def delete(request, redir_id):
    try:
        redir = RedirectDynamic.objects.get(pk=redir_id)
        if redir.dynamic.user_id != request.user.id:
            return redirect(reverse('dynamic.views.domains.index'))
        redir.delete()
        return redirect(reverse('web.views.redirects_dynamic.index', args=[redir.dynamic.record_id]))
    except RedirectDynamic.DoesNotExist:
        pass
    return redirect(reverse('dynamic.views.domains.index'))
