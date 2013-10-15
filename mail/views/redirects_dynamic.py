# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains
from dynamic.models import Domains as DynHosts
from dns.models import Records
from mail.models import RedirectDynHost, RedirectDynHostForm
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
    if not check_owner(rec_id, request.user.id):
        return redirect(reverse('dynamic.views.domains.index'))
    cuenta = Accounts.objects.get(user = request.user.id)
    servicios = RedirectDynHost.objects.filter(record__id=rec_id)
    usados = servicios.count()
    record = Records.objects.get(pk=rec_id)
    return render_to_response('mail_redirects_dynhost_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_email_redirect - usados,
        'total': cuenta.limit_email_redirect,
        'rec_id': rec_id,
        'dom': record.host + '.' + record.domain.domain,
        'tipo': 'Redirecciones'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request, rec_id):
    if not check_owner(rec_id, request.user.id):
        return redirect(reverse('dynamic.views.domains.index'))
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = RedirectDynHost.objects.filter(record__id=rec_id).count()
    record = Records.objects.get(pk=rec_id)
    redir = RedirectDynHost()
    redir.record_id = record.id
    if request.method == 'POST':
        form = RedirectDynHostForm(request.POST, instance=redir, auto_id=False)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('mail.views.redirects_dynamic.index', args=[rec_id]))
            except IntegrityError:
                form._errors['username'] = "El usuario ya existe."
                del form.cleaned_data['username']
    else:
        form = RedirectDynHostForm(instance=redir, auto_id=False)
    return render_to_response('mail_redirects_dynhost_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_email_redirect - usados,
        'total': cuenta.limit_email_redirect,
        'rec_id': rec_id,
        'dom': record.host + '.' + record.domain.domain,
        'tipo': 'Redirecciones'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, mbox_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        redir = RedirectDynHost.objects.get(pk=mbox_id)
        if redir.record.domain.accounts.id != cuenta.id:
            return redirect(reverse('dynamic.views.domains.index'))
        usados = RedirectDynHost.objects.filter(record__id=redir.record.id).count()
        if request.method == 'POST':
            form = RedirectDynHostForm(request.POST, instance=redir, auto_id=False)
            if form.is_valid():
                try:
                    form.save()
                    return redirect(reverse('mail.views.redirects_dynamic.index', args=[redir.record.id]))
                except IntegrityError:
                    form._errors['username'] = ["El usuario ya existe."]
                    del form.cleaned_data['username']
        else:
            form = RedirectDynHostForm(instance=redir, auto_id=False)
        return render_to_response('mail_redirects_dynhost_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_email_redirect - usados,
            'total': cuenta.limit_email_redirect,
            'rec_id': redir.record.id,
            'dom': redir.record.host + '.' + redir.record.domain.domain,
            'tipo': 'Redirecciones'
        }, context_instance=RequestContext(request))
    except RedirectDynHost.DoesNotExist:
        return redirect(reverse('dynamic.views.domains.index'))

@login_required(login_url='/')
def delete(request, mbox_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        print >>sys.stderr, mbox_id
        redir = RedirectDynHost.objects.get(pk=mbox_id)
        if redir.record.domain.accounts.id != cuenta.id:
            return redirect(reverse('dynamic.views.domains.index'))
        redir.delete()
        return redirect(reverse('mail.views.redirects_dynamic.index', args=[redir.record_id]))
    except RedirectDynHost.DoesNotExist:
        pass
    return redirect(reverse('dynamic.views.domains.index'))
