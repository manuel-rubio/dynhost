# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Payments.total'
        db.delete_column('billing_payments', 'total')

        # Changing field 'Payments.type'
        db.alter_column('billing_payments', 'type', self.gf('django.db.models.fields.CharField')(max_length=1))

        # Deleting field 'Accounts.limit_email'
        db.delete_column('billing_accounts', 'limit_email')

        # Adding field 'Accounts.limit_email_redirect'
        db.add_column('billing_accounts', 'limit_email_redirect', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Accounts.limit_email_mailbox'
        db.add_column('billing_accounts', 'limit_email_mailbox', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Accounts.limit_email_lists'
        db.add_column('billing_accounts', 'limit_email_lists', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Accounts.limit_dynhost'
        db.add_column('billing_accounts', 'limit_dynhost', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Domains.email_type'
        db.add_column('billing_domains', 'email_type', self.gf('django.db.models.fields.CharField')(default='N', max_length=1), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Payments.total'
        db.add_column('billing_payments', 'total', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Changing field 'Payments.type'
        db.alter_column('billing_payments', 'type', self.gf('django.db.models.fields.TextField')(max_length=255))

        # Adding field 'Accounts.limit_email'
        db.add_column('billing_accounts', 'limit_email', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'Accounts.limit_email_redirect'
        db.delete_column('billing_accounts', 'limit_email_redirect')

        # Deleting field 'Accounts.limit_email_mailbox'
        db.delete_column('billing_accounts', 'limit_email_mailbox')

        # Deleting field 'Accounts.limit_email_lists'
        db.delete_column('billing_accounts', 'limit_email_lists')

        # Deleting field 'Accounts.limit_dynhost'
        db.delete_column('billing_accounts', 'limit_dynhost')

        # Deleting field 'Domains.email_type'
        db.delete_column('billing_domains', 'email_type')


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
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'billing.payments': {
            'Meta': {'object_name': 'Payments'},
            'accounts': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Accounts']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['billing']
