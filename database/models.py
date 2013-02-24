# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
import MySQLdb as mysql
from dynhost import settings
import re
import sys

def execute(sql):
    conn = mysql.connect(
        host=settings.MARIADB_HOST, 
        user=settings.MARIADB_USER, 
        db='mysql', 
        passwd=settings.MARIADB_PASS
    )
    cursor = conn.cursor()
    print >>sys.stderr, sql
    cursor.execute(sql)
    cursor.close()
    conn.close()

#--- Validations

def validate_database_name(value):
    reserved = ['mysql', 'information_schema', 'test']
    if not re.match("^[a-zA-Z0-9_]+$", value) or value in reserved:
        raise ValidationError(u'Nombre de la Base de Datos no válido.')

def validate_username(value):
    reserved = ['root']
    if value in reserved:
        raise ValidationError(u'No es posible usar ese nombre para el usuario.')

#--- Models

class Users(models.Model):
    username = models.CharField(max_length=50, validators=[validate_username], unique=True)
    password = models.CharField(max_length=50)
    accounts = models.ForeignKey('billing.Accounts', related_name='dbusers')
    #links = models.ManyToManyField('Databases', through='UsersDatabases')
    def __unicode__(self):
        return self.username

class Databases(models.Model):
    database = models.CharField(max_length=50, unique=True, validators=[validate_database_name])
    accounts = models.ForeignKey('billing.Accounts')
    #links = models.ManyToManyField('Users', through='UsersDatabases')
    
    def __unicode__(self):
        return self.database

class UsersDatabases(models.Model):
    user = models.ForeignKey('Users')
    database = models.ForeignKey('Databases')
    class Meta:
        unique_together = ('user', 'database')
        #auto_created = True  # con esto no funcional las signals
    
    def execute(self, query):
        conn = mysql.connect(
            host='localhost',
            user=self.user.username,
            db=self.database.database,
            passwd=self.user.password
        )
        cur = conn.cursor(mysql.cursors.DictCursor)
        try:
            cur.execute(query)
            affected = conn.affected_rows()
            conn.commit()
            data = cur.fetchall()
            if not data:
                if affected > 0:
                    data = ({'OK':'Columnas afectadas: %d' % affected},)
                elif cur.description and len(cur.description) > 0:
                    raw = {}
                    for i in cur.description:
                        raw[i[0]] = ''
                    data = (raw,)
                else:
                    data = ({'OK':'Consulta ejecutada con éxito.'},)
        except Exception as ex:
            return ({'ERROR': ex},)
        cur.close()
        conn.close()
        return data

#--- Forms

class DatabasesForm(forms.ModelForm):
    database = forms.CharField(label='Base de Datos')
    #links = forms.ModelMultipleChoiceField(label='Usuarios', queryset=None, required=False)
    class Meta:
        model = Databases
        fields = [ 'database' ]

class AddUsersForm(forms.ModelForm):
    user = forms.ModelChoiceField(label='Usuarios', queryset=None, required=False)
    class Meta:
        model = UsersDatabases
        fields = [ 'user' ]
        
class AddDatabasesForm(forms.ModelForm):
    database = forms.ModelChoiceField(label='Base de Datos', queryset=None, required=False)
    class Meta:
        model = UsersDatabases
        fields = [ 'database' ]

class UsersForm(forms.ModelForm):
    password = forms.CharField(label='Clave')
    #links = forms.ModelMultipleChoiceField(label='Usuarios', queryset=None, required=False)
    class Meta:
        model = Users
        fields = [ 'username', 'password' ]

#--- Triggers

@receiver(pre_save, sender=Users)
def save_user(sender, instance, **kwargs):
    sql = ""
    try:
        old = Users.objects.get(pk=instance.id)
        if old.username != instance.username:
            sql = settings.MARIADB_CHANGE_USER % {
                'old': old.username,
                'user': instance.username
            }
            execute(sql)
        sql = settings.MARIADB_CHANGE_PASS % {
            'user': instance.username,
            'pass': instance.password
        }
    except Users.DoesNotExist:
        sql = settings.MARIADB_CREATE_USER % {
            'user': instance.username,
            'pass': instance.password
        }
    execute(sql)

@receiver(post_save, sender=Databases)
def create_database(sender, instance, created, **kwargs):
    if created:
        sql = settings.MARIADB_CREATE_DB % {
            'name': instance.database
        }
        execute(sql)
        
@receiver(pre_save, sender=UsersDatabases)
def link_user(sender, instance, **kwargs):
    sql = settings.MARIADB_LINK_USER % {
        'user': instance.user.username,
        'name': instance.database.database
    }
    execute(sql)

@receiver(pre_delete, sender=UsersDatabases)
def unlink_user(sender, instance, **kwargs):
    sql = settings.MARIADB_UNLINK_USER % {
        'user': instance.user.username,
        'name': instance.database.database
    }
    execute(sql)

@receiver(pre_delete, sender=Databases)
def remove_database(sender, instance, **kwargs):
    sql = settings.MARIADB_REMOVE_DB % {
        'name': instance.database 
    }
    execute(sql)

@receiver(pre_delete, sender=Users)
def remove_user(sender, instance, **kwargs):
    sql = settings.MARIADB_REMOVE_USER % {
        'user': instance.username
    }
    execute(sql)
