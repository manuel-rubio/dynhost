# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.forms.util import ErrorList
import os
from dynhost import settings
import hashlib

#--- Validations

def validate_real_user(value):
	passwd = open("/etc/passwd", "r")
	for p in passwd:
		data = p.split(':')
		if len(data) > 0 and data[0][0].strip() != '#':
			if (data[0] == value):
				passwd.close()
				raise ValidationError(u'Usuario existente en sistema, use otro.')
	passwd.close()

#--- Models

class Users(models.Model):
    userid = models.TextField(unique=True, validators=[validate_real_user])
    passwd = models.TextField()
    # uid sera tomado del ID de billing.Accounts + 5000
    # gid sera fijado a 1003
    homedir = models.TextField()
    # shell sera fijado a /sbin/nologin
    accounts = models.ForeignKey('billing.Accounts')

    def __unicode__(self):
        return self.userid
        
    @property
    def pwd(self):
        return self.passwd
    @pwd.setter
    def pwd(self, value):
        if value != '':
            m = hashlib.md5()
            m.update(value)
            self.passwd = m.hexdigest()

#--- Forms

class UsersForm(forms.ModelForm):
    userid = forms.RegexField(
        label='Usuario', max_length=15, min_length=6,
        regex=r'^[a-zA-Z0-9\.]+$',
        error_message='Este campo debe contener solo letras, números y puntos.'
    )
    pwd = forms.CharField(label='Clave', max_length=15, min_length=6, widget=forms.PasswordInput(), required=False)
    pwd_again = forms.CharField(label='Confirma', max_length=15, min_length=6, widget=forms.PasswordInput(), required=False)
    homedir = forms.ChoiceField(label='Directorio', required=True)
    class Meta:
        model = Users
        exclude = ( 'accounts', 'passwd' )

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.has_key('pwd') and cleaned_data.has_key('pwd_again'):
            pwd = cleaned_data['pwd']
            pwd_again = cleaned_data['pwd_again']
            if (len(pwd) > 0 or len(pwd_again)>0) and pwd != pwd_again:
                self._errors['pwd'] = ErrorList(['Las claves deben coincidir'])
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['pwd'] = instance.pwd

    def save(self, commit=True):
        model = super(UsersForm, self).save(commit=False)
        model.pwd = self.cleaned_data['pwd']
        if commit:
            model.save()
        return model

#--- Triggers

@receiver(pre_save, sender=Users)
def create_config(sender, instance, **kwargs):
    try:
        old = Users.objects.get(pk=instance.id)
        filepart_old = settings.HOMEDIR_BASE + "/ftp/"+ old.userid + ".conf"
        if os.path.exists(filepart_old):
            os.unlink(filepart_old)
    except Users.DoesNotExist:
        pass
    filename = settings.HOMEDIR_BASE + "/ftp/"+ instance.userid + ".conf"
    # guardamos el fichero de configuracion
    outfile = open(filename, "w")
    outfile.write(settings.PROFTPD_CONFIG_BASE % {'user':instance.userid})
    outfile.close()
    # recargamos la configuracion
    os.system(settings.PROFTPD_RELOAD_CMD + " &> /dev/null")

@receiver(post_delete, sender=Users)
def remove_config(sender, instance, **kwargs):
    # eliminamos el fichero
    filename = settings.HOMEDIR_BASE + "/ftp/"+ instance.userid + ".conf"
    os.unlink(filename)
    # recargamos la configuracion
    os.system(settings.PROFTPD_RELOAD_CMD + " &> /dev/null")
