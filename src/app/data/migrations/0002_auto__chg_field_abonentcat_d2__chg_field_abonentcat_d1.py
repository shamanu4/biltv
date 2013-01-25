# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AbonentCat.d2'
        db.alter_column('data_abonentcat', 'd2', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'AbonentCat.d1'
        db.alter_column('data_abonentcat', 'd1', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'AbonentCat.d2'
        raise RuntimeError("Cannot reverse this migration. 'AbonentCat.d2' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AbonentCat.d1'
        raise RuntimeError("Cannot reverse this migration. 'AbonentCat.d1' and its values cannot be restored.")

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
            'd1': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'd2': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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