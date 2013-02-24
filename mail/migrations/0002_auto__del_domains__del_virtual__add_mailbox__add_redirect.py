# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Domains'
        db.delete_table('mail_domains')

        # Deleting model 'Virtual'
        db.delete_table('mail_virtual')

        # Adding model 'Mailbox'
        db.create_table('mail_mailbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.TextField')(max_length=250, unique=True)),
            ('password', self.gf('django.db.models.fields.TextField')(max_length=32)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Domains'])),
        ))
        db.send_create_signal('mail', ['Mailbox'])

        # Adding model 'Redirect'
        db.create_table('mail_redirect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.TextField')(max_length=250, unique=True)),
            ('destin', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Domains'])),
        ))
        db.send_create_signal('mail', ['Redirect'])


    def backwards(self, orm):
        
        # Adding model 'Domains'
        db.create_table('mail_domains', (
            ('accounts', self.gf('django.db.models.fields.related.ForeignKey')(related_name='domains_email', to=orm['billing.Accounts'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dominio', self.gf('django.db.models.fields.TextField')(max_length=250, unique=True)),
        ))
        db.send_create_signal('mail', ['Domains'])

        # Adding model 'Virtual'
        db.create_table('mail_virtual', (
            ('origen', self.gf('django.db.models.fields.TextField')(max_length=250, unique=True)),
            ('accounts', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Accounts'])),
            ('destino', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mail', ['Virtual'])

        # Deleting model 'Mailbox'
        db.delete_table('mail_mailbox')

        # Deleting model 'Redirect'
        db.delete_table('mail_redirect')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'billing.accounts': {
            'Meta': {'object_name': 'Accounts'},
            'homedir': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_dns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_dynhost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_lists': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_mailbox': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_redirect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_ftp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_sql': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_web': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paymonth': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'billing.domains': {
            'Meta': {'object_name': 'Domains'},
            'accounts': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Accounts']"}),
            'dns_type': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '1'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email_type': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mail.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Domains']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.TextField', [], {'max_length': '32'}),
            'username': ('django.db.models.fields.TextField', [], {'max_length': '250', 'unique': 'True'})
        },
        'mail.redirect': {
            'Meta': {'object_name': 'Redirect'},
            'destin': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Domains']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {'max_length': '250', 'unique': 'True'})
        }
    }

    complete_apps = ['mail']
