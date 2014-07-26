# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Statement'
        db.create_table('statements_statement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, unique=True)),
            ('opcount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('remains', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('turnover', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('statements', ['Statement'])

        # Adding model 'Entry'
        db.create_table('statements_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('statement', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lines', to=orm['statements.Statement'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['statements.Entry'], null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='lines', null=True, to=orm['statements.Category'])),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date.today)),
            ('amount', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('egrpou', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('verbose_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('account_num', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('mfo', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('descr', self.gf('django.db.models.fields.TextField')()),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('statements', ['Entry'])

        # Adding model 'Category'
        db.create_table('statements_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('svc_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auto_processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.PaymentSource'], null=True, blank=True)),
        ))
        db.send_create_signal('statements', ['Category'])

        # Adding model 'Filter'
        db.create_table('statements_filter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['statements.Category'])),
            ('json', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('statements', ['Filter'])


    def backwards(self, orm):
        # Deleting model 'Statement'
        db.delete_table('statements_statement')

        # Deleting model 'Entry'
        db.delete_table('statements_entry')

        # Deleting model 'Category'
        db.delete_table('statements_category')

        # Deleting model 'Filter'
        db.delete_table('statements_filter')


    models = {
        'statements.category': {
            'Meta': {'object_name': 'Category'},
            'auto_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.PaymentSource']", 'null': 'True', 'blank': 'True'}),
            'svc_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'statements.entry': {
            'Meta': {'object_name': 'Entry'},
            'account_num': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lines'", 'null': 'True', 'to': "orm['statements.Category']"}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            'egrpou': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mfo': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['statements.Entry']", 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'statement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lines'", 'to': "orm['statements.Statement']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.date.today'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'statements.filter': {
            'Meta': {'object_name': 'Filter'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['statements.Category']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'statements.statement': {
            'Meta': {'object_name': 'Statement'},
            'day': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opcount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'remains': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'turnover': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tv.paymentsource': {
            'Meta': {'object_name': 'PaymentSource'},
            'descr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"})
        }
    }

    complete_apps = ['statements']