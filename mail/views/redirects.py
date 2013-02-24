# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains
from ..models import Redirect, RedirectForm
from django.core.urlresolvers import reverse
from django.db import IntegrityError
import sys

def check_owner(dom_id, acc_id):
    try:
        cuenta = Domains.objects.get(pk=dom_id).accounts
        if cuenta.id != acc_id:
            return False
    except Domains.DoesNotExist:
        return False
    return True

@login_required(login_url='/')
def index(request, dom_id, page=None):
    cuenta = Accounts.objects.get(user = request.user.id)
    if not check_owner(dom_id, cuenta.id):
        return redirect(reverse('dns.views.domains.index'))
    servicios = Redirect.objects.filter(domain__id=dom_id)
    usados = servicios.count()
    return render_to_response('mail_redirects_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_email_redirect - usados,
        'total': cuenta.limit_email_redirect,
        'dom_id': dom_id,
        'dom': Domains.objects.get(pk=dom_id).domain,
        'tipo': 'Redirecciones'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request, dom_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    if not check_owner(dom_id, cuenta.id):
        return redirect(reverse('dns.views.domains.index'))
    usados = Redirect.objects.filter(domain__id=dom_id).count()
    domain = Domains.objects.get(pk=dom_id)
    redir = Redirect()
    redir.domain_id = domain.id
    if request.method == 'POST':
        form = RedirectForm(request.POST, instance=redir, auto_id=False)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('mail.views.redirects.index', args=[dom_id]))
            except IntegrityError:
                form._errors['username'] = "El usuario ya existe."
                del form.cleaned_data['username']
        print >>sys.stderr, form.errors
    else:
        print >>sys.stderr, "Peticion GET"
        form = RedirectForm(instance=redir, auto_id=False)
    return render_to_response('mail_redirects_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_email_redirect - usados,
        'total': cuenta.limit_email_redirect,
        'dom_id': dom_id,
        'dom': domain.domain,
        'tipo': 'Redirecciones'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, mbox_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        redir = Redirect.objects.get(pk=mbox_id)
        if redir.domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        usados = Redirect.objects.filter(domain__id=redir.domain.id).count()
        if request.method == 'POST':
            form = RedirectForm(request.POST, instance=redir, auto_id=False)
            if form.is_valid():
                try:
                    form.save()
                    return redirect(reverse('mail.views.redirects.index', args=[redir.domain.id]))
                except IntegrityError:
                    form._errors['username'] = ["El usuario ya existe."]
                    del form.cleaned_data['username']
        else:
            form = RedirectForm(instance=redir, auto_id=False)
        return render_to_response('mail_redirects_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_email_redirect - usados,
            'total': cuenta.limit_email_redirect,
            'dom_id': redir.domain.id,
            'dom': redir.domain.domain,
            'tipo': 'Redirecciones'
        }, context_instance=RequestContext(request))
    except Redirect.DoesNotExist:
        return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def delete(request, mbox_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        print >>sys.stderr, mbox_id
        redir = Redirect.objects.get(pk=mbox_id)
        if redir.domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        redir.delete()
        return redirect(reverse('mail.views.redirects.index', args=[redir.domain_id]))
    except Redirect.DoesNotExist:
        pass
    return redirect(reverse('dns.views.domains.index'))
