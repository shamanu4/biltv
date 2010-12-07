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
            return {'fee':self.sum,'ret':0}

        if not date:
            date=datetime.now()

        day = date.day
        sum = 0
        ret = 0

        ranges = self.ranges.filter(startday__lte=day).filter(endday__gte=day)
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
    fee_list = models.ManyToManyField(FeeType,blank=True,through='TariffPlanFeeRelationship')
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
        self.maked=False
        self.save()
        r = Payment()
        r.sum = -self.sum
        r.inner_descr = "rollback payment id:%s" % self.pk
        r.save()
        r.make()



class Fee(models.Model):

    timestamp = models.DateTimeField(default=datetime.now)
    bill = models.ForeignKey("abon.Bill")
    card = models.ForeignKey("tv.Card")
    sum = models.FloatField(default=0)
    prev = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    maked = models.BooleanField(default=False)
    descr = models.TextField()
    inner_descr = models.TextField()
    tp = models.ForeignKey(TariffPlan, blank=True, null=True)
    fee_type = models.ForeignKey(FeeType, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.sum

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)

    def make(self):        
        self.prev = self.bill.balance
        if not self.fee_type.allow_negative:
            if self.sum > 0 and self.bill.balance - self.sum < 0:
                self.inner_descr = "Not enough money"
                self.save()
                return False
        self.bill.balance = self.bill.balance - self.sum
        self.bill.save()
        self.maked=True
        self.save()
        return True

    def rollback(self):
        self.maked=False
        self.save()
        r = Fee()
        r.sum = -self.sum
        r.inner_descr = "rollback fee id:%s" % self.pk
        r.save()
        r.make()



class TariffPlanFeeRelationship(models.Model):

    tp = models.ForeignKey(TariffPlan, related_name="fees")
    fee_type = models.ForeignKey(FeeType)

    def __unicode__(self):
        return "%s - %s" % (self.tp.name, self.fee_type.name)

    def check_fee(self,card):
        from functions import date_formatter
        date = date_formatter()
        print "checking fee ..."
        my_maked_fees = Fee.objects.filter(card__exact=card, tp__exact=self.tp, fee_type__exact=self.fee_type, maked__exact=True, deleted__exact=False)
        if not card.bill:
            return False
        if self.fee_type.ftype == FEE_TYPE_ONCE:
            return self.make_fee(card)

        if self.fee_type.ftype == FEE_TYPE_CUSTOM:
            return self.make_fee(card)

        if self.fee_type.ftype == FEE_TYPE_DAILY:
            c = my_maked_fees.filter(timestamp__gte=date['day'])
            if c.count()>0:
                return False
            else:
                return self.make_fee(card)

        if self.fee_type.ftype == FEE_TYPE_WEEKLY:
            c = my_maked_fees.filter(timestamp__gte=date['week'])
            if c.count()>0:
                return False
            else:
                return self.make_fee(card)

        if self.fee_type.ftype == FEE_TYPE_MONTHLY:
            c = my_maked_fees.filter(timestamp__gte=date['month'])
            if c.count()>0:
                return False
            else:
                return self.make_fee(card)

        if self.fee_type.ftype == FEE_TYPE_YEARLY:
            c = my_maked_fees.filter(timestamp__gte=date['year'])
            if c.count()>0:
                return False
            else:
                return self.make_fee(card)


    def make_fee(self,card):
        print "making fee ..."
        fee = Fee()
        fee.bill = card.bill
        fee.card = card
        fee.tp = self.tp
        fee.fee_type = self.fee_type
        fee.sum = self.fee_type.get_sum()['fee']
        fee.save()
        return fee.make()

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
    owner = models.ForeignKey("abon.Abonent", blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.num

    def send(self):
        print "sending..."
        from scrambler import UserQuery
        u = UserQuery(self.num)
        u.run()

    def save(self, *args, **kwargs):
        print "saving..."
        if not self.owner:            
            self.detach()
            self.deactivate()
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
    def bill(self):
        if self.owner:
            return self.owner.bill
        else:
            return None

    @property
    def balance(self):
        if self.bill:
            return self.bill.balance
        else:
            return None

    @property
    def balance_int(self):
        return int(self.balance*100)

    @property
    def balance_rounded(self):
        return int(self.balance*100)/100.0

    @property
    def bin_balance(self):
        from functions import int_to_4byte_wrapped
        return int_to_4byte_wrapped(self.balance_int)


    def activate(self):
        if not self.owner:
            return false
        for service in self.services.all():
            service.activate()
        self.active=True
        self.activated=datetime.now()
        self.save()
        return True

    def deactivate(self):
        for service in self.services.all():
            service.deactivate()
        self.active=False
        self.save()

    def detach(self):
        self.tps.all().delete()



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
        fees = self.tp.fees.all()
        print fees
        paid = True
        for fee in fees:
            paid = paid and fee.check_fee(self.card)
        if paid:
            self.active=True
            self.activated=datetime.now()
        else:
            self.deactivate()
            return False
        self.save()
        return True

    def deactivate(self):
        self.active=False
        self.save()
        return True
