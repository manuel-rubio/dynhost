# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Records'
        db.create_table('dns_records', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.TextField')()),
            ('ttl', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('type', self.gf('django.db.models.fields.TextField')()),
            ('mx_priority', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('resp_person', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('serial', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('refresh', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('retry', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('expire', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('minimum', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Domains'])),
        ))
        db.send_create_signal('dns', ['Records'])


    def backwards(self, orm):
        
        # Deleting model 'Records'
        db.delete_table('dns_records')


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
            'homedir': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
        'dns.records': {
            'Meta': {'object_name': 'Records'},
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Domains']"}),
            'expire': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'host': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'mx_priority': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'refresh': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'resp_person': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'retry': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'serial': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'ttl': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['dns']
