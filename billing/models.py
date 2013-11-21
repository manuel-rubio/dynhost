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

LEGAL_FORM = (
    ('corporation', 'Corporation'),
    ('individual', 'Individual'),
    ('association', 'Association'),
    ('other', 'Other')
)

class NIC(models.Model):
    name = models.TextField(null=False)
    firstname = models.TextField(null=False)
    password = models.TextField(null=False, default=settings.OVH_USERS_PASS)
    email = models.TextField(null=False)
    phone = models.TextField(null=False)
    address = models.TextField(null=False)
    city = models.TextField(null=False)
    area = models.TextField(null=False)
    zipCode = models.TextField(null=False)
    country = models.CharField(null=False, max_length=2, default='es')
    language = models.CharField(null=False, max_length=2, default='es')
    legalForm = models.CharField(null=False, max_length=12, default='individual', choices=LEGAL_FORM)
    organization = models.TextField(null=True)
    legalName = models.TextField(null=True)
    legalNumber = models.TextField(null=True)
    vat = models.FloatField(default=21.0)
    nic = models.CharField(null=False, max_length=20)
    removed = models.BooleanField(default=False, null=False)

COUNTRIES = (
    ('es', 'España'),
    ('fr', 'Francia'),
    ('uk', 'Reino Unido'),
    ('pt', 'Portugal'),
    ('it', 'Italia'),
    ('us', 'Estados Unidos'),
    ('co', 'Colombia'),
)

class NICform(forms.ModelForm):
    legalForm = forms.ChoiceField(label='Formal Legal', required=True, choices=LEGAL_FORM,
        widget=forms.Select(attrs={'onchange': 'set_fields();'}))
    organization = forms.CharField(required=False, label='Organización')
    legalName = forms.CharField(required=False, label='Empresa')
    legalNumber = forms.CharField(required=False, label='CIF')
    firstname = forms.CharField(required=True, label='Nombre')
    name = forms.CharField(required=True, label='Apellidos')
    email = forms.EmailField(required=True, label='Email')
    phone = forms.IntegerField(required=True, label='Teléfono')
    address = forms.CharField(required=True, label='Dirección')
    city = forms.CharField(required=True, label='Ciudad')
    area = forms.CharField(required=True, label='Provincia')
    zipCode = forms.IntegerField(required=True, label='Código Postal')
    country = forms.ChoiceField(label='País', required=True, choices=COUNTRIES)

    class Meta:
        model = NIC
        fields = ( 
            'legalForm', 'legalNumber', 'legalName', 'organization',
            'firstname', 'name', 'email', 'phone', 'address', 'city', 
            'area', 'zipCode', 'country' )

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
    nic_data = models.ForeignKey('NIC', null=True)

    def __unicode__(self):
        ret = self.user.username + " ("
        ret += "virtual" if not self.homedir else "real"
        ret += ")"
        return ret

    def dirs(self, relative='www-data'):
        base = self.getPath(relative)
        return { '/': {'content': self._dirs(base, base), 'id':'/' }}

    def _dirs(self, hd, base):
        data = {}
        for name in os.listdir(hd):
            subdir = os.path.join(hd, name)
            if os.path.isdir(subdir):
                data[name] = { 'id': subdir[len(base)-1:], 'content': self._dirs(subdir, base) }
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

DOMAIN_STATUS = (
    ('Z', 'Gratuito'),
    ('N', 'Solicitado Nuevo Dominio'),
    ('T', 'Solicitada Transferencia'),
    ('A', 'Activo'),
    ('B', 'Bloqueado'),
)

class Domains(models.Model):
    domain = models.CharField(max_length=80, unique=True)
    accounts = models.ForeignKey('Accounts')
    email_type = models.CharField(max_length=1, default='R', null=True, choices=EMAIL_TYPE)
    expires = models.DateField(default=None, null=True)
    status = models.CharField(max_length=1, default='Z', null=False, choices=DOMAIN_STATUS)
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

    def _is_valid_suffix(self, domain):
        for i in settings.TLD_GRANTED:
            if domain[-len(i):] == i:
                return True
        return False

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.has_key('domain'):
            if not self._is_valid_suffix(cleaned_data['domain']):
                self._errors['domain'] = ErrorList(['Dominio no válido.'])
            else:
                status = soapi.check_domain(cleaned_data['domain'])
                if not status['is_available'][0]:
                    self._errors['domain'] = ErrorList(['El dominio no está disponible.'])
        return cleaned_data

class DomainTransferForm(forms.ModelForm):
    domain = forms.RegexField(label='Nombre del Dominio', required=True, regex=r'[0-9a-z-_]+\.[a-z]{2,4}')
    authinfo = forms.CharField(label='Auth. Info.', required=True)
    class Meta:
        model = Domains 
        fields = ( 'domain', 'authinfo' )
    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.has_key('domain'):
            status = soapi.check_domain(cleaned_data['domain'])
            if not status['is_transferable'][0]:
                self._errors['domain'] = ErrorList(['El dominio no es transferible.'])
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
