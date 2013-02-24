# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts
from dns.models import Records
from dynhost.models import Domains as DynHosts
from ..models import RedirectDynHost, RedirectDynHostForm
from django.core.urlresolvers import reverse
from django.db import IntegrityError
import sys

def check_owner(rec_id, user_id):
    try:
        uid = DynHosts.objects.get(record__id=rec_id).user_id
        if user_id != uid:
            return False
    except DynHosts.DoesNotExist:
        return False
    return True

@login_required(login_url='/')
def index(request, rec_id, page=None):
    cuenta = Accounts.objects.get(user = request.user.id)
    if not check_owner(rec_id, request.user.id):
        return redirect(reverse('dynhost.views.domains.index'))
    servicios = RedirectDynHost.objects.filter(dynhost__record__id=rec_id)
    usados = servicios.count()
    return render_to_response('web_redirects_dynhost_home.html', {
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
        return redirect(reverse('dynhost.views.domains.index'))
    usados = RedirectDynHost.objects.filter(dynhost__record__id=rec_id).count()
    dynhost = DynHosts.objects.filter(record__id = rec_id)[0]
    redir = RedirectDynHost()
    redir.dynhost_id = dynhost.id
    if request.method == 'POST':
        form = RedirectDynHostForm(request.POST, instance=redir, auto_id=False)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('web.views.redirects_dynamic.index', args=[rec_id]))
            except IntegrityError:
                form._errors['name'] = ["El nombre o la URI ya existen para este DynHost."]
        print >>sys.stderr, form.as_table
    else:
        print >>sys.stderr, "Peticion GET"
        form = RedirectDynHostForm(instance=redir, auto_id=False)
    return render_to_response('web_redirects_dynhost_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_web_redirect - usados,
        'total': cuenta.limit_web_redirect,
        'rec_id': rec_id,
        'dom': dynhost.getName(),
        'tipo': 'Redirecciones Web'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, redir_id):
    cuenta = Accounts.objects.get(user=request.user.id)
    try:
        redir = RedirectDynHost.objects.get(pk=redir_id)
        if redir.dynhost.user_id != cuenta.user_id:
            return redirect(reverse('dynhost.views.domains.index'))
        usados = RedirectDynHost.objects.filter(dynhost__record__id=redir.dynhost.record.id).count()
        if request.method == 'POST':
            form = RedirectDynHostForm(request.POST, instance=redir, auto_id=False)
            if form.is_valid():
                try:
                    form.save()
                    return redirect(reverse('web.views.redirects_dynamic.index', args=[redir.dynhost.record.id]))
                except IntegrityError:
                    form._errors['name'] = ["La redirección ya existe."]
                    del form.cleaned_data['name']
        else:
            form = RedirectDynHostForm(instance=redir, auto_id=False)
        return render_to_response('web_redirects_dynhost_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_web_redirect - usados,
            'total': cuenta.limit_web_redirect,
            'rec_id': redir.dynhost.record.id,
            'dom': redir.dynhost.getName(),
            'tipo': 'Redirecciones Web'
        }, context_instance=RequestContext(request))
    except RedirectDynHost.DoesNotExist:
        return redirect(reverse('dynhost.views.domains.index'))

@login_required(login_url='/')
def delete(request, redir_id):
    try:
        redir = RedirectDynHost.objects.get(pk=redir_id)
        if redir.dynhost.user.id != request.user.id:
            return redirect(reverse('dynhost.views.domains.index'))
        redir.delete()
        return redirect(reverse('web.views.redirects_dynamic.index', args=[redir.dynhost.record_id]))
    except RedirectDynHost.DoesNotExist:
        pass
    return redirect(reverse('dynhost.views.domains.index'))
