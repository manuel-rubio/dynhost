# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.forms.util import ErrorList
from database.models import Databases
from mail.models import Redirect, Mailbox
import os
import sys
from dymmer import settings
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
    phone = models.TextField(null=False)
    address = models.TextField(null=False)
    city = models.TextField(null=False)
    area = models.TextField(null=False)
    zipCode = models.TextField(null=False)
    country = models.CharField(null=False, max_length=2, default='es')
    legalForm = models.CharField(null=False, max_length=12, default='individual', choices=LEGAL_FORM)
    organization = models.TextField(null=True)
    legalName = models.TextField(null=True)
    legalNumber = models.TextField(null=True)
    vat = models.FloatField(default=21.0)
    removed = models.BooleanField(default=False, null=False)

    def country_text(self):
        for (code, text) in COUNTRIES:
            if code == self.country:
                return text
        return None

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
    legalNumber = forms.CharField(required=True, label='CIF/NIF/NIE')
    firstname = forms.CharField(required=True, label='Nombre')
    name = forms.CharField(required=True, label='Apellidos')
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
            'firstname', 'name', 'phone', 'address', 'city', 
            'area', 'zipCode', 'country' )

CURRENCIES = (
    ('EUR', '€'),
    ('USD', '$'),
)

class Accounts(models.Model):
    currency = models.CharField(max_length=3, default='EUR', choices=CURRENCIES)
    user = models.OneToOneField(User)
    nic_data = models.ForeignKey('NIC', null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, blank=False)

    def currency_symbol(self):
        for (i, symbol) in CURRENCIES:
            if i == self.currency:
                return symbol
        return '€'

    def __unicode__(self):
        return self.user.username

CONTRACT_TYPE = (
    ('D', 'Dominio'),
    ('H', 'Disco'),
    ('R', 'Redirecciones de Email'),
    ('m', 'Buzones de Email Plus'),
    ('M', 'Buzones de Email Premium'),
    ('B', 'Base de Datos MySQL'),
)

class Contracts(models.Model):
    type = models.CharField(max_length=1, default='D', choices=CONTRACT_TYPE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    accounts = models.ForeignKey('Accounts')
    begins = models.DateField(auto_now_add=True)
    ends = models.DateField(null=True, default=None)
    concept = models.CharField(max_length=100)
    invoice_id = models.IntegerField(null=True)

    def total_vat(self):
        vat = self.accounts.nic_data.vat / 100.0
        return float(self.price * self.quantity - self.discount) * vat

    def total_incl_vat(self):
        vat = self.accounts.nic_data.vat / 100.0 + 1
        return float(self.price * self.quantity - self.discount) * vat

    def type_text(self):
        for (i,text) in CONTRACT_TYPE:
            if i == self.type:
                return text
        return self.type

    def transfer_concept(self):
        return "ES-%03X-%04X" % (self.accounts_id, self.id)

    def total(self):
        return self.price * self.quantity - self.discount

PAYMENT_TYPE = (
    ('P', 'PayPal'),
    ('T', 'Transferencia'),
)

class Payments(models.Model):
    date = models.DateField()
    amount = models.FloatField()
    accounts = models.ForeignKey('Accounts')
    provider = models.CharField(max_length=1, default='P', null=False, choices=PAYMENT_TYPE)
    tax = models.FloatField()

    def __unicode__(self):
        return "%(type)s: %(price).2f €" % {'type':self.provider_text(), 'price':self.amount}

    def provider_text(self):
        for (i,text) in PAYMENT_TYPE:
            if i == self.provider:
                return text
        return self.type


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
    contract = models.ForeignKey('Contracts', null=True)
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
    tos = forms.BooleanField(label='', required=True)
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
