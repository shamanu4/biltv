# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'House'
        db.create_table('data_house', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('num', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('korp', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('letter', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('data', ['House'])

        # Adding model 'Street'
        db.create_table('data_street', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('data', ['Street'])

        # Adding model 'Address'
        db.create_table('data_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Street'])),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.House'])),
            ('loft', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('faceorder', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
            ('pereoform', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('data', ['Address'])

        # Adding model 'Person'
        db.create_table('data_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fio', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('passport', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('data', ['Person'])

        # Adding model 'Abonent'
        db.create_table('data_abonent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Address'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Person'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('data', ['Abonent'])

        # Adding model 'Category'
        db.create_table('data_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('data', ['Category'])

        # Adding model 'Tariff'
        db.create_table('data_tariff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Category'])),
            ('tar', self.gf('django.db.models.fields.FloatField')()),
            ('d1', self.gf('django.db.models.fields.DateField')()),
            ('d2', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('data', ['Tariff'])

        # Adding model 'AbonentCat'
        db.create_table('data_abonentcat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abonent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Abonent'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Category'])),
            ('d1', self.gf('django.db.models.fields.DateField')()),
            ('d2', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('data', ['AbonentCat'])

        # Adding model 'Proplata'
        db.create_table('data_proplata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abonent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Abonent'])),
            ('d1', self.gf('django.db.models.fields.DateField')()),
            ('d2', self.gf('django.db.models.fields.DateField')()),
            ('sum', self.gf('django.db.models.fields.FloatField')()),
            ('y', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('m', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('v', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('log', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('data', ['Proplata'])


    def backwards(self, orm):
        # Deleting model 'House'
        db.delete_table('data_house')

        # Deleting model 'Street'
        db.delete_table('data_street')

        # Deleting model 'Address'
        db.delete_table('data_address')

        # Deleting model 'Person'
        db.delete_table('data_person')

        # Deleting model 'Abonent'
        db.delete_table('data_abonent')

        # Deleting model 'Category'
        db.delete_table('data_category')

        # Deleting model 'Tariff'
        db.delete_table('data_tariff')

        # Deleting model 'AbonentCat'
        db.delete_table('data_abonentcat')

        # Deleting model 'Proplata'
        db.delete_table('data_proplata')


    models = {
        'data.abonent': {
            'Meta': {'object_name': 'Abonent'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Address']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Person']"})
        },
        'data.abonentcat': {
            'Meta': {'object_name': 'AbonentCat'},
            'abonent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Abonent']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Category']"}),
            'd1': ('django.db.models.fields.DateField', [], {}),
            'd2': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.address': {
            'Meta': {'object_name': 'Address'},
            'faceorder': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loft': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'pereoform': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Street']"}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        'data.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'data.house': {
            'Meta': {'object_name': 'House'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'korp': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'letter': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'num': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'data.person': {
            'Meta': {'object_name': 'Person'},
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passport': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'data.proplata': {
            'Meta': {'object_name': 'Proplata'},
            'abonent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Abonent']"}),
            'd1': ('django.db.models.fields.DateField', [], {}),
            'd2': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {}),
            'm': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sum': ('django.db.models.fields.FloatField', [], {}),
            'v': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'y': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'data.street': {
            'Meta': {'object_name': 'Street'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'data.tariff': {
            'Meta': {'object_name': 'Tariff'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Category']"}),
            'd1': ('django.db.models.fields.DateField', [], {}),
            'd2': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tar': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['data']