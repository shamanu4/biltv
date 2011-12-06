# -*- coding: utf-8 -*-
from datetime import date, datetime
from django.db import models

class Group(models.Model):

    name = models.CharField(max_length=40, unique=True)
    comment = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        
    def __unicode__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if not self.deleted:
            if self.members.filter(deleted=0).count() > 0:
                if 'recursive' in kwargs and kwargs['recursive']:
                    for member in self.members.filter(deleted=0):
                        member.delete(**kwargs)
                else:
                    return (self.members.filter(deleted=0).count(),"there are members in this group. cannot delete")
            else:
                self.deleted=1
                self.save()
                return (0,"deleted")



class Person(models.Model):

    firstname = models.CharField(max_length=40, default='?')
    lastname = models.CharField(max_length=40, default='?')
    middlename = models.CharField(max_length=40, default='?')
    passport = models.CharField(max_length=20, unique=True)
    registration = models.DateField(default=date.today())
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=100)

    class Meta:
        ordering = ['sorting']

    def __unicode__(self):
        return "%s (%s)" % (self.sorting,self.passport)

    def save(self, *args, **kwargs):
        from lib.functions import latinaze            
        self.passport=latinaze(self.passport)
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()
        self.middlename = self.middlename.capitalize()
        self.sorting = self.fio_short()
        for abonent in self.abonents.all():
            abonent.save()
        super(self.__class__, self).save(*args, **kwargs)

        

    def delete(self, *args, **kwargs):
        if self.abonents.count() > 0:
            return (self.members.count(),"there are abonent accounts for this person. cannot delete")
        else:
            self.deleted=1
            self.save()
            return (0,"deleted")

    def fio(self):
        return "%s %s %s" % (self.lastname, self.firstname, self.middlename)

    def fio_short(self):
        return "%s %s. %s." % (self.lastname, self.firstname[0], self.middlename[0])

    def initials(self):
        return "%s. %s. %s." % (self.lastname[0], self.firstname[0], self.middlename[0])

    def contact_add(self,type,value):
        c = Contact()
        c.person=self
        c.ctype=type
        c.value=value
        c.save()

    def contact_del(self,pk):
        try:
            c = self.contacts.get(pk=pk)
        except Contact.DoesNotExist:
            return False
        else:
            c.delete()
            return True

    def contact_edit(self,pk,type,value):
        try:
            c = self.contacts.get(pk=pk)
        except Contact.DoesNotExist:
            return False
        else:
            c.type=type
            c.value=value
            c.save()
            return True

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['person_id'] = self.pk
        obj['firstname'] = self.firstname
        obj['lastname'] = self.lastname
        obj['middlename'] = self.middlename
        obj['passport'] = self.passport
        return obj



class Contact(models.Model):

    CONTACT_TYPE_CHOICES = (
                           (0, u'Тел.'),
                           (1, u'E-mail'),
                           (2, u'ICQ'),
                           (3, u'Факс'),
                         )

    person = models.ForeignKey(Person,related_name='contacts')
    ctype = models.IntegerField(choices=CONTACT_TYPE_CHOICES, default=0)
    value = models.CharField(max_length=40)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (self.get_type_display(), self.value)



class City(models.Model):

    name = models.CharField(max_length=40, unique=True)
    label = models.CharField(blank=True, default='', max_length=40)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    """
    <label> must be ended with space. <label> and <street> contacted without delimeter.
    """
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(City, self).save(*args,**kwargs)

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['name'] = self.name
        obj['label'] = self.label
        obj['deleted'] = self.deleted
        obj['comment'] = self.comment
        return obj



class Street(models.Model):

    city = models.ForeignKey(City, default=1, related_name='streets')
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=2, unique=True)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(max_length=80)

    class Meta:
        ordering = ['name']
        unique_together = (("city", "name",),)

    def __unicode__(self):
        return "%s" % (self.sorting)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.sorting = "%s%s" % (self.city.label, self.name)
        for building in self.buildings.all():
            building.save()
        super(self.__class__, self).save(*args,**kwargs)

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['city'] = self.city.pk
        obj['name'] = self.sorting
        obj['code'] = self.code
        obj['deleted'] = self.deleted
        obj['comment'] = self.comment
        return obj



class House(models.Model):

    num = models.CharField(max_length=10, unique=True)
    code = models.CharField(max_length=7)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['num']
        
    def __unicode__(self):
        return self.num

    def save(self, *args, **kwargs):
        self.num = self.num.upper()
        self.code =  self.code + '0' * (5-len(self.code))
        for building in self.buildings.all():
            building.save()
        super(self.__class__, self).save(*args,**kwargs)

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['num'] = self.num
        obj['code'] = self.code
        obj['deleted'] = self.deleted
        obj['comment'] = self.comment
        return obj



class Building(models.Model):

    street = models.ForeignKey(Street, related_name='buildings')
    house = models.ForeignKey(House, related_name='buildings')
    code = models.CharField(max_length=2)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=100, unique=True)

    class Meta:
        ordering = ['sorting']
        unique_together = (("street", "house",),)

    def __unicode__(self):
        return "%s" % (self.sorting,)

    def get_or_create(self,street,house):
        try:
            building = Building.objects.get(street__sorting=street,house__num=house)
        except Building.DoesNotExist:
            s = Street.objects.get(sorting=street)
            h = House.objects.get(num=house)
            building = Building(street=s,house=h)
            building.save()
        return building

    def get_code(self):
        return "%s%s%s" % (self.street.code, self.house.code, self.code)

    def save(self, *args, **kwargs):
        self.sorting = "%s%s, %s" % (self.street.city.label, self.street.name, self.house.num)
        for address in self.addresses.all():
            address.save()
        super(self.__class__, self).save(*args,**kwargs)

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['street'] = self.street.id
        obj['house'] = self.house.id
        obj['comment'] = self.comment
        return obj



class Address(models.Model):

    building = models.ForeignKey(Building, related_name='addresses')
    flat = models.PositiveIntegerField()
    code = models.CharField(max_length=2)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=100, unique=True)
    override = models.CharField(max_length=20, unique=True, default="")

    class Meta:
        ordering = ['sorting']
        unique_together = (("building", "flat",),)

    def __unicode__(self):
        return "%s" % (self.sorting,)

    def get_or_create(self,building,flat,override=''):
        try:
            address = Address.objects.get(building=building,flat=flat)
        except Address.DoesNotExist:
            try:
                address = Address.objects.get(override=override)
                if address==self:
                    address.flat=flat
                    address.building=building
                else:
                    address = Address(building=building,flat=flat,override=override)
            except Address.DoesNotExist:
                address = Address(building=building,flat=flat,override=override)
        address.save()
        return address

    def get_code(self):
        if len(self.override)>0:
            return self.override
        return "%s%s%s" % (self.building.get_code(), '0' * (3-len(str(self.flat))) + str(self.flat), self.code)

    @property
    def ordernum(self):
        return self.get_code()

    def save(self, *args, **kwargs):        
        self.sorting = unicode("%s%s, %s, %s %s" % (self.building.street.city.label, self.building.street.name, self.building.house.num, u'кв.', self.flat))
        super(self.__class__, self).save(*args,**kwargs)

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['address_id'] = self.pk
        #obj['ext'] = self.code
        obj['ext'] = self.override
        obj['street'] = self.building.street.__unicode__()
        obj['house'] = self.building.house.__unicode__()
        obj['flat'] = self.flat
        return obj



class Bill(models.Model):

    balance = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    
    class Meta:
        permissions= (
            ("manage_bills", "Can manage bills"),
        )

    def __unicode__(self):
        return "%s" % self.balance

    @property
    def balance_int(self):
        return int(self.balance*100)

    @property
    def balance_rounded(self):
        return int(self.balance*100)/100.0

    @property
    def bin_balance(self):
        from lib.functions import int_to_4byte_wrapped
        return int_to_4byte_wrapped(self.balance_int)

    @property
    def bin_flags(self):        
        from tv.models import Trunk
        res = []
        trunks = Trunk.objects.all()
        for t in trunks:
            res.extend(t.user_mask)
        return res


class Abonent(models.Model):
    person = models.ForeignKey(Person, related_name='abonents')
    address = models.ForeignKey(Address, related_name='abonents')
    group = models.ForeignKey(Group, default=1, related_name='members')
    activated = models.DateTimeField(default=datetime.now)
    #deactivated = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=150)
    bill = models.ForeignKey(Bill, related_name="abonents")
    code = models.CharField(blank=False, max_length=20)
    confirmed = models.BooleanField(default=False)
    disabled = models.BooleanField(default=True)
    extid = models.PositiveIntegerField(default=0, unique=True)

    class Meta:
        ordering = ['sorting']
        unique_together = (("person", "address",),)
        permissions = (
            ("can_manage_disabled_abonents", "Can manage disabled abonents"),
            ("can_delete_abonents", "Can delete abonents (RPC)"),            
        )
        
    def __unicode__(self):
        return "%s" % (self.sorting,)

    @property
    def bin_id(self):
        from lib.functions import int_to_4byte_wrapped
        return int_to_4byte_wrapped(self.pk)

    @property
    def bin_card(self):
        from lib.functions import int_to_4byte_wrapped
        return int_to_4byte_wrapped((self.card_id-1)*2)
    
    @property
    def catv_card(self):
        card = (self.cards.filter(num=-self.pk) or [None])[0]
        return card
    
    @property
    def deactivated(self):
        from tv.models import CARD_SERVICE_DEACTIVATED
        if not self.disabled:
            return ''
        try:
            last_disabled = self.catv_card.service_log.filter(action=CARD_SERVICE_DEACTIVATED).latest('date')
        except:
            return ''
        else:
            return last_disabled.date
        
    
    def disable(self,date=None,descr=''):
        print "abonent disabling..."
        if not self.catv_card:            
            return False
        else:
            self.disabled=True
            self.save()
            print "abonent disabled..." 
            print date       
            return self.catv_card.deactivate(date,descr)
    
    def enable(self,date=None,descr=''):
        if not self.catv_card:            
            return False
        else:
            self.disabled=False
            self.save()
            return self.catv_card.activate(date,descr)
    
    def get_code(self):
        return "%s" % (self.address.get_code())

    def create_catv_card(self):
        from tv.models import Card, CardService, TariffPlan
        from settings import DEFAULT_CATV_TP_ID
        try:
            t = TariffPlan.objects.get(pk=DEFAULT_CATV_TP_ID)
        except TariffPlan.DoesNotExist:
            return False
        try:
            c = Card.objects.get(num=-self.pk)
        except Card.DoesNotExist:
            c = Card()
        else:
            c.detach()
        c.num = -self.pk
        c.owner=self
        c.save()
        s = CardService()
        s.card = c
        s.tp = t
        s.save()
        #c.activate(self.activated)
        return True

    def save(self, *args, **kwargs):
        try:
            self.bill
        except Bill.DoesNotExist:
            bill = Bill()
            bill.save()
            self.bill = bill
        self.code = self.get_code()
        self.sorting = "%s, [ %s ]" % (self.address.sorting, self.person.fio_short())
        super(self.__class__, self).save(*args,**kwargs)
        if len(self.cards.filter(num__lte=0))==0:
            print "creating CaTV card ..."
            self.create_catv_card()
            
    def make_fees(self,date):
        if self.deleted or self.disabled:
            return False
        for card in self.cards.all():
            card.make_fees(date)
        return True
    
    # WARNING! This method was used once during MIGRATION. Future uses RESTRICTED! This will cause  history DATA CORRUPT!  
    def import_catv_history(self):        
        from tv.models import CardHistory, CARD_SERVICE_ACTIVATED, CARD_SERVICE_DEACTIVATED
        self.catv_card.service_log.filter(timestamp__lt='2011-03-07').delete()
        print self
        if not self.catv_card:
            return False
        for interval in self.intervals.all():
            history = CardHistory(date=interval.start, card=self.catv_card, action=CARD_SERVICE_ACTIVATED, descr="%s/%s" % (interval.s1,interval.s2), oid=1)
            history.save()
            #print "    ACTIVATED: %s" % history.__unicode__()
            if interval.finish:
                history = CardHistory(date=interval.finish, card=self.catv_card, action=CARD_SERVICE_DEACTIVATED, descr="", oid=1)
                history.save()
                #print "    DEACTIVATED: %s" % history.__unicode__()
            
    def launch_hamster(self,countdown=True,debug=True):
        from lib.functions import date_formatter, add_months
        from tv.models import FeeType, Fee, Payment, TariffPlan
        from django.db.models import Max
        from time import sleep
        import gc
        
        gc.enable()
        
        if debug:
            print "Abonent %s" % self
            if countdown:
                print "    hamster ready to be launched."
                print "    all finance log will be recalculated."
                print "    use only when neccecary."
                print "    -------------------------------------"        
                print "    you have 5 sec to cancel... (Ctrl+C)"
                try:
                    sleep(1)
                    print "    4..."
                    sleep(1)
                    print "    3..."
                    sleep(1)
                    print "    2..."
                    sleep(1)
                    print "    1..."
                    sleep(1)
                    print "    hamster launched..."
                except KeyboardInterrupt:
                    print "    hamster launching cancelled..."
                    print "    Bye..."
                    return False
        
            print "        resetting all finance log..."
            
        self.bill.balance=0
        self.bill.save()
        Fee.objects.filter(bill=self.bill).delete()
        self.catv_card.service_log.all().delete()
        
        pp = Payment.objects.filter(bill=self.bill)
        for p in pp:
            p.maked=False
            if not p.bank_date:
                p.bank_date=p.timestamp.date()
            p.save()
        if debug:
            print "            Done..."
        
        catv = FeeType.objects.get(pk=5)
        catv_part = FeeType.objects.get(pk=1)
        tp = TariffPlan.objects.all()
        tp = tp[0]
        
        thismonth = date_formatter(date.today())['month'].date()
        nextmonth = date_formatter(add_months(thismonth,1))['month'].date()
                
        new = True
        prev_closing_fee = 0
        prev_closing_month = date(1970,1,1)
                
        for i in self.intervals.all():
            if debug:
                print "        processing interval %s-%s" % (i.start,i.finish)
            if not i.finish:
                i.finish = thismonth
            d = i.start    
            
            for service in self.catv_card.services.all():
                service.active=True
                service.save(sdate=d,descr="%s/%s" % (i.s1,i.s2))
                self.catv_card.active = True
                self.catv_card.save()
                self.disabled= False
                self.save()
                
            dd = date_formatter(add_months(d,1))['month'].date()
            
            if debug:
                print "            starting date %s" % d
            pp = Payment.objects.filter(bill=self.bill,maked=False,timestamp__lte=d)
            for p in pp:
                p.save()
                p.make()
            if d > date(2006,2,1) or not new:
                full = catv.get_sum(date=i.start)['fee']
                sum = catv_part.get_sum(date=i.start)['fee']
                if debug:
                    print "                full fee: %s" % full
                    print "                current fee: %s" % sum
                    print "                closing fee: %s" % prev_closing_fee
                    print "                closing month: %s" % prev_closing_month
                    print "                currnet month: %s" % date_formatter(d)['month'].date()
                    print sum+prev_closing_fee>full
                    print date_formatter(d)['month'].date() == prev_closing_month
                if sum+prev_closing_fee>full and date_formatter(d)['month'].date() == prev_closing_month:
                    print "                overpowered fee catched! fixed..."
                    f = Fee(bill=self.bill,card=self.catv_card,sum=full-prev_closing_fee,tp=tp,fee_type=catv_part,timestamp=d, inner_descr=u'Кабельное ТВ | подключение (!)')
                else: 
                    f = Fee(bill=self.bill,card=self.catv_card,sum=sum,tp=tp,fee_type=catv_part,timestamp=d, inner_descr=u'Кабельное ТВ | подключение')
                f.save()
                maxid = Fee.objects.aggregate(Max('id'))['id__max']
                f = Fee.objects.get(pk=maxid) 
                f.make()
            else:
                if debug:
                    print "                ignored because before 2006-02-01"
                f = Fee(bill=self.bill,card=self.catv_card,sum=0,tp=tp,fee_type=catv_part,timestamp=d, inner_descr=u'Кабельное ТВ | подключение (оплачено на месте)')
                f.save()
                maxid = Fee.objects.aggregate(Max('id'))['id__max']
                f = Fee.objects.get(pk=maxid)                 
                f.make()
            new = False                
            d = dd
            dd = date_formatter(add_months(d,1))['month'].date()
            pp = Payment.objects.filter(bill=self.bill,maked=False,timestamp__lte=d)
            for p in pp:
                p.save()
                p.make()
            
            
            while dd < i.finish or dd == nextmonth or dd == thismonth:
                if debug:
                    print "            processing date %s" % d
                sum = catv.get_sum(date=d)['fee']              
                f = Fee(bill=self.bill,card=self.catv_card,sum=sum,tp=tp,fee_type=catv,timestamp=d, inner_descr=u'Кабельное ТВ | абонплата')
                f.save()
                maxid = Fee.objects.aggregate(Max('id'))['id__max']
                f = Fee.objects.get(pk=maxid)                 
                f.make()                
                d = dd
                dd = date_formatter(add_months(d,1))['month'].date()
                pp = Payment.objects.filter(bill=self.bill,maked=False,timestamp__lte=d)
                for p in pp:
                    p.save()
                    p.make()
            
            
            if d < thismonth:
                if debug:
                    print "            closing date %s" % d
                full = catv.get_sum(date=i.finish)['fee']
                sum = full - catv_part.get_sum(date=i.finish)['ret']                
                prev_closing_fee = sum
                prev_closing_month = date_formatter(i.finish)['month'].date()
                f = Fee(bill=self.bill,card=self.catv_card,sum=sum,tp=tp,fee_type=catv,timestamp=i.finish, inner_descr=u'Кабельное ТВ | отключение')
                f.save()
                maxid = Fee.objects.aggregate(Max('id'))['id__max']
                f = Fee.objects.get(pk=maxid)                 
                f.make()
                
                for service in self.catv_card.services.all():
                    service.active=False
                    service.save(sdate=d,descr="")
                    self.catv_card.active = False
                    self.catv_card.save()
                    self.disabled= True
                    self.save()
            
            pp = Payment.objects.filter(bill=self.bill,maked=False,timestamp__lte=d)
            for p in pp:
                p.save()
                p.make()
        
        pp = Payment.objects.filter(bill=self.bill,maked=False)
        for p in pp:
            p.save()
            p.make()
                                       
        if debug:
            print "    hamster finished his work and stopped"
            print "    dont forget donate to WWF ;)"
            print "    Bye..."
        
        gc.collect()
        return True
    
    @classmethod
    def hamsters_swarm(cls,fa=0,fb=0,ts=0,tc=0,tr=0):
        import time
        import gc        
        from lib.functions import seconds2hhmmss
        #import thread
        
        gc.enable()
        
        #print "thread started..."        
        start = ts or int(time.time())            
        total = tc or cls.objects.all().count()        
        ready = tr or 0
        
        #print {'fa':fa,'fb':fb,'ts':start,'tc':total,'tr':ready}
        
        if (fa or fb) and (fa < fb):
            qs = cls.objects.all()[fa:fb]
        else:
            qs = cls.objects.all()
        for abonent in qs:
            abonent.launch_hamster(debug=False)
            ready+=1
            if ready%10 == 0:
                gc.collect()
                elapsed=int(time.time())-start
                progress=float("%.3f" % (ready/total*100))
                remain=int(elapsed*total/ready) 
                print "processed abonents %s/%s (%s%%) elapsed: %s remain: %s" % (ready,total,progress,seconds2hhmmss(elapsed),seconds2hhmmss(remain))
        
        #print "restarting thread..."
        return {'fa':fb,'fb':fb*2-fa,'ts':start,'tc':total,'tr':ready}
            
                
            
    def store_record(self):
        obj = {}
        obj['id'] = self.pk        
        obj['code'] = self.code
        obj['person'] = self.person.fio_short()
        obj['person__passport'] = self.person.passport
        obj['address'] = self.address.__unicode__()
        obj['comment'] = self.comment
        obj['confirmed'] = self.confirmed
        obj['activated'] = self.activated
        obj['deactivated'] = self.deactivated
        obj['disabled'] = self.disabled
        obj['fee'] = 25
        obj['bill__balance'] = self.bill.balance
        return obj



