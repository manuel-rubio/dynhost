# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Domains'
        db.create_table('dynhost_domains', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('dynhost', ['Domains'])


    def backwards(self, orm):
        
        # Deleting model 'Domains'
        db.delete_table('dynhost_domains')


    models = {
        'dynhost.domains': {
            'Meta': {'object_name': 'Domains', 'db_table': '\'dynhost_domains\''},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['dynhost']
