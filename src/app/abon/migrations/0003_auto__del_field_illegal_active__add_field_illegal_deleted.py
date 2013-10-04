# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Illegal.active'
        db.delete_column('abon_illegal', 'active')

        # Adding field 'Illegal.deleted'
        db.add_column('abon_illegal', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Illegal.active'
        db.add_column('abon_illegal', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'Illegal.deleted'
        db.delete_column('abon_illegal', 'deleted')


    models = {
        'abills.bill': {
            'Meta': {'object_name': 'Bill', 'db_table': "'bills'"},
            'company_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deposit': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sync': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'uid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'abills.company': {
            'Meta': {'ordering': "['name']", 'object_name': 'Company', 'db_table': "'companies'"},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'companies'", 'to': "orm['abills.Bill']"}),
            'credit': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'credit_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'abills.user': {
            'Meta': {'ordering': "['login']", 'object_name': 'User', 'db_table': "'users'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clients'", 'to': "orm['abills.Company']"}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'disable'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'uid'"}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_column': "'id'"})
        },
        'abon.abillslink': {
            'Meta': {'object_name': 'AbillsLink'},
            'abills': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abills.User']", 'unique': 'True'}),
            'abonent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abon.Abonent']", 'unique': 'True'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abills_links'", 'unique': 'True', 'to': "orm['tv.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abills_links'", 'unique': 'True', 'to': "orm['tv.CardService']"})
        },
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
        'abon.contact': {
            'Meta': {'object_name': 'Contact'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ctype': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['abon.Person']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'abon.credit': {
            'Meta': {'object_name': 'Credit'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credits'", 'to': "orm['abon.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']", 'null': 'True', 'blank': 'True'}),
            'sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'valid_from': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'valid_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
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
        'abon.illegal': {
            'Meta': {'object_name': 'Illegal'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'registration': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 4, 0, 0)'}),
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

    complete_apps = ['abon']