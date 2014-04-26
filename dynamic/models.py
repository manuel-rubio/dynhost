# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from dns.models import Records
from billing.models import Domains as BillingDomains

def clean_unique(form, field, exclude_initial=True,
                 format="Dinámico %(value)s ocupado."):
    value = form.cleaned_data.get(field)
    if value:
        qs = form._meta.model._default_manager.filter(**{field:value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qs = qs.exclude(**{field:initial_value})
        if qs.count() > 0:
            raise forms.ValidationError(format % {'field':field, 'value':value})
    return value

class Domains(models.Model):
    user_id = models.IntegerField()
    domain = models.CharField(max_length=50)
    record = models.ForeignKey('dns.Records')
    ip = models.CharField(max_length=15)
    def getName(self):
        return self.record.getName()
    def __unicode__(self):
        return str(self.user_id) + " " + \
               str(self.record) + " " + self.ip 

class DomainsForm(forms.ModelForm):
    domain = forms.SlugField(label='Dinámico', required=True)
    ip = forms.IPAddressField(label='Dirección IP', required=True)
    class Meta:
        model = Domains
        fields = ( 'domain', 'ip' )
    def clean_domain(self):
        return clean_unique(self, 'domain')

@receiver(pre_save, sender=Domains)
def create_dynamic(sender, instance, **kwargs):
    if not instance.id:
        dynamic = BillingDomains.objects.filter(domain='dynhost.es')[0]
        record = Records()
        record.data = instance.ip
        record.host = instance.domain
        record.domain = dynamic
        record.ttl = 3600
        record.type = 'A'
        record.save()
        instance.record = record
    else:
        instance.record.data = instance.ip
        instance.record.host = instance.domain
        instance.record.save()

@receiver(post_delete, sender=Domains)
def delete_dynamic(sender, instance, **kwargs):
    Records.objects.get(pk=instance.record_id).delete()
