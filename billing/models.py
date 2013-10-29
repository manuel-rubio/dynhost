# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.forms.util import ErrorList
import os
from dynhost import settings
from ovh import soapi

CURRENCIES = (
    ('EUR', '€'),
    ('USD', '$'),
)

class Accounts(models.Model):
    limit_web = models.IntegerField(default=0)
    limit_web_redirect = models.IntegerField(default=0)
    limit_sql = models.IntegerField(default=0)
    limit_sql_users = models.IntegerField(default=0)
    limit_dns = models.IntegerField(default=0)
    limit_ftp = models.IntegerField(default=0)
    limit_email_redirect = models.IntegerField(default=0)
    limit_email_mailbox = models.IntegerField(default=0)
    limit_email_lists = models.IntegerField(default=0)
    limit_dynhost = models.IntegerField(default=5)
    paymonth = models.FloatField(default=0.0)
    currency = models.CharField(max_length=3, default='EUR', choices=CURRENCIES)
    homedir = models.TextField(null=True)
    user = models.OneToOneField(User)
    nic = models.TextField(null=True)
    def __unicode__(self):
        ret = self.user.username + " ("
        ret += "virtual" if not self.homedir else "real"
        ret += ")"
        return ret
    def dirs(self, relative=None, path='www-data'):
        hd = self.getPath(relative) + path
        data = [ root[len(hd):] for root, dir, files in os.walk(hd) if root.find('.svn') == -1 ]
        if len(data)==0:
            data = [ '/' ]
        else:
            data[0] = '/'
        return data
    def getPath(self, relative=None):
        dir = self.homedir
        skel = settings.REAL_USER_SKEL
        if not dir:
            dir = settings.HOMEDIR_BASE
            skel = settings.USER_SKEL
        if relative:
            dir += '/' + skel[relative] % {'userid':self.user.id}
        return dir + '/'

class Payments(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=1, default='H', choices=(
        ('H', 'Hosting'),
        ('P', 'Pago'),
    ))
    price = models.FloatField()
    accounts = models.ForeignKey('Accounts')
    def __unicode__(self):
        return "%(type)s: %(price).2f €" % {'type':self.type, 'price':self.price}

EMAIL_TYPE = (
    ('R', 'Activa Buzones y Redirecciones'),
    ('V', 'Activa Redirecciones'),
    ('', 'Configuración Manual'),
)

class Domains(models.Model):
    domain = models.CharField(max_length=80, unique=True)
    accounts = models.ForeignKey('Accounts')
    email_type = models.CharField(max_length=1, default='R', null=True, choices=EMAIL_TYPE)
    expires = models.DateField(default=None, null=True)
    def __unicode__(self):
        return self.domain

class DomainsForm(forms.ModelForm):
    domain = forms.RegexField(label='Nombre del Dominio', required=True, regex=r'[0-9a-z-_]+\.[a-z]{2,4}')
    email_type = forms.ChoiceField(label='¿Activar email?', required=False, choices=EMAIL_TYPE)
    class Meta:
        model = Domains
        fields = ( 'domain', 'email_type' )

class DomainCheckForm(forms.ModelForm):
    domain = forms.RegexField(label='Nombre del Dominio', required=True, regex=r'[0-9a-z-_]+\.[a-z]{2,4}')
    class Meta:
        model = Domains
        fields = ( 'domain', )
    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.has_key('domain'):
            status = soapi.check_domain(cleaned_data['domain'])
            if not status['is_available'][0]:
                self._errors['domain'] = ErrorList(['El dominio no está disponible.'])
        return cleaned_data

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Accounts.objects.create(user=instance)
    cuenta = Accounts.objects.filter(user__id=instance.id)[0]
    if not cuenta.homedir:
        base = settings.HOMEDIR_BASE + "/"
        skel = settings.USER_SKEL
    else:
        base = cuenta.homedir + "/"
        skel = settings.REAL_USER_SKEL
    for i in skel:
        v = skel[i]
        dir = base + (v % { 'userid': instance.id })
        if not os.path.exists(dir):
            os.makedirs(dir)
