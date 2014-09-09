# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from django.db import models
from datetime import date
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
            'locked': self.processed or self.register
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
    source = models.ForeignKey("tv.PaymentSource", blank=True, null=True)

    def __unicode__(self):
        return self.name

    def store_record(self):
        return {
            'id': self.pk,
            'name': self.name,
            'svc_type': self.get_svc_type_display()
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

