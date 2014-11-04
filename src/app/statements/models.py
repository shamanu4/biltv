# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from django.db import models
from datetime import date
from tv.models import PaymentRegister
import json


class Statement(models.Model):
    day = models.DateField(default=date.today, unique=True)
    opcount = models.PositiveIntegerField(default=0)
    remains = models.FloatField(default=0)
    turnover = models.FloatField(default=0)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.day.strftime("%Y-%m-%d")

    def process(self):
        for f in Filter.objects.filter(enabled=True):
            f.process(self)

    def save(self, *args, **kw):
        super(Statement, self).save(*args, **kw)
        self.process()

    def get_lines(self):
        return self.lines.filter(category__isnull=True)

    def get_total_amount(self):
        return self.get_lines().aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_processed_amount(self):
        return self.get_lines().filter(processed=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_unprocessed_amount(self):
        return self.get_total_amount() - self.get_processed_amount()

    def get_unregistered_unprocessed_amount(self):
        return self.get_unregistered_unprocessed_lines().aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_unregistered_unprocessed_lines(self):
        return self.get_lines().filter(processed=False, register__isnull=True)


    def get_cat_lines(self):
        return self.lines.filter(category__isnull=False)

    def get_cat_total_amount(self):
        return self.get_cat_lines().aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_cat_processed_amount(self):
        return self.get_cat_lines().filter(processed=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_cat_unprocessed_amount(self):
        return self.get_cat_total_amount() - self.get_cat_processed_amount()

    def get_cat_unregistered_unprocessed_amount(self):
        return self.get_cat_unregistered_unprocessed_lines().aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_cat_unregistered_unprocessed_lines(self):
        return self.get_cat_lines().filter(processed=False, register__isnull=True)

    def store_record(self):
        return {
            'day': self.day,
            'total': "%0.2f" % self.get_total_amount(),
            'unregistered': "%0.2f" % self.get_unregistered_unprocessed_amount(),
            'unprocessed': "%0.2f" % self.get_unprocessed_amount(),
            'total_cat': "%0.2f" % self.get_cat_total_amount(),
            'unregistered_cat': "%0.2f" % self.get_cat_unregistered_unprocessed_amount(),
            'unprocessed_cat': "%0.2f" % self.get_cat_unprocessed_amount()
        }


class Entry(models.Model):
    statement = models.ForeignKey("statements.Statement", related_name="lines")
    parent = models.ForeignKey("statements.Entry", blank=True, null=True)
    category = models.ForeignKey("statements.Category", blank=True, null=True, related_name="lines")
    pid = models.CharField(max_length=32)
    timestamp = models.DateTimeField(default=date.today)
    amount = models.FloatField(default=0.0)
    currency = models.CharField(max_length=10)
    egrpou = models.CharField(max_length=32)
    verbose_name = models.CharField(max_length=100)
    account_num = models.CharField(max_length=32)
    mfo = models.PositiveIntegerField()
    descr = models.TextField()
    processed = models.BooleanField(default=False)
    register = models.ForeignKey("tv.PaymentRegister", blank=True, null=True)

    def __unicode__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def store_record(self):
        return {
            'id': self.pk,
            'statement_id': self.statement.id,
            'parent_id': self.parent.id if self.parent else None,
            'category_id': self.category.id if self.parent else None,
            'pid': self.pid,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'amount': "%0.2f" % self.amount,
            'currency': self.currency,
            'egrpou': self.egrpou,
            'verbose_name': self.verbose_name,
            'account_num': self.account_num,
            'mfo': self.mfo,
            'descr': self.descr,
            'processed': self.processed,
            'register_id': self.register.id if self.register else None,
            'locked': self.processed or not self.register is None
        }


TYPE_UNDEF = 0
TYPE_INET = 1
TYPE_CATV = 2


CATEGORY_TYPES = (
    (TYPE_INET, u'INET'),
    (TYPE_CATV, u'CATV'),
    (TYPE_UNDEF, u'UNDEF'),
)


class Category(models.Model):
    name = models.CharField(max_length=64)
    svc_type = models.PositiveSmallIntegerField(choices=CATEGORY_TYPES)
    default = models.BooleanField(default=False)
    auto_processed = models.BooleanField(default=False)
    source = models.ForeignKey("tv.PaymentSource", blank=True, null=True, related_name="statements_categories")

    def __unicode__(self):
        return self.name

    def can_create_register(self, statement_id):
        return self.svc_type == TYPE_CATV and not self.auto_processed and (True if self.source else False) and \
               self.get_unregistered_unprocessed_lines(statement_id).count() > 0

    def get_lines(self, statement_id):
        return self.lines.filter(statement__id=statement_id)

    def get_total_amount(self, statement_id):
        return self.get_lines(statement_id).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_processed_amount(self, statement_id):
        return self.get_lines(statement_id).filter(processed=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_unprocessed_amount(self, statement_id):
        return self.get_total_amount(statement_id) - self.get_processed_amount(statement_id)

    def get_unregistered_unprocessed_amount(self, statement_id):
        return self.get_unregistered_unprocessed_lines(statement_id).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_unregistered_unprocessed_lines(self, statement_id):
        return self.get_lines(statement_id).filter(processed=False, register__isnull=True)

    def get_registry_start(self, statement_id):
        return self.get_unregistered_unprocessed_lines(statement_id).aggregate(models.Min('timestamp'))['timestamp__min'].date()

    def get_registry_end(self, statement_id):
        return self.get_unregistered_unprocessed_lines(statement_id).aggregate(models.Max('timestamp'))['timestamp__max'].date()

    def get_registry_bank(self, statement_id):
        lines = self.get_unregistered_unprocessed_lines(statement_id)
        if lines.count():
            return lines[0].statement.day
        else:
            return None

    def create_register(self, statement_id):
        """
            source = models.ForeignKey("tv.PaymentSource")
            total = models.FloatField(default=0)
            closed = models.BooleanField(default=False)
            start = models.DateField(blank=True,null=True)
            end = models.DateField(blank=True,null=True)
            bank = models.DateField(blank=True,null=True)
        """
        register = PaymentRegister.objects.create(source=self.source,
                                                  total=self.get_unregistered_unprocessed_amount(statement_id),
                                                  start=None,
                                                  end=None,
                                                  bank=self.get_registry_bank(statement_id),
                                                  )
        # register = PaymentRegister.objects.create(source=self.source,
        #                                           total=self.get_unregistered_unprocessed_amount(),
        #                                           start=self.get_registry_start(),
        #                                           end=self.get_registry_end(),
        #                                           bank=self.get_registry_bank(),
        #                                           )
        self.get_unregistered_unprocessed_lines().update(register=register)
        return register

    def store_record(self):
        return {
            'id': self.pk,
            'name': self.name,
            'svc_type': self.get_svc_type_display(),
            'source_id': self.source_id if self.source else None
        }

    def store_record_stats(self, statement_id):
        return {
            'id': self.pk,
            'name': self.name,
            'svc_type': self.get_svc_type_display(),
            'source_id': self.source_id if self.source else None,
            'can_create_register': self.can_create_register(statement_id),
            'total': "%0.2f" % self.get_total_amount(statement_id),
            'unregistered': "%0.2f" % self.get_unregistered_unprocessed_amount(statement_id),
            'unprocessed': "%0.2f" % self.get_unprocessed_amount(statement_id)
        }


class Filter(models.Model):
    name = models.CharField(max_length=64)
    enabled = models.BooleanField(default=False)
    category = models.ForeignKey("statements.Category")
    json = models.TextField()

    def __unicode__(self):
        return self.name

    @property
    def f(self):
        return json.loads(self.json)

    def process(self, statement):
        entries = statement.lines.filter(category__isnull=True, processed=False).filter(**self.f)
        for e in entries:
            e.category = self.category
            e.processed = self.category.auto_processed
            e.save()

