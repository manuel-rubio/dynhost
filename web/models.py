# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from billing.models import Accounts
import sys
import os
from dynhost import settings

#--- Models

WEB_TYPES = (
    ('H', 'Hosting'),
    ('R', 'Redirección')
)

class Hosting(models.Model):
    name = models.TextField(unique=True, max_length=60)
    type = models.CharField(max_length=1, choices=WEB_TYPES, default='R')
    url = models.TextField(null=True)
    directory = models.TextField(null=True)
    uri = models.TextField()
    record = models.ForeignKey('dns.Records')
    def __unicode__(self):
        return self.name
    class Meta:
        unique_together = (('name', 'record'), ('uri', 'record'))

class RedirectDynHost(models.Model):
    name = models.TextField(unique=True, max_length=60)
    url = models.TextField()
    uri = models.TextField(default='/')
    dynamic = models.ForeignKey('dynamic.Domains', related_name="dynamic.Domains_RedirectDynHost")
    def __unicode__(self):
        return self.name
    class Meta:
        unique_together = (('name', 'dynamic'), ('uri', 'dynamic'))

#--- Forms

class RedirectForm(forms.ModelForm):
    name = forms.SlugField(label='Nombre')
    url = forms.URLField(label='URL', initial='http://', required=True)
    uri = forms.CharField(label='URI', initial='/')
    record = forms.ModelChoiceField(queryset=None,label='Dominio', required=True) # form.fields["rate"].queryset =
    class Meta:
        model = Hosting
        exclude = ( 'directory', 'type', )

class HostingForm(forms.ModelForm):
    name = forms.SlugField(label='Nombre')
    directory = forms.ChoiceField(label='Directorio', required=True)
    uri = forms.CharField(label='URI', initial='/')
    record = forms.ModelChoiceField(queryset=None,label='Dominio', required=True)
    class Meta:
        model = Hosting
        exclude = ( 'url', 'type', )

class RedirectDynHostForm(forms.ModelForm):
    name = forms.SlugField(label='Nombre')
    url = forms.URLField(label='URL', initial='http://')
    uri = forms.CharField(label='URI', initial='/')
    class Meta:
        model = RedirectDynHost
        exclude = ( 'dynamic', )

#--- Triggers

@receiver(pre_save, sender=Hosting)
def create_config_hosting(sender, instance, **kwargs):
    try:
        old = Hosting.objects.get(pk=instance.id)
        filepart_old = old.record.domain.accounts.getPath('hosting') + old.name + '.' + old.record.getName()
        if os.path.exists(filepart_old):
            os.unlink(filepart_old)
    except Hosting.DoesNotExist:
        pass
    if not instance.url:
        filepart = instance.record.domain.accounts.getPath('hosting') + instance.name + '.' + instance.record.getName()
        # guardamos el fichero específico
        outfile = open(filepart, "w")
        outfile.write(settings.APACHE_HOSTING_PART % {
            'path': instance.record.domain.accounts.getPath('www-data') + instance.directory,
            'uri': instance.uri,
            'options': '-Indexes MultiViews SymLinksIfOwnerMatch',
        })
        outfile.close()
    elif not instance.directory:
        filepart = instance.record.domain.accounts.getPath('redirect') + instance.name + '.' + instance.record.getName()
        outfile = open(filepart, "w")
        outfile.write(settings.APACHE_REDIRECT_PART % {
            'uri': instance.uri,
            'url': instance.url
        })
        outfile.close()
    else:
        raise Exception(instance)
    # regeneramos el base
    filebase = instance.record.domain.accounts.getPath('base') + instance.record.getName()
    # guardamos el fichero de configuracion
    outfile = open(filebase, "w")
    outfile.write(settings.APACHE_BASE % {
        'name': instance.record.getName(),
        'email': instance.record.domain.accounts.user.email,
        'configdir': instance.record.domain.accounts.getPath('base'),
        'path': instance.record.domain.accounts.getPath('www-data'),
        'options': '-Indexes MultiViews FollowSymLinks',
        'uid': instance.record.domain.accounts.user.id + 5000,
    })
    outfile.close()
    # recargamos la configuración
    os.system(settings.APACHE_RELOAD_CMD + " &> /dev/null")

@receiver(pre_save, sender=RedirectDynHost)
def create_config_dynhost(sender, instance, **kwargs):
    try:
        old = RedirectDynHost.objects.get(pk=instance.id)
        cuenta = Accounts.objects.get(user__id=old.dynamic.user_id)
        filepart_old = cuenta.getPath('dynhost') + old.name + "." + old.dynamic.getName()
        if os.path.exists(filepart_old):
            os.unlink(filepart_old)
    except RedirectDynHost.DoesNotExist:
        pass
    cuenta = Accounts.objects.get(user__id=instance.dynamic.user_id)
    filepart = cuenta.getPath('dynhost') + instance.name + "." + instance.dynamic.getName()
    # guardamos el fichero específico
    outfile = open(filepart, "w")
    outfile.write(settings.APACHE_REDIRECT_PART % {
        'uri': instance.uri,
        'url': instance.url
    })
    outfile.close()
    # regeneramos el base
    record = instance.dynamic.record
    base = cuenta.getPath('dynhost')
    print >>sys.stderr, "Base: " + base
    filebase = base + record.getName()
    if not os.path.exists(base):
        os.makedirs(base)
    print >>sys.stderr, "Fichero: " + filebase
    # guardamos el fichero de configuracion
    outfile = open(filebase, "w")
    outfile.write(settings.APACHE_BASE % {
        'name': record.getName(),
        'email': cuenta.user.email,
        'dyndir': cuenta.getPath('dynhost')[:-1],
        'reddir': cuenta.getPath('redirect')[:-1],
        'hosdir': cuenta.getPath('hosting')[:-1],
        'logdir': cuenta.getPath('logs')[:-1],
        'path': cuenta.getPath('www-data'),
        'options': '-Indexes MultiViews FollowSymLinks',
        'uid': cuenta.user.id + 5000,
    })
    outfile.close()
    # recargamos la configuracion
    os.system(settings.APACHE_RELOAD_CMD + " &> /dev/null")

@receiver(post_delete, sender=Hosting)
def remove_config_hosting(sender, instance, **kwargs):
    if not instance.url:
        filepart = instance.record.domain.accounts.getPath('hosting') + \
            instance.name + '.' + instance.record.getName()
        os.unlink(filepart)
        os.system(settings.APACHE_RELOAD_CMD + " &> /dev/null")
    elif not instance.directory:
        filepart = instance.record.domain.accounts.getPath('redirect') + \
            instance.name + '.' + instance.record.getName()
        os.unlink(filepart)
        os.system(settings.APACHE_RELOAD_CMD + " &> /dev/null")

@receiver(post_delete, sender=RedirectDynHost)
def remove_config_dynhost(sender, instance, **kwargs):
    cuenta = Accounts.objects.get(user = instance.dynamic.user_id)
    filepart = cuenta.getPath('dynhost') + \
        instance.name + '.' + instance.dynamic.getName()
    os.unlink(filepart)
    os.system(settings.APACHE_RELOAD_CMD + " &> /dev/null")
