# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trunk'
        db.create_table('tv_trunk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.IntegerField')(default=1, unique=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cached', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('tv', ['Trunk'])

        # Adding model 'Channel'
        db.create_table('tv_channel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='channel name', max_length=32)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('tv', ['Channel'])

        # Adding model 'TrunkChannelRelationship'
        db.create_table('tv_trunkchannelrelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trunk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='slotlist', to=orm['tv.Trunk'])),
            ('slot', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.Channel'])),
            ('encoded', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tv', ['TrunkChannelRelationship'])

        # Adding unique constraint on 'TrunkChannelRelationship', fields ['trunk', 'channel']
        db.create_unique('tv_trunkchannelrelationship', ['trunk_id', 'channel_id'])

        # Adding model 'FeeIntervals'
        db.create_table('tv_feeintervals', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2100, 1, 1, 0, 0))),
        ))
        db.send_create_signal('tv', ['FeeIntervals'])

        # Adding model 'FeeType'
        db.create_table('tv_feetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='fee type', max_length=32)),
            ('ftype', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('allow_negative', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('proportional', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sum', self.gf('django.db.models.fields.FloatField')()),
            ('bonus', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('tv', ['FeeType'])

        # Adding model 'FeeRanges'
        db.create_table('tv_feeranges', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interval', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.FeeIntervals'])),
            ('fee_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ranges', to=orm['tv.FeeType'])),
            ('sum', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('tv', ['FeeRanges'])

        # Adding model 'FeeCustomRanges'
        db.create_table('tv_feecustomranges', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interval', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.FeeIntervals'])),
            ('fee_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customranges', to=orm['tv.FeeType'])),
            ('startday', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('endday', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sum', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('ret', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('tv', ['FeeCustomRanges'])

        # Adding model 'TariffPlan'
        db.create_table('tv_tariffplan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='tariff plan', max_length=64)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_restore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fallback_tp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.TariffPlan'], null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('tv', ['TariffPlan'])

        # Adding model 'TariffPlanChannelRelationship'
        db.create_table('tv_tariffplanchannelrelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.TariffPlan'])),
            ('chrel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.TrunkChannelRelationship'])),
        ))
        db.send_create_signal('tv', ['TariffPlanChannelRelationship'])

        # Adding unique constraint on 'TariffPlanChannelRelationship', fields ['tp', 'chrel']
        db.create_unique('tv_tariffplanchannelrelationship', ['tp_id', 'chrel_id'])

        # Adding model 'PaymentSource'
        db.create_table('tv_paymentsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='40')),
            ('descr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('tv', ['PaymentSource'])

        # Adding model 'PaymentRegister'
        db.create_table('tv_paymentregister', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.PaymentSource'])),
            ('total', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('end', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('bank', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('tv', ['PaymentRegister'])

        # Adding model 'PaymentRegisterStamp'
        db.create_table('tv_paymentregisterstamp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('register', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.PaymentRegister'])),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tv', ['PaymentRegisterStamp'])

        # Adding model 'Payment'
        db.create_table('tv_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments', to=orm['abon.Bill'])),
            ('sum', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('prev', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('maked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rolled_by', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tv.Payment'], unique=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.TextField')()),
            ('inner_descr', self.gf('django.db.models.fields.TextField')()),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.PaymentSource'], null=True, blank=True)),
            ('register', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='payments', null=True, to=orm['tv.PaymentRegister'])),
            ('bank_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('tv', ['Payment'])

        # Adding model 'Fee'
        db.create_table('tv_fee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fees', to=orm['abon.Bill'])),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.Card'], null=True, blank=True)),
            ('sum', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('prev', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('bonus', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('maked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rolled_by', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tv.Fee'], unique=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.TextField')()),
            ('inner_descr', self.gf('django.db.models.fields.TextField')()),
            ('tp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.TariffPlan'], null=True, blank=True)),
            ('fee_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.FeeType'], null=True, blank=True)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], null=True, blank=True)),
        ))
        db.send_create_signal('tv', ['Fee'])

        # Adding model 'TariffPlanFeeRelationship'
        db.create_table('tv_tariffplanfeerelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tp', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fees', to=orm['tv.TariffPlan'])),
            ('fee_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.FeeType'])),
        ))
        db.send_create_signal('tv', ['TariffPlanFeeRelationship'])

        # Adding unique constraint on 'TariffPlanFeeRelationship', fields ['tp', 'fee_type']
        db.create_unique('tv_tariffplanfeerelationship', ['tp_id', 'fee_type_id'])

        # Adding model 'CardHistory'
        db.create_table('tv_cardhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(related_name='service_log', to=orm['tv.Card'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='services_log', null=True, to=orm['abon.Abonent'])),
            ('action', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('oid', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('descr', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('tv', ['CardHistory'])

        # Adding model 'Card'
        db.create_table('tv_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('activated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cards', null=True, to=orm['abon.Abonent'])),
        ))
        db.send_create_signal('tv', ['Card'])

        # Adding model 'CardDigital'
        db.create_table('tv_carddigital', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.OneToOneField')(related_name='digital', unique=True, to=orm['tv.Card'])),
        ))
        db.send_create_signal('tv', ['CardDigital'])

        # Adding model 'CardService'
        db.create_table('tv_cardservice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', to=orm['tv.Card'])),
            ('tp', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', to=orm['tv.TariffPlan'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('activated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal('tv', ['CardService'])

        # Adding model 'RestoreService'
        db.create_table('tv_restoreservice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backup', to=orm['tv.CardService'])),
            ('tp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tv.TariffPlan'])),
            ('abonent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abon.Abonent'])),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='saved_services', to=orm['abon.Bill'])),
            ('create_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('restore_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('restored', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('feedback_sum', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('tv', ['RestoreService'])

        # Adding model 'FeesCalendar'
        db.create_table('tv_feescalendar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('tv', ['FeesCalendar'])

        # Adding model 'PromotionLink'
        db.create_table('tv_promotionlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tp', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='promotions', unique=True, null=True, to=orm['tv.TariffPlan'])),
            ('abills_tp_id', self.gf('django.db.models.fields.IntegerField')(db_column='abills_tp_id')),
        ))
        db.send_create_signal('tv', ['PromotionLink'])

        # Adding model 'PaymentAutoMake'
        db.create_table('tv_paymentautomake', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('register', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tv.PaymentRegister'], unique=True)),
        ))
        db.send_create_signal('tv', ['PaymentAutoMake'])


    def backwards(self, orm):
        # Removing unique constraint on 'TariffPlanFeeRelationship', fields ['tp', 'fee_type']
        db.delete_unique('tv_tariffplanfeerelationship', ['tp_id', 'fee_type_id'])

        # Removing unique constraint on 'TariffPlanChannelRelationship', fields ['tp', 'chrel']
        db.delete_unique('tv_tariffplanchannelrelationship', ['tp_id', 'chrel_id'])

        # Removing unique constraint on 'TrunkChannelRelationship', fields ['trunk', 'channel']
        db.delete_unique('tv_trunkchannelrelationship', ['trunk_id', 'channel_id'])

        # Deleting model 'Trunk'
        db.delete_table('tv_trunk')

        # Deleting model 'Channel'
        db.delete_table('tv_channel')

        # Deleting model 'TrunkChannelRelationship'
        db.delete_table('tv_trunkchannelrelationship')

        # Deleting model 'FeeIntervals'
        db.delete_table('tv_feeintervals')

        # Deleting model 'FeeType'
        db.delete_table('tv_feetype')

        # Deleting model 'FeeRanges'
        db.delete_table('tv_feeranges')

        # Deleting model 'FeeCustomRanges'
        db.delete_table('tv_feecustomranges')

        # Deleting model 'TariffPlan'
        db.delete_table('tv_tariffplan')

        # Deleting model 'TariffPlanChannelRelationship'
        db.delete_table('tv_tariffplanchannelrelationship')

        # Deleting model 'PaymentSource'
        db.delete_table('tv_paymentsource')

        # Deleting model 'PaymentRegister'
        db.delete_table('tv_paymentregister')

        # Deleting model 'PaymentRegisterStamp'
        db.delete_table('tv_paymentregisterstamp')

        # Deleting model 'Payment'
        db.delete_table('tv_payment')

        # Deleting model 'Fee'
        db.delete_table('tv_fee')

        # Deleting model 'TariffPlanFeeRelationship'
        db.delete_table('tv_tariffplanfeerelationship')

        # Deleting model 'CardHistory'
        db.delete_table('tv_cardhistory')

        # Deleting model 'Card'
        db.delete_table('tv_card')

        # Deleting model 'CardDigital'
        db.delete_table('tv_carddigital')

        # Deleting model 'CardService'
        db.delete_table('tv_cardservice')

        # Deleting model 'RestoreService'
        db.delete_table('tv_restoreservice')

        # Deleting model 'FeesCalendar'
        db.delete_table('tv_feescalendar')

        # Deleting model 'PromotionLink'
        db.delete_table('tv_promotionlink')

        # Deleting model 'PaymentAutoMake'
        db.delete_table('tv_paymentautomake')


    models = {
        'abon.abonent': {
            'Meta': {'ordering': "['sorting']", 'unique_together': "(('person', 'address'),)", 'object_name': 'Abonent'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abonents'", 'to': "orm['abon.Address']"}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abonents'", 'to': "orm['abon.Bill']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'extid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'unique': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'members'", 'to': "orm['abon.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abonents'", 'to': "orm['abon.Person']"}),
            'sorting': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'abon.address': {
            'Meta': {'ordering': "['sorting']", 'unique_together': "(('building', 'flat'),)", 'object_name': 'Address'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': "orm['abon.Building']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flat': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'override': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '20'}),
            'sorting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        'abon.bill': {
            'Meta': {'object_name': 'Bill'},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'abon.building': {
            'Meta': {'ordering': "['sorting']", 'unique_together': "(('street', 'house'),)", 'object_name': 'Building'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buildings'", 'to': "orm['abon.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sorting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buildings'", 'to': "orm['abon.Street']"})
        },
        'abon.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'abon.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'abon.house': {
            'Meta': {'ordering': "['num']", 'object_name': 'House'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'abon.person': {
            'Meta': {'ordering': "['sorting']", 'object_name': 'Person'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firstname': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            'middlename': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            'passport': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'registration': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 24, 0, 0)'}),
            'sorting': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'abon.street': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('city', 'name'),)", 'object_name': 'Street'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'streets'", 'to': "orm['abon.City']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'sorting': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'accounts.user': {
            'Meta': {'object_name': 'User', '_ormbases': ['auth.User']},
            'icq': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '0', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
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
        'tv.card': {
            'Meta': {'object_name': 'Card'},
            'activated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards'", 'null': 'True', 'to': "orm['abon.Abonent']"}),
            'tps': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tv.TariffPlan']", 'through': "orm['tv.CardService']", 'symmetrical': 'False'})
        },
        'tv.carddigital': {
            'Meta': {'object_name': 'CardDigital'},
            'card': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'digital'", 'unique': 'True', 'to': "orm['tv.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tv.cardhistory': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'CardHistory'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service_log'", 'to': "orm['tv.Card']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oid': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'services_log'", 'null': 'True', 'to': "orm['abon.Abonent']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'tv.cardservice': {
            'Meta': {'object_name': 'CardService'},
            'activated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': "orm['tv.Card']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': "orm['tv.TariffPlan']"})
        },
        'tv.channel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Channel'},
            'bound': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'channels'", 'to': "orm['tv.Trunk']", 'through': "orm['tv.TrunkChannelRelationship']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'channel name'", 'max_length': '32'})
        },
        'tv.fee': {
            'Meta': {'object_name': 'Fee'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']", 'null': 'True', 'blank': 'True'}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fees'", 'to': "orm['abon.Bill']"}),
            'bonus': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.Card']", 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            'fee_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.FeeType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inner_descr': ('django.db.models.fields.TextField', [], {}),
            'maked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prev': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rolled_by': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tv.Fee']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.TariffPlan']", 'null': 'True', 'blank': 'True'})
        },
        'tv.feecustomranges': {
            'Meta': {'ordering': "['startday']", 'object_name': 'FeeCustomRanges'},
            'endday': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'fee_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customranges'", 'to': "orm['tv.FeeType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.FeeIntervals']"}),
            'ret': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'startday': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'tv.feeintervals': {
            'Meta': {'object_name': 'FeeIntervals'},
            'end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2100, 1, 1, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'tv.feeranges': {
            'Meta': {'ordering': "('interval',)", 'object_name': 'FeeRanges'},
            'fee_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ranges'", 'to': "orm['tv.FeeType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.FeeIntervals']"}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'tv.feescalendar': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'FeesCalendar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        'tv.feetype': {
            'Meta': {'object_name': 'FeeType'},
            'allow_negative': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bonus': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ftype': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'fee type'", 'max_length': '32'}),
            'proportional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sum': ('django.db.models.fields.FloatField', [], {})
        },
        'tv.payment': {
            'Meta': {'object_name': 'Payment'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']", 'null': 'True', 'blank': 'True'}),
            'bank_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': "orm['abon.Bill']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descr': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inner_descr': ('django.db.models.fields.TextField', [], {}),
            'maked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prev': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'register': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'payments'", 'null': 'True', 'to': "orm['tv.PaymentRegister']"}),
            'rolled_by': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tv.Payment']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.PaymentSource']", 'null': 'True', 'blank': 'True'}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'tv.paymentautomake': {
            'Meta': {'object_name': 'PaymentAutoMake'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'register': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tv.PaymentRegister']", 'unique': 'True'})
        },
        'tv.paymentregister': {
            'Meta': {'object_name': 'PaymentRegister'},
            'bank': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.PaymentSource']"}),
            'start': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'total': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'tv.paymentregisterstamp': {
            'Meta': {'object_name': 'PaymentRegisterStamp'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'register': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.PaymentRegister']"})
        },
        'tv.paymentsource': {
            'Meta': {'object_name': 'PaymentSource'},
            'descr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'40'"})
        },
        'tv.promotionlink': {
            'Meta': {'object_name': 'PromotionLink'},
            'abills_tp_id': ('django.db.models.fields.IntegerField', [], {'db_column': "'abills_tp_id'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'promotions'", 'unique': 'True', 'null': 'True', 'to': "orm['tv.TariffPlan']"})
        },
        'tv.restoreservice': {
            'Meta': {'object_name': 'RestoreService'},
            'abonent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abon.Abonent']"}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'saved_services'", 'to': "orm['abon.Bill']"}),
            'create_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'feedback_sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'restore_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'restored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backup'", 'to': "orm['tv.CardService']"}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.TariffPlan']"})
        },
        'tv.tariffplan': {
            'Meta': {'object_name': 'TariffPlan'},
            'allow_restore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tps'", 'blank': 'True', 'through': "orm['tv.TariffPlanChannelRelationship']", 'to': "orm['tv.TrunkChannelRelationship']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fallback_tp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.TariffPlan']", 'null': 'True', 'blank': 'True'}),
            'fee_list': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tv.FeeType']", 'symmetrical': 'False', 'through': "orm['tv.TariffPlanFeeRelationship']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'tariff plan'", 'max_length': '64'})
        },
        'tv.tariffplanchannelrelationship': {
            'Meta': {'ordering': "('tp__name', 'chrel__channel__name')", 'unique_together': "(('tp', 'chrel'),)", 'object_name': 'TariffPlanChannelRelationship'},
            'chrel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.TrunkChannelRelationship']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.TariffPlan']"})
        },
        'tv.tariffplanfeerelationship': {
            'Meta': {'ordering': "('tp__name', 'fee_type__name')", 'unique_together': "(('tp', 'fee_type'),)", 'object_name': 'TariffPlanFeeRelationship'},
            'fee_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.FeeType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fees'", 'to': "orm['tv.TariffPlan']"})
        },
        'tv.trunk': {
            'Meta': {'ordering': "('num',)", 'object_name': 'Trunk'},
            'cached': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '1', 'unique': 'True'})
        },
        'tv.trunkchannelrelationship': {
            'Meta': {'ordering': "('trunk__num', 'slot')", 'unique_together': "(('trunk', 'channel'),)", 'object_name': 'TrunkChannelRelationship'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.Channel']"}),
            'encoded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trunk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slotlist'", 'to': "orm['tv.Trunk']"})
        }
    }

    complete_apps = ['tv']