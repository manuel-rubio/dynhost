# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RedirectDynamic'
        db.create_table(u'mail_redirectdynamic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('destin', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('dynamic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynamic.Domains'])),
        ))
        db.send_create_signal(u'mail', ['RedirectDynamic'])

        # Adding unique constraint on 'RedirectDynamic', fields ['username', 'dynamic']
        db.create_unique(u'mail_redirectdynamic', ['username', 'dynamic_id'])

        # Adding model 'Redirect'
        db.create_table(u'mail_redirect', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.TextField')(max_length=50)),
            ('destin', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Domains'])),
        ))
        db.send_create_signal(u'mail', ['Redirect'])

        # Adding unique constraint on 'Redirect', fields ['username', 'domain']
        db.create_unique(u'mail_redirect', ['username', 'domain_id'])

        # Adding model 'Mailbox'
        db.create_table(u'mail_mailbox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.TextField')(unique=True, max_length=250)),
            ('password', self.gf('django.db.models.fields.TextField')(max_length=32)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Domains'])),
        ))
        db.send_create_signal(u'mail', ['Mailbox'])

        # Adding unique constraint on 'Mailbox', fields ['username', 'domain']
        db.create_unique(u'mail_mailbox', ['username', 'domain_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Mailbox', fields ['username', 'domain']
        db.delete_unique(u'mail_mailbox', ['username', 'domain_id'])

        # Removing unique constraint on 'Redirect', fields ['username', 'domain']
        db.delete_unique(u'mail_redirect', ['username', 'domain_id'])

        # Removing unique constraint on 'RedirectDynamic', fields ['username', 'dynamic']
        db.delete_unique(u'mail_redirectdynamic', ['username', 'dynamic_id'])

        # Deleting model 'RedirectDynamic'
        db.delete_table(u'mail_redirectdynamic')

        # Deleting model 'Redirect'
        db.delete_table(u'mail_redirect')

        # Deleting model 'Mailbox'
        db.delete_table(u'mail_mailbox')


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
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '3'}),
            'homedir': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_dns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_dynamic': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'limit_email_lists': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_mailbox': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_redirect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_ftp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_sql': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_sql_users': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_web': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_web_redirect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nic_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.NIC']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'billing.contracts': {
            'Meta': {'object_name': 'Contracts'},
            'accounts': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.Accounts']"}),
            'begins': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'concept': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            'ends': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'})
        },
        u'billing.domains': {
            'Meta': {'object_name': 'Domains'},
            'accounts': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.Accounts']"}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.Contracts']", 'null': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'email_type': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1', 'null': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Z'", 'max_length': '1'})
        },
        u'billing.nic': {
            'Meta': {'object_name': 'NIC'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'area': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.TextField', [], {}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'es'", 'max_length': '2'}),
            'email': ('django.db.models.fields.TextField', [], {}),
            'firstname': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'es'", 'max_length': '2'}),
            'legalForm': ('django.db.models.fields.CharField', [], {'default': "'individual'", 'max_length': '12'}),
            'legalName': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'legalNumber': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'nic': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'organization': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'password': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'phone': ('django.db.models.fields.TextField', [], {}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vat': ('django.db.models.fields.FloatField', [], {'default': '21.0'}),
            'zipCode': ('django.db.models.fields.TextField', [], {})
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
        u'mail.mailbox': {
            'Meta': {'unique_together': "(('username', 'domain'),)", 'object_name': 'Mailbox'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.Domains']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.TextField', [], {'max_length': '32'}),
            'username': ('django.db.models.fields.TextField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'mail.redirect': {
            'Meta': {'unique_together': "(('username', 'domain'),)", 'object_name': 'Redirect'},
            'destin': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.Domains']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {'max_length': '50'})
        },
        u'mail.redirectdynamic': {
            'Meta': {'unique_together': "(('username', 'dynamic'),)", 'object_name': 'RedirectDynHost'},
            'destin': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'dynamic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dynamic.Domains']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['mail']