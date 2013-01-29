# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('abon_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('abon', ['Group'])

        # Adding model 'Person'
        db.create_table('abon_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(default='?', max_length=40)),
            ('lastname', self.gf('django.db.models.fields.CharField')(default='?', max_length=40)),
            ('middlename', self.gf('django.db.models.fields.CharField')(default='?', max_length=40)),
            ('passport', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('registration', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 29, 0, 0))),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sorting', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('abon', ['Person'])

        # Adding model 'Contact'
        db.create_table('abon_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contacts', to=orm['abon.Person'])),
            ('ctype', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('abon', ['Contact'])

        # Adding model 'City'
        db.create_table('abon_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('abon', ['City'])

        # Adding model 'Street'
        db.create_table('abon_street', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='streets', to=orm['abon.City'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sorting', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('abon', ['Street'])

        # Adding unique constraint on 'Street', fields ['city', 'name']
        db.create_unique('abon_street', ['city_id', 'name'])

        # Adding model 'House'
        db.create_table('abon_house', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('abon', ['House'])

        # Adding model 'Building'
        db.create_table('abon_building', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buildings', to=orm['abon.Street'])),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buildings', to=orm['abon.House'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sorting', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, blank=True)),
        ))
        db.send_create_signal('abon', ['Building'])

        # Adding unique constraint on 'Building', fields ['street', 'house']
        db.create_unique('abon_building', ['street_id', 'house_id'])

        # Adding model 'Address'
        db.create_table('abon_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(related_name='addresses', to=orm['abon.Building'])),
            ('flat', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sorting', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, blank=True)),
            ('override', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('abon', ['Address'])

        # Adding unique constraint on 'Address', fields ['building', 'flat']
        db.create_unique('abon_address', ['building_id', 'flat'])

        # Adding model 'Bill'
        db.create_table('abon_bill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('balance', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('abon', ['Bill'])

        # Adding model 'Credit'
        db.create_table('abon_credit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credits', to=orm['abon.Bill'])),
            ('sum', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('valid_from', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('valid_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'], null=True, blank=True)),
        ))
        db.send_create_signal('abon', ['Credit'])

        # Adding model 'Abonent'
        db.create_table('abon_abonent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abonents', to=orm['abon.Person'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abonents', to=orm['abon.Address'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='members', to=orm['abon.Group'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sorting', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abonents', to=orm['abon.Bill'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('extid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, unique=True)),
        ))
        db.send_create_signal('abon', ['Abonent'])

        # Adding unique constraint on 'Abonent', fields ['person', 'address']
        db.create_unique('abon_abonent', ['person_id', 'address_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Abonent', fields ['person', 'address']
        db.delete_unique('abon_abonent', ['person_id', 'address_id'])

        # Removing unique constraint on 'Address', fields ['building', 'flat']
        db.delete_unique('abon_address', ['building_id', 'flat'])

        # Removing unique constraint on 'Building', fields ['street', 'house']
        db.delete_unique('abon_building', ['street_id', 'house_id'])

        # Removing unique constraint on 'Street', fields ['city', 'name']
        db.delete_unique('abon_street', ['city_id', 'name'])

        # Deleting model 'Group'
        db.delete_table('abon_group')

        # Deleting model 'Person'
        db.delete_table('abon_person')

        # Deleting model 'Contact'
        db.delete_table('abon_contact')

        # Deleting model 'City'
        db.delete_table('abon_city')

        # Deleting model 'Street'
        db.delete_table('abon_street')

        # Deleting model 'House'
        db.delete_table('abon_house')

        # Deleting model 'Building'
        db.delete_table('abon_building')

        # Deleting model 'Address'
        db.delete_table('abon_address')

        # Deleting model 'Bill'
        db.delete_table('abon_bill')

        # Deleting model 'Credit'
        db.delete_table('abon_credit')

        # Deleting model 'Abonent'
        db.delete_table('abon_abonent')


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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flat': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'override': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
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
        'abon.person': {
            'Meta': {'ordering': "['sorting']", 'object_name': 'Person'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firstname': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            'middlename': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '40'}),
            'passport': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'registration': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 29, 0, 0)'}),
            'sorting': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'abon.street': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('city', 'name'),)", 'object_name': 'Street'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'streets'", 'to': "orm['abon.City']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
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
        }
    }

    complete_apps = ['abon']