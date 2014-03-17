# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContactInformation'
        db.create_table(u'contest_contactinformation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.IntegerField')(max_length=12)),
        ))
        db.send_create_signal(u'contest', ['ContactInformation'])

        # Adding model 'Contest'
        db.create_table(u'contest_contest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('teamreg_end_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2099, 1, 1, 0, 0))),
            ('css', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'contest', ['Contest'])

        # Adding M2M table for field contact_infos on 'Contest'
        m2m_table_name = db.shorten_name(u'contest_contest_contact_infos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contest', models.ForeignKey(orm[u'contest.contest'], null=False)),
            ('contactinformation', models.ForeignKey(orm[u'contest.contactinformation'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contest_id', 'contactinformation_id'])


        # Adding SortedM2M table for field links on 'Contest'
        db.create_table(u'contest_contest_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contest', models.ForeignKey(orm[u'contest.contest'], null=False)),
            ('link', models.ForeignKey(orm[u'contest.link'], null=False)),
            ('sort_value', models.IntegerField())
        ))
        db.create_unique(u'contest_contest_links', ['contest_id', 'link_id'])
        # Adding M2M table for field sponsors on 'Contest'
        m2m_table_name = db.shorten_name(u'contest_contest_sponsors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contest', models.ForeignKey(orm[u'contest.contest'], null=False)),
            ('sponsor', models.ForeignKey(orm[u'contest.sponsor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contest_id', 'sponsor_id'])

        # Adding model 'Link'
        db.create_table(u'contest_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('contestUrl', self.gf('django.db.models.fields.BooleanField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'contest', ['Link'])

        # Adding model 'Team'
        db.create_table(u'contest_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('onsite', self.gf('django.db.models.fields.BooleanField')()),
            ('leader', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leader', null=True, to=orm['userregistration.CustomUser'])),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contest', null=True, to=orm['contest.Contest'])),
            ('offsite', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'contest', ['Team'])

        # Adding M2M table for field members on 'Team'
        m2m_table_name = db.shorten_name(u'contest_team_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm[u'contest.team'], null=False)),
            ('customuser', models.ForeignKey(orm[u'userregistration.customuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['team_id', 'customuser_id'])

        # Adding model 'Invite'
        db.create_table(u'contest_invite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.Team'])),
            ('is_member', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'contest', ['Invite'])

        # Adding model 'Sponsor'
        db.create_table(u'contest_sponsor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Logo', max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
        ))
        db.send_create_signal(u'contest', ['Sponsor'])


    def backwards(self, orm):
        # Deleting model 'ContactInformation'
        db.delete_table(u'contest_contactinformation')

        # Deleting model 'Contest'
        db.delete_table(u'contest_contest')

        # Removing M2M table for field contact_infos on 'Contest'
        db.delete_table(db.shorten_name(u'contest_contest_contact_infos'))

        # Removing M2M table for field links on 'Contest'
        db.delete_table(db.shorten_name(u'contest_contest_links'))

        # Removing M2M table for field sponsors on 'Contest'
        db.delete_table(db.shorten_name(u'contest_contest_sponsors'))

        # Deleting model 'Link'
        db.delete_table(u'contest_link')

        # Deleting model 'Team'
        db.delete_table(u'contest_team')

        # Removing M2M table for field members on 'Team'
        db.delete_table(db.shorten_name(u'contest_team_members'))

        # Deleting model 'Invite'
        db.delete_table(u'contest_invite')

        # Deleting model 'Sponsor'
        db.delete_table(u'contest_sponsor')


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
            'phone': ('django.db.models.fields.IntegerField', [], {'max_length': '12'})
        },
        u'contest.contest': {
            'Meta': {'object_name': 'Contest'},
            'contact_infos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contest.ContactInformation']", 'symmetrical': 'False'}),
            'css': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('sortedm2m.fields.SortedManyToManyField', [], {'to': u"orm['contest.Link']", 'symmetrical': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contest.Sponsor']", 'symmetrical': 'False', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'teamreg_end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2099, 1, 1, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'contest.invite': {
            'Meta': {'object_name': 'Invite'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contest.Team']"})
        },
        u'contest.link': {
            'Meta': {'object_name': 'Link'},
            'contestUrl': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'offsite': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'onsite': ('django.db.models.fields.BooleanField', [], {})
        },
        u'userregistration.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'email_activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
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

    complete_apps = ['contest']