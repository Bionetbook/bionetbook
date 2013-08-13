# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Workflow', fields ['name']
        db.delete_unique('workflow_workflow', ['name'])

        # Deleting model 'WorkflowProtocol'
        db.delete_table('workflow_workflowprotocol')

        # Deleting field 'Workflow.description'
        db.delete_column('workflow_workflow', 'description')

        # Deleting field 'Workflow.duration'
        db.delete_column('workflow_workflow', 'duration')

        # Deleting field 'Workflow.owner'
        db.delete_column('workflow_workflow', 'owner_id')

        # Deleting field 'Workflow.author'
        db.delete_column('workflow_workflow', 'author_id')

        # Deleting field 'Workflow.note'
        db.delete_column('workflow_workflow', 'note')

        # Adding field 'Workflow.user'
        db.add_column('workflow_workflow', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Workflow.start'
        db.add_column('workflow_workflow', 'start',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 9, 0, 0)),
                      keep_default=False)

        # Adding field 'Workflow.data'
        db.add_column('workflow_workflow', 'data',
                      self.gf('jsonfield.fields.JSONField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'WorkflowProtocol'
        db.create_table('workflow_workflowprotocol', (
            ('protocol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['protocols.Protocol'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.Workflow'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('workflow', ['WorkflowProtocol'])

        # Adding field 'Workflow.description'
        db.add_column('workflow_workflow', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Workflow.duration'
        db.add_column('workflow_workflow', 'duration',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Workflow.owner'
        db.add_column('workflow_workflow', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='andrewmori', to=orm['organization.Organization']),
                      keep_default=False)

        # Adding field 'Workflow.author'
        db.add_column('workflow_workflow', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Workflow.note'
        db.add_column('workflow_workflow', 'note',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Workflow.user'
        db.delete_column('workflow_workflow', 'user_id')

        # Deleting field 'Workflow.start'
        db.delete_column('workflow_workflow', 'start')

        # Deleting field 'Workflow.data'
        db.delete_column('workflow_workflow', 'data')

        # Adding unique constraint on 'Workflow', fields ['name']
        db.create_unique('workflow_workflow', ['name'])


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'workflow.workflow': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Workflow'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['workflow']