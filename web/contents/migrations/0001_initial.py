# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContentBlock'
        db.create_table('contents_contentblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('content', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('_content_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('contents', ['ContentBlock'])

    def backwards(self, orm):
        # Deleting model 'ContentBlock'
        db.delete_table('contents_contentblock')

    models = {
        'contents.contentblock': {
            'Meta': {'object_name': 'ContentBlock'},
            '_content_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['contents']