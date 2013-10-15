# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import *
from models import *
from django.core.urlresolvers import reverse
from datetime import datetime

def getForm(cuenta, post, ftp):
    if not post:
        form = UsersForm(instance=ftp, auto_id=False)
    else:
        form = UsersForm(post, instance=ftp, auto_id=False)
    form.fields['homedir'].choices = tuple([ (x,x) for x in cuenta.dirs() ])
    return form

@login_required(login_url='/')
def index(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    servicios = Users.objects.filter(accounts = cuenta)
    usados = servicios.count()
    return render_to_response('ftp_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_ftp - usados,
        'total': cuenta.limit_ftp,
        'tipo': 'Accesos FTP'
    }, context_instance=RequestContext(request))
    
@login_required(login_url='/')
def new(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = Users.objects.filter(accounts = cuenta).count()
    if usados >= cuenta.limit_ftp:
        return redirect(reverse('ftp.views.index'))
    ftp = Users()
    ftp.accounts = cuenta
    if request.method == 'POST':
        form = getForm(cuenta, request.POST, ftp)
        if form.is_valid():
            form.save()
            return redirect(reverse('ftp.views.index'))
    else:
        form = getForm(cuenta, request.POST, ftp)
    return render_to_response('ftp_edit.html', {
        'cuenta': cuenta,
        'form': form,
        'usados': usados,
        'disponibles': cuenta.limit_ftp - usados,
        'total': cuenta.limit_ftp,
        'tipo': 'Accesos FTP',
        'nuevo': True,
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, ftp_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = Users.objects.filter(accounts = cuenta).count()
    try:
        ftp = Users.objects.get(pk=ftp_id)
        if ftp.accounts.id != cuenta.id:
            return redirect(reverse('ftp.views.index'))
        if request.method == 'POST':
            form = getForm(cuenta, request.POST, ftp)
            if form.is_valid():
                form.save()
                return redirect(reverse('ftp.views.index'))
        else:
            form = getForm(cuenta, request.POST, ftp)
        return render_to_response('ftp_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_ftp - usados,
            'total': cuenta.limit_ftp,
            'ftp_id': ftp.id,
            'tipo': 'Accesos FTP'
        }, context_instance=RequestContext(request))
    except Users.DoesNotExist:
        return redirect(reverse('ftp.views.index'))

@login_required(login_url='/')
def delete(request, ftp_id):
    try:
        cuenta = Accounts.objects.get(user = request.user.id)
        ftp = Users.objects.get(pk=ftp_id)
        if ftp.accounts.id != cuenta.id:
            return redirect(reverse('ftp.views.index'))
        ftp.delete()
    except Users.DoesNotExist:
        pass
    return redirect(reverse('ftp.views.index'))
