# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'RedirectDynHost', fields ['dynhost', 'uri']
        db.delete_unique(u'web_redirectdynhost', ['dynhost_id', 'uri'])

        # Removing unique constraint on 'RedirectDynHost', fields ['dynhost', 'name']
        db.delete_unique(u'web_redirectdynhost', ['dynhost_id', 'name'])

        # Deleting field 'RedirectDynHost.dynhost'
        db.delete_column(u'web_redirectdynhost', 'dynhost_id')

        # Adding field 'RedirectDynHost.dynamic'
        db.add_column(u'web_redirectdynhost', 'dynamic',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='dynamic.Domains_RedirectDynHost', to=orm['dynamic.Domains']),
                      keep_default=False)

        # Adding unique constraint on 'RedirectDynHost', fields ['dynamic', 'name']
        db.create_unique(u'web_redirectdynhost', ['dynamic_id', 'name'])

        # Adding unique constraint on 'RedirectDynHost', fields ['dynamic', 'uri']
        db.create_unique(u'web_redirectdynhost', ['dynamic_id', 'uri'])


    def backwards(self, orm):
        # Removing unique constraint on 'RedirectDynHost', fields ['dynamic', 'uri']
        db.delete_unique(u'web_redirectdynhost', ['dynamic_id', 'uri'])

        # Removing unique constraint on 'RedirectDynHost', fields ['dynamic', 'name']
        db.delete_unique(u'web_redirectdynhost', ['dynamic_id', 'name'])


        # User chose to not deal with backwards NULL issues for 'RedirectDynHost.dynhost'
        raise RuntimeError("Cannot reverse this migration. 'RedirectDynHost.dynhost' and its values cannot be restored.")
        # Deleting field 'RedirectDynHost.dynamic'
        db.delete_column(u'web_redirectdynhost', 'dynamic_id')

        # Adding unique constraint on 'RedirectDynHost', fields ['dynhost', 'name']
        db.create_unique(u'web_redirectdynhost', ['dynhost_id', 'name'])

        # Adding unique constraint on 'RedirectDynHost', fields ['dynhost', 'uri']
        db.create_unique(u'web_redirectdynhost', ['dynhost_id', 'uri'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'billing.accounts': {
            'Meta': {'object_name': 'Accounts'},
            'currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '3'}),
            'homedir': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_dns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_dynhost': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'limit_email_lists': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_mailbox': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_redirect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_ftp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_sql': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_sql_users': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_web': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_web_redirect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paymonth': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'billing.domains': {
            'Meta': {'object_name': 'Domains'},
            'accounts': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.Accounts']"}),
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'email_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dns.records': {
            'Meta': {'object_name': 'Records'},
            'data': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.Domains']"}),
            'expire': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'host': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'mx_priority': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'refresh': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'resp_person': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'retry': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'serial': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'ttl': ('django.db.models.fields.IntegerField', [], {'default': '38400'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'dynamic.domains': {
            'Meta': {'object_name': 'Domains'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dns.Records']"}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'web.hosting': {
            'Meta': {'unique_together': "(('name', 'record'), ('uri', 'record'))", 'object_name': 'Hosting'},
            'directory': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True', 'max_length': '60'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dns.Records']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1'}),
            'uri': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'web.redirectdynhost': {
            'Meta': {'unique_together': "(('name', 'dynamic'), ('uri', 'dynamic'))", 'object_name': 'RedirectDynHost'},
            'dynamic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dynamic.Domains_RedirectDynHost'", 'to': u"orm['dynamic.Domains']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True', 'max_length': '60'}),
            'uri': ('django.db.models.fields.TextField', [], {'default': "'/'"}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['web']