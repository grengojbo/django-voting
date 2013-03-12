# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['user', 'content_type', 'object_id']
        db.delete_unique('votes', ['user_id', 'content_type_id', 'object_id'])

        # Deleting model 'Vote'
        db.delete_table('votes')


    def backwards(self, orm):
        # Adding model 'Vote'
        db.create_table('votes', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user', null=True, to=orm['auth.User'], blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('vote', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('voting', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['user', 'content_type', 'object_id']
        db.create_unique('votes', ['user_id', 'content_type_id', 'object_id'])


    models = {
        'voting.viewsobj': {
            'Meta': {'object_name': 'ViewsObj', 'db_table': "'votes_view'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'model_view': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['voting']