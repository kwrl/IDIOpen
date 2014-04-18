# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'clarification_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('body', self.gf('django.db.models.fields.TextField')(max_length=355)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.Team'])),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.Contest'])),
        ))
        db.send_create_signal(u'clarification', ['Message'])

        # Adding model 'MessageAnswer'
        db.create_table(u'clarification_messageanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(default='Not Yet Answered', max_length=120)),
            ('body', self.gf('django.db.models.fields.TextField')(default='Not Yet Answered', max_length=355)),
            ('answared_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userregistration.CustomUser'], null=True, blank=True)),
            ('answared_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clarification.Message'])),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.Contest'])),
        ))
        db.send_create_signal(u'clarification', ['MessageAnswer'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'clarification_message')

        # Deleting model 'MessageAnswer'
        db.delete_table(u'clarification_messageanswer')
        

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
        u'clarification.message': {
            'Meta': {'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {'max_length': '355'}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contest.Contest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contest.Team']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'clarification.messageanswer': {
            'Meta': {'object_name': 'MessageAnswer'},
            'answared_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'answared_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userregistration.CustomUser']", 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'Not Yet Answered'", 'max_length': '355'}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contest.Contest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clarification.Message']"}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "'Not Yet Answered'", 'max_length': '120'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'contest.contactinformation': {
            'Meta': {'object_name': 'ContactInformation'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'contest.contest': {
            'Meta': {'object_name': 'Contest'},
            'contact_infos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contest.ContactInformation']", 'null': 'True', 'symmetrical': 'False'}),
            'css': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('sortedm2m.fields.SortedManyToManyField', [], {'to': u"orm['contest.Link']", 'symmetrical': 'False'}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'penalty_constant': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contest.Sponsor']", 'symmetrical': 'False', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'teamreg_end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'contest.link': {
            'Meta': {'object_name': 'Link'},
            'contestUrl': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'separator': ('django.db.models.fields.BooleanField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contest.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Logo'", 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'contest.team': {
            'Meta': {'object_name': 'Team'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contest'", 'null': 'True', 'to': u"orm['contest.Contest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leader'", 'null': 'True', 'to': u"orm['userregistration.CustomUser']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'members'", 'symmetrical': 'False', 'to': u"orm['userregistration.CustomUser']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'offsite': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'onsite': ('django.db.models.fields.BooleanField', [], {})
        },
        u'userregistration.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'email_activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '1'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skill_level': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '4'}),
            'temp_email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['clarification']