# -*- coding: utf-8 -*-

from django.db import models
from logger.models import logging_postsave, logging_postdelete
from datetime import datetime


class Trunk(models.Model):

    num = models.IntegerField(default=1,unique=True)
    enabled = models.BooleanField(default = False)
    cached = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.num

    class Meta:
        ordering = ('num',)
        permissions = (
            ("manage_trunk", "Can manage trunks"),
        )

    @property
    def channel_mask(self):
        from functions import short_to_2byte_wrapped
        return short_to_2byte_wrapped(self.cached)
    
    @property
    def slots(self):
        res = []
        for i in range(1,17):
            try:
                ch = TrunkChannelRelationship.objects.get(trunk=self,slot=i)
            except TrunkChannelRelationship.DoesNotExist:
                ch = None
            res.append(ch)
        return res

    def rehash(self):
        hash = 0
        for i,slot in enumerate(self.slots):
            if not slot or slot.encoded:
                hash += (1<<i)
        self.cached=hash
        self.save(rehashed=True)

    def save(self, *args, **kwargs):
        from scrambler import ChannelQuery
        if not 'rehashed' in kwargs or not kwargs['rehashed']:            
            self.rehash()
        else:
            del kwargs['rehashed']
            super(Trunk, self).save(*args,**kwargs)
            q = ChannelQuery()
            q.run()



class Channel(models.Model):

    name = models.CharField(max_length=32,default='channel name')
    bound = models.ManyToManyField(Trunk, blank=True, null=True, related_name="channels", through='TrunkChannelRelationship')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        ordering = ('name',)
        permissions = (
            ("manage_channel", "Can manage channels"),
        )

models.signals.post_save.connect(logging_postsave, sender=Channel)
models.signals.post_delete.connect(logging_postdelete, sender=Channel)



class TrunkChannelRelationship(models.Model):
    SLOT_CHOICES = (
        (1, u'слот 1'),
        (2, u'слот 2'),
        (3, u'слот 3'),
        (4, u'слот 4'),
        (5, u'слот 5'),
        (6, u'слот 6'),
        (7, u'слот 7'),
        (8, u'слот 8'),
        (9, u'слот 9'),
        (10, u'слот 10'),
        (11, u'слот 11'),
        (12, u'слот 12'),
        (13, u'слот 13'),
        (14, u'слот 14'),
        (15, u'слот 15'),
        (16, u'слот 16'),
    )
    trunk = models.ForeignKey(Trunk,related_name='slotlist')
    slot = models.IntegerField(choices=SLOT_CHOICES, blank=True, null=True)
    channel = models.ForeignKey(Channel)
    encoded = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        if self.trunk:
            self.trunk.rehash()

    def __unicode__(self):
        return "%s [%s:%s]" % (self.channel.name,self.trunk.num,self.slot)

    class Meta:
        ordering = ('trunk__num','slot')
        unique_together = (('trunk', 'channel'),)


FEE_TYPE_DAILY=0
FEE_TYPE_WEEKLY=1
FEE_TYPE_MONTHLY=2
FEE_TYPE_YEARLY=3
FEE_TYPE_ONCE=4
FEE_TYPE_CUSTOM=5


class FeeType(models.Model):

    FEE_TYPES = (
        (FEE_TYPE_DAILY, u'daily'),
        (FEE_TYPE_WEEKLY, u'weekly'),
        (FEE_TYPE_MONTHLY, u'monthly'),
        (FEE_TYPE_YEARLY, u'yearly'),
        (FEE_TYPE_ONCE, u'once'),
        (FEE_TYPE_CUSTOM, u'custom'),
    )

    name = models.CharField(max_length=32,default='fee type')
    ftype = models.PositiveSmallIntegerField(choices=FEE_TYPES, default=FEE_TYPE_MONTHLY)
    allow_negative = models.BooleanField(default=True)
    sum = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'Снятие денег | %s (%s)' % (self.name, self.sum)

    def get_sum(self,date=None):
        if not self.ftype == FEE_TYPE_CUSTOM:
            return {'fee':self.sum(),'ret':0}

        if not date:
            date=datetime.now()

        day = date.day
        sum = 0
        ret = 0

        ranges = self.ranges.filter(startday<day).filter(endday>=day)
        for range in ranges:
            sum += range.sum
            ret += range.ret

        return {'fee':sum,'ret':ret}




class FeeCustomRanges(models.Model):

    fee_type = models.ForeignKey(FeeType, related_name='ranges')
    startday = models.PositiveSmallIntegerField()
    endday = models.PositiveSmallIntegerField()
    sum = models.FloatField(default=0)
    ret = models.FloatField(default=0)

    def __unicode__(self):
        return u'%s-%s: %s; %s;' % (self.startday, self.endday, self.sum, self.ret)



class TariffPlan(models.Model):

    name = models.CharField(max_length=64,default='tariff plan')
    channels = models.ManyToManyField(TrunkChannelRelationship,blank=True,related_name='tps',through='TariffPlanChannelRelationship')
    enabled = models.BooleanField(default=False)
    fees = models.ManyToManyField(FeeType,blank=True,through='TariffPlanFeeRelationship')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    def send(self):
        for service in self.services.all():
            service.card.send()

    def save(self, *args, **kwargs):
        print "saving tp..."
        super(self.__class__, self).save(*args, **kwargs)
        self.send()

    @property
    def bin_flags(self):
        res = []
        trunks = Trunk.objects.all()
        for t in trunks:
            res.extend([0,0])
        for ch in self.channels.all():
            shift = (ch.trunk.num-1)*2
            if ch.slot>8:
                shift+=1
                byte = ch.slot-9
            else:
                byte = ch.slot-1
            res[shift]=res[shift]|1<<byte
        return res



class TariffPlanChannelRelationship(models.Model):

    tp = models.ForeignKey(TariffPlan)
    chrel = models.ForeignKey(TrunkChannelRelationship, verbose_name=u'канал')

    def __unicode__(self):
        return "%s - %s [%s:%s]" % (self.tp.name, self.chrel.channel.name, self.chrel.trunk.num, self.chrel.slot)

    class Meta:
        ordering = ('tp__name','chrel__channel__name')
        unique_together = (('tp', 'chrel'),)



class Payment(models.Model):

    timestamp = models.DateTimeField(default=datetime.now)
    bill = models.ForeignKey("abon.Bill")
    sum = models.FloatField(default=0)
    prev = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    maked = models.BooleanField(default=False)
    descr = models.TextField()
    inner_descr = models.TextField()

    def __unicode__(self):
        return "%s" % self.sum

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)

    def make(self):
        self.prev = self.bill.balance
        self.save()
        self.bill.balance = self.bill.balance + self.sum
        self.bill.balance.save()
        self.maked=True

    def rollback(self):
        self.bill.balance = self.bill.balance - self.sum
        self.bill.balance.save()
        self.maked=False
        self.save()
        upper = self.__class__.objects.filter(bill=self.bill).filter(timestamp>self.timestamp).filter(pk>self.pk)
        for fee in upper:
            fee.prev = fee.prev - self.sum
            fee.save()



class TariffPlanFeeRelationship(models.Model):

    tp = models.ForeignKey(TariffPlan)
    fee_type = models.ForeignKey(FeeType)

    def __unicode__(self):
        return "%s - %s" % (self.tp.name, self.fee.name)

    def check_fee(self):
        from functions import date_formatter
        date = date_formatter()

        if self.fee_type == FEE_TYPE_ONCE:
            return self.make_fee()

        if self.fee_type == FEE_TYPE_DAILY:
            c = self.fees.filter(timestamp>date['day'])
            if c.count()>0:
                return False
            else:
                return self.make_fee()
        if self.fee_type == FEE_TYPE_WEEKLY:
            c = self.fees.filter(timestamp>date['week'])
            if c.count()>0:
                return False
            else:
                return self.make_fee()

        if self.fee_type == FEE_TYPE_MONTHLY:
            c = self.fees.filter(timestamp>date['month'])
            if c.count()>0:
                return False
            else:
                return self.make_fee()

        if self.fee_type == FEE_TYPE_YEARLY:
            c = self.fees.filter(timestamp>date['year'])
            if c.count()>0:
                return False
            else:
                return self.make_fee()


    def make_fee(self):
        fee = Fee()
        fee.tpfr = self
        fee.sum = self.fee_type
        return True

    class Meta:
        ordering = ('tp__name','fee_type__name')
        unique_together = (('tp', 'fee_type'),)


class Card(models.Model):

    num = models.IntegerField(unique=True)
    active = models.BooleanField(default=False)
    tps = models.ManyToManyField(TariffPlan, through='CardService')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    activated = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "%s" % self.num

    def send(self):
        print "sending..."
        from scrambler import UserQuery
        u = UserQuery(self.num)
        u.run()

    def save(self, *args, **kwargs):
        print "saving..."
        super(self.__class__, self).save(*args, **kwargs)
        self.send()

    def save_formset(self, *args, **kwargs):
        print "saving formset..."
        super(self.__class__, self).save_formset(*args, **kwargs)


    @property
    def bin_flags(self):
        from functions import byte_or
        res = []
        trunks = Trunk.objects.all()
        for t in trunks:
            res.extend([0,0])
        for service in self.services.all():
            if service.active:
                if res:
                    res = byte_or(res,service.tp.bin_flags)
                else:
                    res = service.tp.bin_flags
        return res

    @property
    def balance(self):
        return 1

    def activate(self):
        for service in self.services:
            service.activate()
        self.active=True
        self.activated=datetime.now()
        self.save()

    def deactivate(self):
        for service in self.services:
            service.deactivate()
        self.active=False
        self.save()





class CardService(models.Model):

    card = models.ForeignKey(Card,related_name='services')
    tp = models.ForeignKey(TariffPlan,related_name='services')
    active = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    activated = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "%s - %s" % (self.card.num,self.tp.name)

    def save(self, *args, **kwargs):
        print "saving service..."
        super(self.__class__, self).save(*args, **kwargs)
        self.card.send()

    def activate(self):
        self.active=True
        self.activated=datetime.now()
        self.save()

    def deactivate(self):
        self.active=False
        self.save()
