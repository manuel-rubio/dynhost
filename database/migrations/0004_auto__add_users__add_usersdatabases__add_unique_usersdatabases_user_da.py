# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Users'
        db.create_table('database_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('accounts', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dbusers', to=orm['billing.Accounts'])),
        ))
        db.send_create_signal('database', ['Users'])

        # Adding model 'UsersDatabases'
        db.create_table('database_usersdatabases', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Users'])),
            ('database', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Databases'])),
        ))
        db.send_create_signal('database', ['UsersDatabases'])

        # Adding unique constraint on 'UsersDatabases', fields ['user', 'database']
        db.create_unique('database_usersdatabases', ['user_id', 'database_id'])

        # Deleting field 'Databases.username'
        db.delete_column('database_databases', 'username')

        # Deleting field 'Databases.password'
        db.delete_column('database_databases', 'password')


    def backwards(self, orm):
        
        # Removing unique constraint on 'UsersDatabases', fields ['user', 'database']
        db.delete_unique('database_usersdatabases', ['user_id', 'database_id'])

        # Deleting model 'Users'
        db.delete_table('database_users')

        # Deleting model 'UsersDatabases'
        db.delete_table('database_usersdatabases')

        # Adding field 'Databases.username'
        db.add_column('database_databases', 'username', self.gf('django.db.models.fields.CharField')(default=0, max_length=50, unique=True), keep_default=False)

        # Adding field 'Databases.password'
        db.add_column('database_databases', 'password', self.gf('django.db.models.fields.CharField')(default=0, max_length=50), keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'billing.accounts': {
            'Meta': {'object_name': 'Accounts'},
            'homedir': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_dns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_dynhost': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'limit_email_lists': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_mailbox': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_email_redirect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_ftp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_sql': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_web': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'limit_web_redirect': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paymonth': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'database.databases': {
            'Meta': {'object_name': 'Databases'},
            'accounts': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Accounts']"}),
            'database': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'database.users': {
            'Meta': {'object_name': 'Users'},
            'accounts': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dbusers'", 'to': "orm['billing.Accounts']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'database.usersdatabases': {
            'Meta': {'unique_together': "(('user', 'database'),)", 'object_name': 'UsersDatabases'},
            'database': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['database.Databases']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['database.Users']"})
        }
    }

    complete_apps = ['database']
