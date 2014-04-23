# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'judge_view'
        db.create_table(u'judge_supervise_judge_view', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'judge_supervise', ['judge_view'])


    def backwards(self, orm):
        # Deleting model 'judge_view'
        db.delete_table(u'judge_supervise_judge_view')


    models = {
        u'judge_supervise.judge_view': {
            'Meta': {'object_name': 'judge_view'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['judge_supervise']