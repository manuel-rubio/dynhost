# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import *
from ..models import *
from django.core.urlresolvers import reverse
import sys

@login_required(login_url='/')
def index(request, page=None):
    cuenta = Accounts.objects.get(user = request.user.id)
    servicios = Databases.objects.filter(accounts__id=cuenta.id)
    usados = servicios.count()
    return render_to_response('databases_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_sql - usados,
        'total': cuenta.limit_sql,
        'tipo': 'Base de Datos'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = Databases.objects.filter(accounts__id=cuenta.id).count()
    database = Databases()
    database.accounts_id = cuenta.id
    if request.method == 'POST':
        form = DatabasesForm(request.POST, instance=database, auto_id=False)
        #form.fields['links'].queryset = Users.objects.filter(accounts__id=cuenta.id)
        if form.is_valid():
            form.save()
            return redirect(reverse('database.views.databases.index'))
    else:
        form = DatabasesForm(instance=database, auto_id=False)
        #form.fields['links'].queryset = Users.objects.filter(accounts__id=cuenta.id)
    return render_to_response('databases_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_sql - usados,
        'total': cuenta.limit_sql,
        'tipo': 'Base de Datos'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def show(request, db_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        database = Databases.objects.get(pk=db_id)
        form = DatabasesForm(instance=database, auto_id=False)
        usados = Databases.objects.filter(accounts__id=cuenta.id).count()
        link = UsersDatabases()
        user = AddUsersForm(instance=link, auto_id=False)
        user_actual = UsersDatabases.objects.filter(database__id=db_id).values('user_id').query
        user.fields['user'].queryset = Users.objects.filter(accounts__id=cuenta.id).exclude(id__in=user_actual)
        return render_to_response('databases_edit.html', {
            'cuenta': cuenta,
            'database': database,
            'users': user,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_sql - usados,
            'total': cuenta.limit_sql,
            'tipo': 'Base de Datos',
            'links': UsersDatabases.objects.filter(user__accounts__id=cuenta.id, database__id=db_id),
            'db_id': db_id,
            'show': True
        }, context_instance=RequestContext(request))
    except Databases.DoesNotExist:
        return redirect(reverse('database.views.databases.index'))

@login_required(login_url='/')
def delete(request, db_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        database = Databases.objects.get(pk=db_id)
        if database.accounts.id == cuenta.id:
            database.delete()
        return redirect(reverse('database.views.databases.index'))
    except Databases.DoesNotExist:
        pass
    return redirect(reverse('database.views.databases.index'))

@login_required(login_url='/')
def unlink(request, lk_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        link = UsersDatabases.objects.get(pk=lk_id)
        if link.user.accounts.id == cuenta.id:
            link.delete()
        return redirect(reverse('database.views.databases.show', args=[link.database.id]))
    except UsersDatabases.DoesNotExist:
        pass
    return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def link(request, db_id):
    if request.method == 'POST':
        try:
            cuenta = Accounts.objects.get(user=request.user.id)
            database = Databases.objects.get(pk=db_id)
            if database.accounts.id == cuenta.id:
                if 'user' in request.POST and request.POST['user'] != '':
                    link = UsersDatabases()
                    link.database_id = database.id
                    link.user_id = request.POST['user']
                    link.save()
                return redirect(reverse('database.views.databases.show', args=[database.id]))
        except UsersDatabases.DoesNotExist:
            pass
    return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def execute(request, lk_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        link = UsersDatabases.objects.get(pk=lk_id)
        keys = None
        values = None
        if request.method == 'POST':
            result = link.execute(request.POST['query'])
            keys = result[0].keys()
            values = [ x.values() for x in result ]
        return render_to_response('databases_query.html', {
            'cuenta': cuenta,
            'query': request.POST['query'] if request.method == 'POST' else '',
            'heads': keys,
            'result': values,
            'tipo': 'Base de Datos'
        }, context_instance=RequestContext(request))
    except Databases.DoesNotExist:
        return redirect(reverse('database.views.databases.index'))
