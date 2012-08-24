# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'ContentBlock', fields ['name']
        db.create_unique('contents_contentblock', ['name'])

    def backwards(self, orm):
        # Removing unique constraint on 'ContentBlock', fields ['name']
        db.delete_unique('contents_contentblock', ['name'])

    models = {
        'contents.contentblock': {
            'Meta': {'object_name': 'ContentBlock'},
            '_content_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['contents']