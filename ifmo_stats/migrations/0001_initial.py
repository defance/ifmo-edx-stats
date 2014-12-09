# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Grading'
        db.create_table('ifmo_stats_grading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('problem_number', self.gf('django.db.models.fields.IntegerField')()),
            ('deadline', self.gf('django.db.models.fields.DateField')(null=True)),
            ('min_grade', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('ifmo_stats', ['Grading'])


    def backwards(self, orm):
        # Deleting model 'Grading'
        db.delete_table('ifmo_stats_grading')


    models = {
        'ifmo_stats.grading': {
            'Meta': {'object_name': 'Grading'},
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'deadline': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_grade': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'problem_number': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['ifmo_stats']