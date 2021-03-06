# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains
from dynamic.models import Domains as Dynamics
from dns.models import Records
from mail.models import RedirectDynamic, RedirectDynamicForm
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db import connection
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
    if not check_owner(rec_id, request.user.id):
        return redirect(reverse('dynamic.views.domains.index'))
    cuenta = Accounts.objects.get(user = request.user.id)
    servicios = RedirectDynamic.objects.filter(dynamic__record__id=rec_id)
    usados = servicios.count()
    return render_to_response('mail_redirects_dynamic_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_email_redirect - usados,
        'total': cuenta.limit_email_redirect,
        'rec_id': rec_id,
        'dom': Records.objects.get(pk=rec_id).getName(),
        'tipo': 'Redirecciones'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request, rec_id):
    if not check_owner(rec_id, request.user.id):
        return redirect(reverse('dynamic.views.domains.index'))
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = RedirectDynamic.objects.filter(dynamic__record__id=rec_id).count()
    dynamic = Dynamics.objects.filter(record__id = rec_id)[0]
    redir = RedirectDynamic()
    # Cuento cuantos usuarios nulos existe, para comprar si ya ha 
    # marcado el checkbox de "Redireccionar todo"
    if RedirectDynamic.objects.filter(dynamic__record__id=rec_id).filter(username='').count() == 1 :
        exist_all_redirect = True
    else:
        exist_all_redirect = False        
    redir.dynamic_id = dynamic.id

    if request.method == 'POST':
        form = RedirectDynamicForm(request.POST, instance=redir, auto_id=False)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('mail.views.redirects_dynamic.index', args=[rec_id]))
            except IntegrityError:
                connection._rollback()
                form._errors['username'] = ["El usuario ya existe."]
                del form.cleaned_data['username']
    else:
        form = RedirectDynamicForm(instance=redir, auto_id=False)
    return render_to_response('mail_redirects_dynamic_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_email_redirect - usados,
        'total': cuenta.limit_email_redirect,
        'rec_id': rec_id,
        'dom': dynamic.getName(),
        'tipo': 'Redirecciones',
        'nuevo': True,
        'exist_all_redirect': exist_all_redirect
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, mbox_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        redir = RedirectDynamic.objects.get(pk=mbox_id)
        if redir.dynamic.user_id != cuenta.user_id:
            return redirect(reverse('dynamic.views.domains.index'))
        usados = RedirectDynamic.objects.filter(dynamic__record__id=redir.dynamic.record.id).count()
        if request.method == 'POST':
            form = RedirectDynamicForm(request.POST, instance=redir, auto_id=False)
            if form.is_valid():
                try:
                    form.save()
                    return redirect(reverse('mail.views.redirects_dynamic.index', args=[redir.dynamic.record.id]))
                except IntegrityError:
                    connection._rollback()
                    form._errors['username'] = ["El usuario ya existe."]
                    del form.cleaned_data['username']
        else:
            form = RedirectDynamicForm(instance=redir, auto_id=False)
        return render_to_response('mail_redirects_dynamic_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_email_redirect - usados,
            'total': cuenta.limit_email_redirect,
            'rec_id': redir.dynamic.record.id,
            'dom': redir.dynamic.getName(),
            'tipo': 'Redirecciones'
        }, context_instance=RequestContext(request))
    except RedirectDynamic.DoesNotExist:
        return redirect(reverse('dynamic.views.domains.index'))

@login_required(login_url='/')
def delete(request, mbox_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        print >>sys.stderr, mbox_id
        redir = RedirectDynamic.objects.get(pk=mbox_id)
        if redir.dynamic.user_id != request.user.id:
            return redirect(reverse('dynamic.views.domains.index'))
        redir.delete()
        return redirect(reverse('mail.views.redirects_dynamic.index', args=[redir.dynamic.record_id]))
    except RedirectDynamic.DoesNotExist:
        pass
    return redirect(reverse('dynamic.views.domains.index'))
