# -*- coding: utf-8 -*-
from django.db import models
from django import forms
import hashlib
from django.forms.util import ErrorList

class RedirectDynamic(models.Model):
    username = models.CharField(max_length=50)
    destin = models.TextField(max_length=250)
    dynamic = models.ForeignKey('dynamic.Domains')
    class Meta:
        unique_together = ("username", "dynamic")

    def user(self):
        return self.username + "@" + self.dynamic.record.host + ".dymmer.com"

    def __unicode__(self):
        return self.user()

class RedirectDynamicForm(forms.ModelForm):
    all_domain = forms.BooleanField(label="¿Redirecciona todo?", required=False,
        widget=forms.CheckboxInput(attrs={'onchange': 'set_redirect_user();', 'id': 'id_type'})
    )
    username = forms.CharField(max_length=50, label="Usuario", required=False,
        widget=forms.TextInput(attrs={'id': 'id_username'})
    )
    destin = forms.CharField(max_length=250, label="Destinos")
    class Meta:
        model = RedirectDynamic
        fields = ("all_domain", "username", "destin")

class Redirect(models.Model):
    username = models.TextField(max_length=50)
    destin = models.TextField(max_length=250)
    domain = models.ForeignKey('billing.Domains')
    class Meta:
        unique_together = ("username", "domain")

    def user(self):
        return self.username + "@" + self.domain.domain

    def __unicode__(self):
        return self.user()

class RedirectForm(forms.ModelForm):
    all_domain = forms.BooleanField(label="¿Redirecciona todo?", required=False,
        widget=forms.CheckboxInput(attrs={'onchange': 'set_redirect_user();', 'id': 'id_type'})
    )
    username = forms.CharField(max_length=50, label="Usuario", required=False,
        widget=forms.TextInput(attrs={'id': 'id_username'})
    )
    destin = forms.CharField(max_length=250, label="Destinos")
    class Meta:
        model = Redirect
        fields = ("all_domain", "username", "destin")

class Mailbox(models.Model):
    username = models.TextField(max_length=250, unique=True)
    password = models.TextField(max_length=32)
    domain = models.ForeignKey('billing.Domains')
    class Meta:
        unique_together = ("username", "domain")

    def user(self):
        return self.username + "@" + self.domain.domain

    def __unicode__(self):
        return self.user()

    @property
    def pwd(self):
        return self.password
    @pwd.setter
    def pwd(self, value):
        if value != '':
            m = hashlib.md5()
            m.update(value)
            self.password = m.hexdigest()

class MailboxForm(forms.ModelForm):
    username = forms.RegexField(
        label='Usuario', max_length=15, min_length=4,
        regex=r'^[a-zA-Z0-9\.]+$',
        error_message='Este campo debe contener solo letras, números y puntos.'
    )
    pwd = forms.CharField(label='Clave', max_length=15, min_length=6, widget=forms.PasswordInput(), required=False)
    pwd_again = forms.CharField(label='Confirma', max_length=15, min_length=6, widget=forms.PasswordInput(), required=False)

    class Meta:
        model=Mailbox
        fields = ( 'username', 'pwd' )

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.has_key('pwd') and cleaned_data.has_key('pwd_again'):
            pwd = cleaned_data['pwd']
            pwd_again = cleaned_data['pwd_again']
            if (len(pwd) > 0 or len(pwd_again)>0) and pwd != pwd_again:
                self._errors['pwd'] = ErrorList(['Las claves deben coincidir'])
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(MailboxForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['pwd'] = instance.pwd

    def save(self, commit=True):
        model = super(MailboxForm, self).save(commit=False)
        model.pwd = self.cleaned_data['pwd']
        if commit:
            model.save()
        return model
