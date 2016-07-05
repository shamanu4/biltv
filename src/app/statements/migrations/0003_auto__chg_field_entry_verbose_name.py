# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Entry.verbose_name'
        db.alter_column(u'statements_entry', 'verbose_name', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Entry.verbose_name'
        db.alter_column(u'statements_entry', 'verbose_name', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'statements.category': {
            'Meta': {'object_name': 'Category'},
            'auto_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'statements_categories'", 'null': 'True', 'to': u"orm['tv.PaymentSource']"}),
            'svc_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'statements.entry': {
            'Meta': {'object_name': 'Entry'},
            'account_num': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lines'", 'null': 'True', 'to': u"orm['statements.Category']"}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            'egrpou': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mfo': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['statements.Entry']", 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'register': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.PaymentRegister']", 'null': 'True', 'blank': 'True'}),
            'statement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lines'", 'to': u"orm['statements.Statement']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.date.today'}),
            'verbose_name': ('django.db.models.fields.TextField', [], {})
        },
        u'statements.filter': {
            'Meta': {'object_name': 'Filter'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['statements.Category']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'statements.statement': {
            'Meta': {'object_name': 'Statement'},
            'day': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opcount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'remains': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'turnover': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'tv.paymentregister': {
            'Meta': {'object_name': 'PaymentRegister'},
            'bank': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.PaymentSource']"}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'tv.paymentsource': {
            'Meta': {'object_name': 'PaymentSource'},
            'descr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"})
        }
    }

    complete_apps = ['statements']