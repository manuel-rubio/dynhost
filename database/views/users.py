# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import *
from ..models import *
from django.core.urlresolvers import reverse
from django.db.models import Q
import sys

@login_required(login_url='/')
def index(request, page=None):
    cuenta = Accounts.objects.get(user = request.user.id)
    servicios = Users.objects.filter(accounts__id=cuenta.id).order_by('username')
    usados = servicios.count()
    return render_to_response('databases_users_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_sql_users - usados,
        'total': cuenta.limit_sql_users,
        'tipo': 'Usuarios BD',
        'form': UsersForm(instance=Users(), auto_id=False),
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request):
    cuenta = Accounts.objects.get(user = request.user.id)
    usados = Users.objects.filter(accounts__id=cuenta.id).count()
    user = Users()
    user.accounts_id = cuenta.id
    if request.method == 'POST':
        form = UsersForm(request.POST, instance=user, auto_id=True)
        #form.fields['links'].queryset = Databases.objects.filter(accounts__id=cuenta.id)
        if form.is_valid():
            form.save()
            return redirect(reverse('database.views.users.index'))
        print >>sys.stderr, form.errors
    else:
        print >>sys.stderr, "Peticion GET"
        form = UsersForm(instance=user, auto_id=True)
        #form.fields['links'].queryset = Databases.objects.filter(accounts__id=cuenta.id)
    return render_to_response('databases_users_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_sql_users - usados,
        'total': cuenta.limit_sql_users,
        'tipo': 'Usuarios BD'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, user_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        user = Users.objects.get(pk=user_id)
        link = UsersDatabases()
        database = AddDatabasesForm(instance=link, auto_id=False)
        database_actual = UsersDatabases.objects.filter(user__id=user_id).values('database_id').query
        database.fields['database'].queryset = Databases.objects.filter(accounts__id=cuenta.id).exclude(id__in=database_actual)
        if request.method == 'POST':
            form = UsersForm(request.POST, instance=user, auto_id=True)
            #form.fields['links'].queryset = Databases.objects.filter(accounts__id=cuenta.id)
            if form.is_valid():
                form.save()
                return redirect(reverse('database.views.users.index'))
        else:
            form = UsersForm(instance=user, auto_id=True)
            #form.fields['links'].queryset = Databases.objects.filter(accounts__id=cuenta.id)
        usados = Users.objects.filter(accounts__id=cuenta.id).count()
        return render_to_response('databases_users_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'database': database,
            'usados': usados,
            'disponibles': cuenta.limit_sql_users - usados,
            'total': cuenta.limit_sql_users,
            'tipo': 'Usuarios BD',
            'links': UsersDatabases.objects.filter(user__accounts__id=cuenta.id, user__id=user_id),
            'user_id': user_id,
            'show': True
        }, context_instance=RequestContext(request))
    except Users.DoesNotExist:
        return redirect(reverse('database.views.users.index'))

@login_required(login_url='/')
def delete(request, user_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        user = Users.objects.get(pk=user_id)
        if user.accounts.id == cuenta.id:
            user.delete()
            return redirect(reverse('database.views.users.index'))
    except Users.DoesNotExist:
        pass
    return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def unlink(request, lk_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        link = UsersDatabases.objects.get(pk=lk_id)
        if link.user.accounts.id == cuenta.id:
            link.delete()
            return redirect(reverse('database.views.users.edit', args=[link.user.id]))
    except UsersDatabases.DoesNotExist:
        pass
    return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def link(request, user_id):
    if request.method == 'POST':
        try:
            cuenta = Accounts.objects.get(user=request.user.id)
            user = Users.objects.get(pk=user_id)
            if user.accounts.id == cuenta.id:
                if 'database' in request.POST and request.POST['database'] != '':
                    link = UsersDatabases()
                    link.user_id = user.id
                    link.database_id = request.POST['database']
                    link.save()
                return redirect(reverse('database.views.users.edit', args=[user.id]))
        except UsersDatabases.DoesNotExist:
            pass
    return redirect(reverse('dns.views.domains.index'))
