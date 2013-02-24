# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from billing.models import Accounts, Domains
from ..models import Mailbox, MailboxForm
from django.core.urlresolvers import reverse
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
    servicios = Mailbox.objects.filter(domain__id=dom_id)
    usados = servicios.count()
    return render_to_response('mail_mailboxes_home.html', {
        'cuenta': cuenta,
        'servicios': servicios,
        'usados': usados,
        'disponibles': cuenta.limit_email_mailbox - usados,
        'total': cuenta.limit_email_mailbox,
        'dom_id': dom_id,
        'dom': Domains.objects.get(pk=dom_id).domain,
        'tipo': 'Buzones'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def new(request, dom_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    if not check_owner(dom_id, cuenta.id):
        return redirect(reverse('dns.views.domains.index'))
    usados = Mailbox.objects.filter(domain__id=dom_id).count()
    domain = Domains.objects.get(pk=dom_id)
    mailbox = Mailbox()
    mailbox.domain_id = domain.id
    if request.method == 'POST':
        form = MailboxForm(request.POST, instance=mailbox, auto_id=False)
        if form.is_valid():
            form.save()
            return redirect(reverse('mail.views.mailboxes.index', args=[dom_id]))
    else:
        form = MailboxForm(instance=mailbox, auto_id=False)
    return render_to_response('mail_mailboxes_edit.html', {
        'form': form,
        'cuenta': cuenta,
        'usados': usados,
        'disponibles': cuenta.limit_email_mailbox - usados,
        'total': cuenta.limit_email_mailbox,
        'dom_id': dom_id,
        'dom': domain.domain,
        'tipo': 'Buzones'
    }, context_instance=RequestContext(request))

@login_required(login_url='/')
def edit(request, mbox_id):
    cuenta = Accounts.objects.get(user = request.user.id)
    try:
        mailbox = Mailbox.objects.get(pk=mbox_id)
        if mailbox.domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        usados = Mailbox.objects.filter(domain__id=mailbox.domain.id).count()
        if request.method == 'POST':
            form = MailboxForm(request.POST, instance=mailbox, auto_id=False)
            if form.is_valid():
                form.save()
                return redirect(reverse('mail.views.mailboxes.index', args=[mailbox.domain.id]))
        else:
            form = MailboxForm(instance=mailbox, auto_id=False)
        return render_to_response('mail_mailboxes_edit.html', {
            'cuenta': cuenta,
            'form': form,
            'usados': usados,
            'disponibles': cuenta.limit_email_mailbox - usados,
            'total': cuenta.limit_email_mailbox,
            'dom_id': mailbox.domain.id,
            'dom': mailbox.domain.domain,
            'tipo': 'Buzones'
        }, context_instance=RequestContext(request))
    except Mailbox.DoesNotExist:
        return redirect(reverse('dns.views.domains.index'))

@login_required(login_url='/')
def delete(request, mbox_id):
    try:
        cuenta = Accounts.objects.get(user=request.user.id)
        print >>sys.stderr, mbox_id
        mailbox = Mailbox.objects.get(pk=mbox_id)
        if mailbox.domain.accounts.id != cuenta.id:
            return redirect(reverse('dns.views.domains.index'))
        mailbox.delete()
        return redirect(reverse('mail.views.mailboxes.index', args=[mailbox.domain_id]))
    except Mailbox.DoesNotExist:
        pass
    return redirect(reverse('dns.views.domains.index'))
