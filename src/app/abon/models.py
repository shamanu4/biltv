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

    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    middlename = models.CharField(max_length=40)
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
    deactivated = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=150)
    bill = models.ForeignKey(Bill, related_name="abonents")
    code = models.CharField(blank=False, max_length=20)
    confirmed = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    extid = models.PositiveIntegerField(default=0, unique=True)

    class Meta:
        ordering = ['sorting']
        unique_together = (("person", "address",),)

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
        return (self.cards.filter(num=-self.pk) or [None])[0]
    
    def disable(self,date=None,descr=''):
        print "abonent disabling..."
        if not self.catv_card:            
            return False
        else:
            self.disabled=True
            self.save()
            print "abonent disabled..."        
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
        c.activate(self.activated)
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
            history = CardHistory(timestamp=interval.start, card=self.catv_card, action=CARD_SERVICE_ACTIVATED, descr="%s/%s" % (interval.s1,interval.s2), oid=0)
            history.save()
            print "    ACTIVATED: %s" % history.__unicode__()
            if interval.finish:
                history = CardHistory(timestamp=interval.finish, card=self.catv_card, action=CARD_SERVICE_DEACTIVATED, descr="", oid=0)
                history.save()
                print "    DEACTIVATED: %s" % history.__unicode__()
            
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
        return obj



