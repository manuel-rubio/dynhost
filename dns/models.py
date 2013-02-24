# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from billing.models import Domains
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.util import ErrorList
from datetime import datetime
from dynhost import settings
import socket
import re

CHOICES = choices=(
    ('A', 'Dirección IP (A)'),
    ('CNAME', 'Alias (CNAME)'),
    ('MX', 'Correo (MX)'),
    ('TXT', 'Especial (TXT)'),
)

class Records(models.Model):
    host = models.TextField()
    ttl = models.IntegerField(default=38400)
    type = models.CharField(max_length=6, choices=CHOICES)
    mx_priority = models.IntegerField(null=True)
    resp_person = models.TextField(null=True)
    serial = models.IntegerField(null=True)
    refresh = models.IntegerField(null=True)
    retry = models.IntegerField(null=True)
    expire = models.IntegerField(null=True)
    minimum = models.IntegerField(null=True)
    data = models.TextField(null=True)
    domain = models.ForeignKey('billing.Domains')
    def getName(self):
        return ((self.host + ".") if self.host != '@' else '') + self.domain.domain
    def __unicode__(self):
        return self.domain.domain + ": " + self.host + " (" + self.type + ")"
    @property
    def email(self):
        return self.resp_person.replace('.', '@', 1)[:-1]
    @email.setter
    def email(self, value):
        self.resp_person = value.replace('@', '.') + '.'

class SoaRecordForm(forms.ModelForm):
    ttl = forms.IntegerField(label='Tiempo de Vida (seg)', initial=38400)
    email = forms.EmailField(max_length=250, label='Email del Responsable')
    class Meta:
        model = Records
        fields = ( 'ttl', 'email' )

    def __init__(self, *args, **kwargs):
        super(SoaRecordForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['email'] = instance.email

    def save(self, commit=True):
        model = super(SoaRecordForm, self).save(commit=False)
        model.email = self.cleaned_data['email']
        if commit:
            model.save()
        return model

class RecordsForm(forms.ModelForm):
    type = forms.ChoiceField(label='Tipo de registro', choices=CHOICES,
        widget=forms.Select(attrs={'onchange': 'set_fields();', 'id': 'id_type'})
    )
    ttl = forms.IntegerField(label='Tiempo de Vida (seg)', initial=38400)
    mx_priority = forms.IntegerField(label='Prioridad', required=False,
        widget=forms.TextInput(attrs={'id': 'id_mx_priority'})
    )
    host = forms.CharField(max_length=120, label='Nombre',
        widget=forms.TextInput(attrs={'id': 'id_host'})
    )
    data = forms.CharField(max_length=120, label='Contenido')

    class Meta:
        model = Records
        fields = ( 'type', 'ttl', 'mx_priority', 'host', 'data' )

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['type'] == 'A' and cleaned_data.has_key('data'):
            try:
                socket.inet_aton(cleaned_data['data'])
            except socket.error:
                self._errors['data'] = ErrorList(['Dirección IP no válida.'])
        elif cleaned_data['type'] == 'CNAME' and cleaned_data.has_key('data'):
            # se permiten nombre de máquinas y dominios absolutos
            p = re.compile(r'^([0-9a-zA-Z-_\.]+\.|[0-9a-zA-Z-_]+)$')
            if not p.match(cleaned_data['data']):
                self._errors['data'] = ErrorList(['Debe indicar un nombre de máquina o dominio (terminado el punto).'])
        elif cleaned_data['type'] == 'MX' and cleaned_data.has_key('data'):
            # se permiten nombre de máquinas
            record = Records.objects.filter(type='A',host=cleaned_data['data'])
            if not record:
                self._errors['data'] = ErrorList(['mensaje'])
            elif cleaned_data['data'] == '@':
                cleaned_data['data'] = record[0].domain.domain + '.'
        return cleaned_data

@receiver(post_save, sender=Domains)
def add_fixed_records(sender, instance, created, **kwargs):
    if created:
        soa = Records()
        soa.type = 'SOA'
        soa.domain = instance
        soa.serial = datetime.now().strftime('%Y%m%d%H')
        soa.refresh = 10800
        soa.expire = 604800
        soa.retry = 3600
        soa.minimum = 38400
        soa.host = '@'
        soa.data = 'ovh.bosqueviejo.net.'
        soa.email = instance.accounts.user.email
        for i in range(1,5):
            ns = Records()
            ns.type = 'NS'
            ns.host = '@'
            ns.data = 'ns' + str(i) + '.bosqueviejo.net.'
            ns.domain = instance
            ns.save()
        primary = Records()
        primary.type = 'A'
        primary.domain = instance
        primary.host = '@'
        primary.data = settings.DEFAULT_IP
        primary.save()
    if instance.email_type in [ 'R', 'V' ]:
        Records.objects.filter(type='MX').filter(domain__id=instance.id).delete()
        mx = Records()
        mx.type = 'MX'
        mx.mx_priority = 0
        mx.host = '@'
        mx.data = instance.domain + '.'
        mx.domain = instance
        mx.save()
