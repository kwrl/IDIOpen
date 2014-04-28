# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Latex_Teamview'
        db.create_table(u'render_texdata_latex_teamview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latex_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'render_texdata', ['Latex_Teamview'])


    def backwards(self, orm):
        # Deleting model 'Latex_Teamview'
        db.delete_table(u'render_texdata_latex_teamview')


    models = {
        u'render_texdata.latex_teamview': {
            'Meta': {'object_name': 'Latex_Teamview'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latex_text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['render_texdata']