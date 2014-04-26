# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NIC'
        db.create_table(u'billing_nic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('firstname', self.gf('django.db.models.fields.TextField')()),
            ('password', self.gf('django.db.models.fields.TextField')(default='')),
            ('email', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('django.db.models.fields.TextField')()),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('city', self.gf('django.db.models.fields.TextField')()),
            ('area', self.gf('django.db.models.fields.TextField')()),
            ('zipCode', self.gf('django.db.models.fields.TextField')()),
            ('country', self.gf('django.db.models.fields.CharField')(default='es', max_length=2)),
            ('language', self.gf('django.db.models.fields.CharField')(default='es', max_length=2)),
            ('legalForm', self.gf('django.db.models.fields.CharField')(default='individual', max_length=12)),
            ('organization', self.gf('django.db.models.fields.TextField')(null=True)),
            ('legalName', self.gf('django.db.models.fields.TextField')(null=True)),
            ('legalNumber', self.gf('django.db.models.fields.TextField')(null=True)),
            ('vat', self.gf('django.db.models.fields.FloatField')(default=21.0)),
            ('nic', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('removed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'billing', ['NIC'])

        # Adding model 'Accounts'
        db.create_table(u'billing_accounts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('limit_web', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_web_redirect', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_sql', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_sql_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_dns', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_ftp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_email_redirect', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_email_mailbox', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_email_lists', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('limit_dynamic', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='EUR', max_length=3)),
            ('homedir', self.gf('django.db.models.fields.TextField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('nic_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.NIC'], null=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal(u'billing', ['Accounts'])

        # Adding model 'Contracts'
        db.create_table(u'billing_contracts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('accounts', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Accounts'])),
            ('begins', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('ends', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('concept', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('invoice_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'billing', ['Contracts'])

        # Adding model 'Payments'
        db.create_table(u'billing_payments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.CharField')(default='H', max_length=1)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Contracts'])),
        ))
        db.send_create_signal(u'billing', ['Payments'])

        # Adding model 'Domains'
        db.create_table(u'billing_domains', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('accounts', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Accounts'])),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Contracts'], null=True)),
            ('email_type', self.gf('django.db.models.fields.CharField')(default='R', max_length=1, null=True)),
            ('expires', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Z', max_length=1)),
        ))
        db.send_create_signal(u'billing', ['Domains'])


    def backwards(self, orm):
        # Deleting model 'NIC'
        db.delete_table(u'billing_nic')

        # Deleting model 'Accounts'
        db.delete_table(u'billing_accounts')

        # Deleting model 'Contracts'
        db.delete_table(u'billing_contracts')

        # Deleting model 'Payments'
        db.delete_table(u'billing_payments')

        # Deleting model 'Domains'
        db.delete_table(u'billing_domains')


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
        u'billing.payments': {
            'Meta': {'object_name': 'Payments'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.Contracts']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['billing']