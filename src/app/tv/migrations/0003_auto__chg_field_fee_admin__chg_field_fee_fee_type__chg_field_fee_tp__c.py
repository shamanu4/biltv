# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Fee.admin'
        db.alter_column(u'tv_fee', 'admin_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Fee.fee_type'
        db.alter_column(u'tv_fee', 'fee_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.FeeType'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Fee.tp'
        db.alter_column(u'tv_fee', 'tp_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.TariffPlan'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Fee.card'
        db.alter_column(u'tv_fee', 'card_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.Card'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Payment.admin'
        db.alter_column(u'tv_payment', 'admin_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Payment.source'
        db.alter_column(u'tv_payment', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.PaymentSource'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Payment.register'
        db.alter_column(u'tv_payment', 'register_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['tv.PaymentRegister']))

    def backwards(self, orm):

        # Changing field 'Fee.admin'
        db.alter_column(u'tv_fee', 'admin_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], null=True))

        # Changing field 'Fee.fee_type'
        db.alter_column(u'tv_fee', 'fee_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.FeeType'], null=True))

        # Changing field 'Fee.tp'
        db.alter_column(u'tv_fee', 'tp_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.TariffPlan'], null=True))

        # Changing field 'Fee.card'
        db.alter_column(u'tv_fee', 'card_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.Card'], null=True))

        # Changing field 'Payment.admin'
        db.alter_column(u'tv_payment', 'admin_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], null=True))

        # Changing field 'Payment.source'
        db.alter_column(u'tv_payment', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.PaymentSource'], null=True))

        # Changing field 'Payment.register'
        db.alter_column(u'tv_payment', 'register_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['tv.PaymentRegister']))

    models = {
        u'abon.abonent': {
            'Meta': {'ordering': "['sorting']", 'unique_together': "(('person', 'address'),)", 'object_name': 'Abonent'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abonents'", 'to': u"orm['abon.Address']"}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abonents'", 'to': u"orm['abon.Bill']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'extid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'unique': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'members'", 'to': u"orm['abon.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abonents'", 'to': u"orm['abon.Person']"}),
            'sorting': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        u'abon.address': {
            'Meta': {'ordering': "['sorting']", 'unique_together': "(('building', 'flat'),)", 'object_name': 'Address'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': u"orm['abon.Building']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flat': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'override': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '20'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'sorting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        u'abon.bill': {
            'Meta': {'object_name': 'Bill'},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'balance2': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'abon.building': {
            'Meta': {'ordering': "['sorting']", 'unique_together': "(('street', 'house'),)", 'object_name': 'Building'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buildings'", 'to': u"orm['abon.House']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sorting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buildings'", 'to': u"orm['abon.Street']"})
        },
        u'abon.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        u'abon.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        u'abon.house': {
            'Meta': {'ordering': "['num']", 'object_name': 'House'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'abon.person': {
            'Meta': {'ordering': "['sorting']", 'object_name': 'Person'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firstname': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            'middlename': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            'passport': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'registration': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 11, 24, 0, 0)'}),
            'sorting': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'abon.street': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('city', 'name'),)", 'object_name': 'Street'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'streets'", 'to': u"orm['abon.City']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'sorting': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'accounts.user': {
            'Meta': {'object_name': 'User', '_ormbases': [u'auth.User']},
            'icq': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '0', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tv.card': {
            'Meta': {'object_name': 'Card'},
            'activated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards'", 'null': 'True', 'to': u"orm['abon.Abonent']"}),
            'tps': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tv.TariffPlan']", 'through': u"orm['tv.CardService']", 'symmetrical': 'False'})
        },
        u'tv.carddigital': {
            'Meta': {'object_name': 'CardDigital'},
            'card': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'digital'", 'unique': 'True', 'to': u"orm['tv.Card']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'tv.cardhistory': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'CardHistory'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service_log'", 'to': u"orm['tv.Card']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oid': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'services_log'", 'null': 'True', 'to': u"orm['abon.Abonent']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'tv.cardservice': {
            'Meta': {'object_name': 'CardService'},
            'activated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['tv.Card']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['tv.TariffPlan']"})
        },
        u'tv.channel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Channel'},
            'bound': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'channels'", 'to': u"orm['tv.Trunk']", 'through': u"orm['tv.TrunkChannelRelationship']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'channel name'", 'max_length': '32'})
        },
        u'tv.fee': {
            'Meta': {'object_name': 'Fee'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fees'", 'to': u"orm['abon.Bill']"}),
            'bonus': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.Card']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            'fee_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.FeeType']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inner_descr': ('django.db.models.fields.TextField', [], {}),
            'maked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prev': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rolled_by': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tv.Fee']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.TariffPlan']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'tv.feecustomranges': {
            'Meta': {'ordering': "['startday']", 'object_name': 'FeeCustomRanges'},
            'endday': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'fee_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customranges'", 'to': u"orm['tv.FeeType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.FeeIntervals']"}),
            'ret': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'startday': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'tv.feeintervals': {
            'Meta': {'object_name': 'FeeIntervals'},
            'end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2100, 1, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        u'tv.feeranges': {
            'Meta': {'ordering': "('interval',)", 'object_name': 'FeeRanges'},
            'fee_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ranges'", 'to': u"orm['tv.FeeType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.FeeIntervals']"}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'tv.feescalendar': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'FeesCalendar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        u'tv.feetype': {
            'Meta': {'object_name': 'FeeType'},
            'allow_negative': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bonus': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ftype': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'fee type'", 'max_length': '32'}),
            'proportional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sum': ('django.db.models.fields.FloatField', [], {})
        },
        u'tv.payment': {
            'Meta': {'object_name': 'Payment'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'bank_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': u"orm['abon.Bill']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inner_descr': ('django.db.models.fields.TextField', [], {}),
            'maked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prev': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'register': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'payments'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['tv.PaymentRegister']"}),
            'rolled_by': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tv.Payment']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.PaymentSource']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'tv.paymentautomake': {
            'Meta': {'object_name': 'PaymentAutoMake'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'register': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tv.PaymentRegister']", 'unique': 'True'})
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
        u'tv.paymentregisterstamp': {
            'Meta': {'object_name': 'PaymentRegisterStamp'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'register': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.PaymentRegister']"})
        },
        u'tv.paymentsource': {
            'Meta': {'object_name': 'PaymentSource'},
            'descr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"})
        },
        u'tv.promotionlink': {
            'Meta': {'object_name': 'PromotionLink'},
            'abills_tp_id': ('django.db.models.fields.IntegerField', [], {'db_column': "'abills_tp_id'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'promotions'", 'unique': 'True', 'null': 'True', 'to': u"orm['tv.TariffPlan']"})
        },
        u'tv.restoreservice': {
            'Meta': {'object_name': 'RestoreService'},
            'abonent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['abon.Abonent']"}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'saved_services'", 'to': u"orm['abon.Bill']"}),
            'create_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'feedback_sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'restore_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'restored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backup'", 'to': u"orm['tv.CardService']"}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.TariffPlan']"})
        },
        u'tv.tariffplan': {
            'Meta': {'object_name': 'TariffPlan'},
            'allow_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tps'", 'blank': 'True', 'through': u"orm['tv.TariffPlanChannelRelationship']", 'to': u"orm['tv.TrunkChannelRelationship']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fallback_tp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.TariffPlan']", 'null': 'True', 'blank': 'True'}),
            'fee_list': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tv.FeeType']", 'symmetrical': 'False', 'through': u"orm['tv.TariffPlanFeeRelationship']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'tariff plan'", 'max_length': '64'})
        },
        u'tv.tariffplanchannelrelationship': {
            'Meta': {'ordering': "('tp__name', 'chrel__channel__name')", 'unique_together': "(('tp', 'chrel'),)", 'object_name': 'TariffPlanChannelRelationship'},
            'chrel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.TrunkChannelRelationship']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.TariffPlan']"})
        },
        u'tv.tariffplanfeerelationship': {
            'Meta': {'ordering': "('tp__name', 'fee_type__name')", 'unique_together': "(('tp', 'fee_type'),)", 'object_name': 'TariffPlanFeeRelationship'},
            'fee_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.FeeType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fees'", 'to': u"orm['tv.TariffPlan']"})
        },
        u'tv.trunk': {
            'Meta': {'ordering': "('num',)", 'object_name': 'Trunk'},
            'cached': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '1', 'unique': 'True'})
        },
        u'tv.trunkchannelrelationship': {
            'Meta': {'ordering': "('trunk__num', 'slot')", 'unique_together': "(('trunk', 'channel'),)", 'object_name': 'TrunkChannelRelationship'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tv.Channel']"}),
            'encoded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trunk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slotlist'", 'to': u"orm['tv.Trunk']"})
        }
    }

    complete_apps = ['tv']