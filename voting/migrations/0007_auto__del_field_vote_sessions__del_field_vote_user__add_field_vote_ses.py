# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['model_view', 'object_id', 'sessions']
        db.delete_unique('votes', ['model_view', 'object_id', 'sessions'])

        # Removing unique constraint on 'Vote', fields ['user', 'object_id', 'model_view']
        db.delete_unique('votes', ['user_id', 'object_id', 'model_view'])

        # Deleting field 'Vote.sessions'
        db.delete_column('votes', 'sessions')

        # Deleting field 'Vote.user'
        db.delete_column('votes', 'user_id')

        # Adding field 'Vote.sessions_hash'
        db.add_column('votes', 'sessions_hash',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Vote', fields ['sessions_hash', 'object_id', 'model_view']
        db.create_unique('votes', ['sessions_hash', 'object_id', 'model_view'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['sessions_hash', 'object_id', 'model_view']
        db.delete_unique('votes', ['sessions_hash', 'object_id', 'model_view'])

        # Adding field 'Vote.sessions'
        db.add_column('votes', 'sessions',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Vote.user'
        db.add_column('votes', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='user', null=True, to=orm['auth.User'], blank=True),
                      keep_default=False)

        # Deleting field 'Vote.sessions_hash'
        db.delete_column('votes', 'sessions_hash')

        # Adding unique constraint on 'Vote', fields ['user', 'object_id', 'model_view']
        db.create_unique('votes', ['user_id', 'object_id', 'model_view'])

        # Adding unique constraint on 'Vote', fields ['model_view', 'object_id', 'sessions']
        db.create_unique('votes', ['model_view', 'object_id', 'sessions'])


    models = {
        'voting.viewsobj': {
            'Meta': {'unique_together': "(('model_view', 'object_id'),)", 'object_name': 'ViewsObj', 'db_table': "'votes_view'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'model_view': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'voting.vote': {
            'Meta': {'unique_together': "(('sessions_hash', 'model_view', 'object_id'),)", 'object_name': 'Vote', 'db_table': "'votes'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'model_view': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sessions_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['voting']