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
        self.fio_set()
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()
        self.middlename = self.middlename.capitalize()
        self.sorting = self.fio_short()
        for abonent in self.abonents.all():
            abonent.save()
        super(self.__class__, self).save(*args, **kwargs)

    def fio_set(self):
        import re
        r = re.compile("(\S+)[\ |\.]{1}(\S+)[\ |\.]{1}([^\ \.]+)[\ |\.]?.*")
        m = r.match(self.lastname)
        if m:
            self.lastname = m.group(1)
            self.firstname = m.group(2)
            self.middlename = m.group(3)

    def delete(self, *args, **kwargs):
        if self.abonents.count() > 0:
            return (self.members.count(),"there are abonent accounts for this person. cannot delete")
        else:
            self.deleted=1
            self.save()
            return (0,"deleted")

    @classmethod
    def get_or_create_cls(cls,fio,passport):
        from lib.functions import latinaze
        passport = latinaze(passport)
        try:
            person = cls.objects.get(passport=passport)
        except cls.DoesNotExist:
            person = cls(passport=passport,lastname=fio)
            person.save()
        return person

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
    code = models.CharField(max_length=4, unique=True)
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
    code = models.CharField(max_length=11)
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

    @classmethod
    def get_or_create_cls(cls,street,house):
        try:
            building =cls.objects.get(street__sorting=street,house__num=house)
        except cls.DoesNotExist:
            s = Street.objects.get(sorting=street)
            h = House.objects.get(num=house)
            building = cls(street=s,house=h)
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
        obj['street_name'] = self.street.name
        obj['house_num'] = self.house.num
        obj['comment'] = self.comment
        return obj

ALPHA_INDEX = [u'', u'\u0430', u'\u0431', u'\u0432', u'\u0433', u'\u0434', u'\u0435', u'\u0454', u'\u0436', u'\u0437',
               u'\u0438', u'\u0456', u'\u0457', u'\u0439', u'\u043a', u'\u043b', u'\u043c', u'\u043d', u'\u043e',
               u'\u043f', u'\u0440', u'\u0441', u'\u0442', u'\u0443', u'\u0444', u'\u0445', u'\u0446', u'\u0447',
               u'\u0448', u'\u0449', u'\u044e', u'\u044f', u'\u044c']

class Address(models.Model):

    FLAT_EXT_TYPE_CHOICES = (
        (0, u'none'),
        (1, u'slash'),
        (2, u'alpha'),
        (3, u'invalid'),
    )

    building = models.ForeignKey(Building, related_name='addresses')
    flat = models.PositiveIntegerField()
    code = models.CharField(max_length=20)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=100, unique=True)
    override = models.CharField(max_length=20,blank=True, null=True)
    flat_ext = models.PositiveIntegerField(blank=True, default=0)
    flat_ext_type = models.PositiveSmallIntegerField(choices=FLAT_EXT_TYPE_CHOICES, default=0)

    class Meta:
        ordering = ['sorting']
        unique_together = (("building", "flat", "flat_ext", "flat_ext_type"),)

    def __unicode__(self):
        return "%s" % (self.sorting,)

    def get_or_create(self,building,flat,override=''):
        flat, flat_ext, flat_ext_type = self.clean_flat_other(flat)
        try:
            address = Address.objects.get(building=building, flat=flat, flat_ext=flat_ext, flat_ext_type=flat_ext_type)
        except Address.DoesNotExist:
            address = Address(building=building,flat=flat, flat_ext=flat_ext, flat_ext_type=flat_ext_type)
        address.save()
        return address

    @classmethod
    def get_or_create_cls(cls,street,house,flat,override=0):
        flat, flat_ext, flat_ext_type = cls.clean_flat_other(flat)
        print "cls"
        print (flat, flat_ext, flat_ext_type)
        building = Building.get_or_create_cls(street,house)
        if not override:
            override=0
        try:
            address = Address.objects.get(building=building, flat=flat, flat_ext=flat_ext, flat_ext_type=flat_ext_type)
        except Address.DoesNotExist:
            address = Address(building=building,flat=flat, flat_ext=flat_ext, flat_ext_type=flat_ext_type)
        address.save()
        return address

    def get_code(self):
        if self.override and len(self.override)>0:
            return self.override
        return "%s%s%s" % (self.building.get_code(), '0' * (3-len(str(self.flat))) + str(self.flat), self.code)

    @property
    def ordernum(self):
        return self.get_code()

    @property
    def generated(self):
        return "%s%s" % (self.building.get_code(), '0' * (3-len(str(self.flat))) + str(self.flat)) + str(self.flat_ext)

    @staticmethod
    def clean_flat_other(flat_other):

        flat_other = unicode(flat_other).lower()
        flat = 0
        flat_ext = 0
        flat_ext_type = 0

        import re
        flat_clean = re.compile("^(\d{1,3})$")
        flat_slash = re.compile("^(\d{1,3})\/(\d{1,2})$")
        flat_alpha = re.compile("^(\d{1,3})(\w{1})$", re.U)
        if flat_clean.match(flat_other):
            m = flat_clean.match(flat_other)
            flat = m.group(1)
        elif flat_slash.match(flat_other):
            m = flat_slash.match(flat_other)
            flat = m.group(1)
            flat_ext = m.group(2)
            flat_ext_type = 1
        elif flat_alpha.match(flat_other):
            m = flat_alpha.match(flat_other)
            flat = m.group(1)
            try:
                flat_ext = ALPHA_INDEX.index(unicode(m.group(2)).lower())
                flat_ext_type = 2
            except:
                flat_ext = 0
                flat_ext_type = 3
        else:
            flat = 0
            flat_ext = 0
            flat_ext_type = 3
        return flat, flat_ext, flat_ext_type

    @property
    def flat_extended(self):
        if self.flat_ext_type == 0:
            return self.flat
        if self.flat_ext_type == 1:
            return "%s/%s" % (self.flat,self.flat_ext)
        if self.flat_ext_type == 2:
            return "%s%s" % (self.flat,ALPHA_INDEX[self.flat_ext])
        if self.flat_ext_type == 3:
            return "invalid format"

    def save(self, *args, **kwargs):
        if self.flat_ext_type ==3:
            raise Exception, "Invalid flat data format. Accepting: [digit]{1,3} or [digit]{1,3}[alpha]{1} or [digit]{1,3}/[digit]{1,2}"
        if self.override == 0:
            self.override = self.get_code()
        self.sorting = unicode("%s%s, %s, %s %s" % (self.building.street.city.label, self.building.street.name, self.building.house.num, u'кв.', self.flat_extended))
        super(self.__class__, self).save(*args,**kwargs)

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['address_id'] = self.pk
        #obj['ext'] = self.code
        obj['ext'] = self.override
        obj['street'] = self.building.street.__unicode__()
        obj['house'] = self.building.house.__unicode__()
        obj['flat'] = self.flat_extended
        return obj



class Bill(models.Model):

    balance = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)

    class Meta:
        permissions= (
            ("manage_bills", "Can manage bills"),
        )

    def __unicode__(self):
        return "%s" % self.balance_get()

    def get_credit(self,dt=None):
        from django.db.models import Sum
        import settings
        if not dt:
            dt = date.today()
        credit = self.credits.filter(valid_from__lte=dt,valid_until__gte=dt).aggregate(total=Sum('sum'))['total'] or 0
        if credit < settings.ALL_USERS_CREDIT:
            return settings.ALL_USERS_CREDIT
        return credit


    def balance_get_wo_credit(self):
        from lib.functions import round1000
        from django.db.models import Sum
        balance = self.balance + (self.payments.filter(maked__exact=False,deleted__exact=False,rolled_by__exact=None).aggregate(total=Sum('sum'))['total'] or 0)
        return round1000(balance)


    def balance_get(self):
        return self.balance_get_wo_credit()+self.get_credit()

    @property
    def balance_int(self):
        return int(self.balance_get()*100)

    @property
    def balance_rounded(self):
        return int(self.balance_get()*100)/100.0

    @property
    def balance_wo_credit(self):
        return self.balance_get_wo_credit()

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

    def balance_on_date(self,date=date.today()):
        from itertools import chain
        from operator import attrgetter
        from tv.models import Fee,Payment
        balance = 0
        print "balance on date %s " % date
        for op in sorted(
                list(chain(self.fees.filter(deleted=False,maked=True,rolled_by=None,timestamp__lt=date),
                    self.payments.filter(deleted=False,rolled_by=None,bank_date__lt=date),)),
                    key=attrgetter('sort')):
            if type(op)==Fee:
                balance-=op.sum
            if type(op)==Payment:
                balance+=op.sum
        print balance
        return balance

    def operations_log(self,last_operation_date=None):
        from itertools import chain
        from operator import attrgetter
        if last_operation_date:
            return sorted(
                list(chain(self.fees.filter(deleted=False,maked=True,rolled_by=None,timestamp__gte=last_operation_date),
                    self.payments.filter(deleted=False,rolled_by=None,bank_date__gte=last_operation_date),)),
                    key=attrgetter('sort'))
        else:
            return sorted(
                list(chain(self.fees.filter(deleted=False,maked=True,rolled_by=None),
                    self.payments.filter(deleted=False,rolled_by=None),)),
                    key=attrgetter('sort'))

    def fix_operations_log(self,last_operation_date=None):
        from tv.models import Fee,Payment
        if not last_operation_date:
            balance = 0
        else:
            balance = self.balance_on_date(last_operation_date)
        print "fix_operations_log starting balance: %s" % balance
        for op in self.operations_log(last_operation_date):
            print "%s %s %s" % (type(op),op,balance)
            op.prev=balance
            op.save()
            if type(op)==Fee:
                balance-=op.sum
            if type(op)==Payment:
                balance+=op.sum

    def checksum(self):
        calculated = self.balance_on_date(date=date(2999, 12, 31))
        current = self.balance_wo_credit
        if not calculated == current:
            try:
                report = "bill checksum mismatch abonent_id:%s  bill_id:%s current:%s counted:%s" % (self.abonents.get().pk,self.pk,current,calculated)
                print report
                subject, from_email, to = 'BilTV checksum error', 'biltv@it-tim.net', 'mm@it-tim.net'
                text_content = report
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.send()
            except:
                pass

    def restore_tp_check(self):
        pass
#        if self.balance_get()>=0 and self.saved_services.filter(restored=False).count():
#            for s in self.saved_services.all():
#                print "try to restore service %s" % s
#                if s.restore():
#                    print "    restored"
#                else:
#                    print "    failed"


    def save(self,*args,**kwargs):
        if 'last_operation_date' in kwargs:
            last_operation_date = kwargs['last_operation_date']
            del kwargs['last_operation_date']
        else:
            last_operation_date = None
        super(self.__class__, self).save(*args, **kwargs)
        print "bill recalc from %s" % last_operation_date
        self.fix_operations_log(last_operation_date)
        self.checksum()
        self.restore_tp_check()


class Credit(models.Model):
    bill = models.ForeignKey(Bill,related_name="credits")
    sum = models.FloatField(default=0)
    valid_from = models.DateField(default=date.today)
    valid_until = models.DateField(blank=True,null=True)
    #valid = models.BooleanField(default=True)
    manager = models.ForeignKey("accounts.User",blank=True,null=True)

    def __unicode__(self):
        return "%s" % self.sum

    def save(self, *args, **kwargs):
        from tv.models import CardService
        super(self.__class__, self).save(*args, **kwargs)
        self.bill.restore_tp_check()
        for fee in self.bill.fees.filter(maked__exact=False,deleted__exact=False,rolled_by__exact=None):
            print fee
            if not fee.card or not fee.tp:
                fee.make()
            else:
                try:
                    cs = CardService.objects.get(card=fee.card,tp=fee.tp)
                except CardService.DoesNotExist:
                    pass
                else:
                    cs.activate(activated=fee.timestamp.date())
                    fee.delete()
                    #cs.activate()
    @property
    def valid(self):
        from datetime import date
        today=date.today()
        return self.valid_from<=today and self.valid_until>=today

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['bill'] = self.bill.pk
        obj['sum'] = self.sum
        obj['valid_from'] = self.valid_from
        obj['valid_until'] = self.valid_until
        obj['valid'] = self.valid
        try:
            obj['manager'] = self.manager.username
        except:
            obj['manager'] = 'System'
        return obj



class Abonent(models.Model):
    person = models.ForeignKey(Person, related_name='abonents')
    address = models.ForeignKey(Address, related_name='abonents')
    group = models.ForeignKey(Group, default=1, related_name='members')
    #activated = models.DateTimeField(default=datetime.now)
    #deactivated = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=150)
    bill = models.ForeignKey(Bill, related_name="abonents")
    code = models.CharField(blank=False, max_length=20)
    confirmed = models.BooleanField(default=False)
    disabled = models.BooleanField(default=True)
    extid = models.PositiveIntegerField(default=0)

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

    @property
    def activated(self):
        from tv.models import CARD_SERVICE_ACTIVATED
        try:
            last_disabled = self.catv_card.service_log.filter(action=CARD_SERVICE_ACTIVATED).latest('date')
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

    def was_active(self,date):
        from tv.models import CARD_SERVICE_ACTIVATED, CARD_SERVICE_DEACTIVATED
        last_activated_qs = self.catv_card.service_log.filter(action=CARD_SERVICE_ACTIVATED,date__lte=date).order_by('-date')
        last_deactivated_qs = self.catv_card.service_log.filter(action=CARD_SERVICE_DEACTIVATED,date__lte=date).order_by('-date')
        if not last_activated_qs.count():
            return False
        if not last_deactivated_qs.count():
            return True

        last_activated = last_activated_qs[0]
        last_deactivated = last_deactivated_qs[0]

        if last_activated.date < last_deactivated.date:
            return False
        if last_activated.date > last_deactivated.date:
            return True
        if last_activated.timestamp < last_deactivated.timestamp:
            return False
        if last_activated.timestamp > last_deactivated.timestamp:
            return True
        if last_activated.pk < last_deactivated.pk:
            return False
        else:
            return True

#    def abills_get_user(self,login):
#        from abills.models import User
#        try:
#            return User.objects.get(login__exact=login)
#        except:
#            return None
#
#    def check_abills_bill_link(self,card,cs):
#        print "checking link %s %s %s" % (self,card,cs)
#        u = self.abills_get_user(cs.extra)
#        if u:
#            AbillsLink.check(self,u,card,cs)

#    # WARNING! This method was used once during MIGRATION. Future uses RESTRICTED! This will cause  history DATA CORRUPT!
#    def import_catv_history(self):
#        from tv.models import CardHistory, CARD_SERVICE_ACTIVATED, CARD_SERVICE_DEACTIVATED
#        self.catv_card.service_log.filter(timestamp__lt='2011-03-07').delete()
#        print self
#        if not self.catv_card:
#            return False
#        for interval in self.intervals.all():
#            history = CardHistory(date=interval.start, card=self.catv_card, action=CARD_SERVICE_ACTIVATED, descr="%s/%s" % (interval.s1,interval.s2), oid=1)
#            history.save()
#            #print "    ACTIVATED: %s" % history.__unicode__()
#            if interval.finish:
#                history = CardHistory(date=interval.finish, card=self.catv_card, action=CARD_SERVICE_DEACTIVATED, descr="", oid=1)
#                history.save()
#                #print "    DEACTIVATED: %s" % history.__unicode__()

#    def launch_hamster(self,countdown=True,debug=True):
#        from lib.functions import date_formatter, add_months
#        from tv.models import FeeType, Fee, Payment, TariffPlan
#        from django.db.models import Max
#        from time import sleep
#        import gc
#
#        gc.enable()
#
#        if debug:
#            print "Abonent %s" % self
#            if countdown:
#                print "    hamster ready to be launched."
#                print "    all finance log will be recalculated."
#                print "    use only when neccecary."
#                print "    -------------------------------------"
#                print "    you have 5 sec to cancel... (Ctrl+C)"
#                try:
#                    sleep(1)
#                    print "    4..."
#                    sleep(1)
#                    print "    3..."
#                    sleep(1)
#                    print "    2..."
#                    sleep(1)
#                    print "    1..."
#                    sleep(1)
#                    print "    hamster launched..."
#                except KeyboardInterrupt:
#                    print "    hamster launching cancelled..."
#                    print "    Bye..."
#                    return False
#
#            print "        resetting all finance log..."
#
#        self.bill.balance=0
#        self.bill.save()
#        Fee.objects.filter(bill=self.bill).delete()
#        self.catv_card.service_log.all().delete()
#
#        pp = Payment.objects.filter(bill=self.bill)
#        for p in pp:
#            p.maked=False
#            if not p.bank_date:
#                p.bank_date=p.timestamp.date()
#            p.save()
#        if debug:
#            print "            Done..."
#
#        catv = FeeType.objects.get(pk=5)
#        catv_part = FeeType.objects.get(pk=1)
#        tp = TariffPlan.objects.all()
#        tp = tp[0]
#
#        thismonth = date_formatter(date.today())['month'].date()
#        nextmonth = date_formatter(add_months(thismonth,1))['month'].date()
#
#        new = True
#        prev_closing_fee = 0
#        prev_closing_month = date(1970,1,1)
#
#        for i in self.intervals.all():
#            if debug:
#                print "        processing interval %s-%s" % (i.start,i.finish)
#            if not i.finish:
#                i.finish = thismonth
#            d = i.start
#
#            for service in self.catv_card.services.all():
#                service.active=True
#                service.save(sdate=d,descr="%s/%s" % (i.s1,i.s2))
#                self.catv_card.active = True
#                self.catv_card.save()
#                self.disabled= False
#                self.save()
#
#            dd = date_formatter(add_months(d,1))['month'].date()
#
#            if debug:
#                print "            starting date %s" % d
#            pp = Payment.objects.filter(bill=self.bill,maked=False,bank_date__lte=d)
#            for p in pp:
#                p.save()
#                p.make()
#            if d > date(2006,2,1) or not new:
#                full = catv.get_sum(date=i.start)['fee']
#                sum = catv_part.get_sum(date=i.start)['fee']
#                if debug:
#                    print "                full fee: %s" % full
#                    print "                current fee: %s" % sum
#                    print "                closing fee: %s" % prev_closing_fee
#                    print "                closing month: %s" % prev_closing_month
#                    print "                currnet month: %s" % date_formatter(d)['month'].date()
#                    print sum+prev_closing_fee>full
#                    print date_formatter(d)['month'].date() == prev_closing_month
#                if sum+prev_closing_fee>full and date_formatter(d)['month'].date() == prev_closing_month:
#                    print "                overpowered fee catched! fixed..."
#                    f = Fee(bill=self.bill,card=self.catv_card,sum=full-prev_closing_fee,tp=tp,fee_type=catv_part,timestamp=d, inner_descr=u'Кабельное ТВ | подключение (!)')
#                else:
#                    f = Fee(bill=self.bill,card=self.catv_card,sum=sum,tp=tp,fee_type=catv_part,timestamp=d, inner_descr=u'Кабельное ТВ | подключение')
#                f.save()
#                maxid = Fee.objects.aggregate(Max('id'))['id__max']
#                f = Fee.objects.get(pk=maxid)
#                f.make()
#            else:
#                if debug:
#                    print "                ignored because before 2006-02-01"
#                f = Fee(bill=self.bill,card=self.catv_card,sum=0,tp=tp,fee_type=catv_part,timestamp=d, inner_descr=u'Кабельное ТВ | подключение (оплачено на месте)')
#                f.save()
#                maxid = Fee.objects.aggregate(Max('id'))['id__max']
#                f = Fee.objects.get(pk=maxid)
#                f.make()
#            new = False
#            d = dd
#            dd = date_formatter(add_months(d,1))['month'].date()
#            pp = Payment.objects.filter(bill=self.bill,maked=False,bank_date__lte=d)
#            for p in pp:
#                p.save()
#                p.make()
#
#
#            while dd < i.finish or dd == nextmonth or dd == thismonth:
#                if debug:
#                    print "            processing date %s" % d
#                sum = catv.get_sum(date=d)['fee']
#                f = Fee(bill=self.bill,card=self.catv_card,sum=sum,tp=tp,fee_type=catv,timestamp=d, inner_descr=u'Кабельное ТВ | абонплата')
#                f.save()
#                maxid = Fee.objects.aggregate(Max('id'))['id__max']
#                f = Fee.objects.get(pk=maxid)
#                f.make()
#                d = dd
#                dd = date_formatter(add_months(d,1))['month'].date()
#                pp = Payment.objects.filter(bill=self.bill,maked=False,bank_date__lte=d)
#                for p in pp:
#                    p.save()
#                    p.make()
#
#
#            if d < thismonth:
#                if debug:
#                    print "            closing date %s" % d
#                full = catv.get_sum(date=i.finish)['fee']
#                sum = full - catv_part.get_sum(date=i.finish)['ret']
#                prev_closing_fee = sum
#                prev_closing_month = date_formatter(i.finish)['month'].date()
#                f = Fee(bill=self.bill,card=self.catv_card,sum=sum,tp=tp,fee_type=catv,timestamp=i.finish, inner_descr=u'Кабельное ТВ | отключение')
#                f.save()
#                maxid = Fee.objects.aggregate(Max('id'))['id__max']
#                f = Fee.objects.get(pk=maxid)
#                f.make()
#
#                for service in self.catv_card.services.all():
#                    service.active=False
#                    service.save(sdate=d,descr="")
#                    self.catv_card.active = False
#                    self.catv_card.save()
#                    self.disabled= True
#                    self.save()
#
#            pp = Payment.objects.filter(bill=self.bill,maked=False,bank_date__lte=d)
#            for p in pp:
#                p.save()
#                p.make()
#
#        pp = Payment.objects.filter(bill=self.bill,maked=False)
#        for p in pp:
#            p.save()
#            p.make()
#
#        if debug:
#            print "    hamster finished his work and stopped"
#            print "    dont forget donate to WWF ;)"
#            print "    Bye..."
#
#        gc.collect()
#        return True

#    @classmethod
#    def hamsters_swarm(cls,fa=0,fb=0,ts=0,tc=0,tr=0):
#        import time
#        import gc
#        from lib.functions import seconds2hhmmss
#        #import thread
#
#        gc.enable()
#
#        #print "thread started..."
#        start = ts or int(time.time())
#        total = tc or cls.objects.all().count()
#        ready = tr or 0
#
#        #print {'fa':fa,'fb':fb,'ts':start,'tc':total,'tr':ready}
#
#        if (fa or fb) and (fa < fb):
#            qs = cls.objects.all()[fa:fb]
#        else:
#            qs = cls.objects.all()
#        for abonent in qs:
#            abonent.launch_hamster(debug=False)
#            ready+=1
#            if ready%10 == 0:
#                gc.collect()
#                elapsed=int(time.time())-start
#                progress=float("%.3f" % (ready/total*100))
#                remain=int(elapsed*total/ready)
#                print "processed abonents %s/%s (%s%%) elapsed: %s remain: %s" % (ready,total,progress,seconds2hhmmss(elapsed),seconds2hhmmss(remain))
#
#        #print "restarting thread..."
#        return {'fa':fb,'fb':fb*2-fa,'ts':start,'tc':total,'tr':ready}



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
        obj['bill__balance'] = self.bill.balance_get()
        obj['bill__balance_wo_credit'] = self.bill.balance_get_wo_credit()
        return obj



#class AbillsLink(models.Model):
#
#    abonent = models.ForeignKey(Abonent, unique=True)
#    abills = models.ForeignKey("abills.User", unique=True)
#    card = models.ForeignKey("tv.Card", unique=True)
#    service = models.ForeignKey("tv.CardService", unique=True)
#
#    class Meta:
#        pass
#    #    ordering = ['sorting']
#    #    unique_together = (("person", "address",),)
#    #    permissions = (
#    #        ("can_manage_disabled_abonents", "Can manage disabled abonents"),
#    #        ("can_delete_abonents", "Can delete abonents (RPC)"),
#    #        )
#
#    def __unicode__(self):
#        return "%s" % (self.abonent.__unicode__(),)
#
#    def delete(self, *args, **kwargs):
#        bill = self.abills.bill
#        bill.linked = False
#        bill.deposit = 0
#        bill.sync = 0
#        bill.save()
#        self.abills.admin_log('Unlinked from TV billing. deposit set to %s UAH' % (bill.sync,), datetime.now())
#        super(self.__class__, self).delete(*args, **kwargs)
#
#    @classmethod
#    def exists(cls,abonent,abills,card,service):
#        return cls.objects.filter(abonent=abonent,abills=abills,card=card,service=service).count()>0
#
#    @classmethod
#    def conflicts(cls,abonent,abills,card,service):
#        from django.db.models import Q
#        return cls.objects.filter(Q(abonent=abonent)|Q(abills=abills)|Q(card=card)|Q(service=service)).count()>0
#
#    @classmethod
#    def create(cls,abonent,abills,card,service):
#        obj = cls()
#        obj.abonent=abonent
#        obj.abills=abills
#        obj.card=card
#        obj.service=service
#        try:
#            obj.save()
#        except:
#            return False
#        obj.new_link()
#        return True
#
#    @classmethod
#    def check(cls,abonent,abills,card,service):
#        if not cls.exists(abonent,abills,card,service):
#            if not cls.conflicts(abonent,abills,card,service):
#                cls.create(abonent,abills,card,service)
#        else:
#            obj =  cls.objects.get(abonent=abonent,abills=abills,card=card,service=service)
#            obj.sync()
#
#    @classmethod
#    def process(cls):
#        for link in cls.objects.all():
#            link.sync()
#
#    def new_link(self):
#        bill = self.abills.bill
#        bill.linked = True
#        bill.sync = 0
#        bill.save()
#        self.abills.admin_log('Linked to TV billing. deposit was %s UAH' % (bill.sync,), datetime.now())
#        self.sync()
#
#    def payment(self,sum):
#        from tv.models import Payment
#        p = Payment()
#        p.register = None
#        p.source_id = 20
#        p.bill = self.abonent.bill
#        p.sum = sum
#        p.descr = ''
#        p.inner_descr = ''
#        p.admin_id= 2
#        p.bank_date = date.today()
#        p.save()
#        p.make()
#
#    def fee(self,sum):
#        from tv.models import Fee
#        f = Fee()
#        f.bill = self.abonent.bill
#        f.sum = sum
#        f.descr = 'Услуги "Интернет"'
#        f.inner_descr = f.descr
#        f.admin_id= 2
#        f.bank_date = date.today()
#        f.save()
#        f.make()
#
#    def sync(self):
#        from lib.functions import round1000
#        u = self.abonent.abills_get_user(self.service.extra)
#        bill = self.abills.bill
#        print
#        print "syncing abonent %s. card %s. bill %s" % (self.abonent,self.card,bill)
#        if not u == self.abills:
#            print "link not valid. deleting..."
#            self.delete()
#            return False
#        if not bill.deposit == bill.sync:
#            diff = bill.deposit - bill.sync
#            print "diff %s" % diff
#            diff = round1000(diff)
#            print "rounded diff %s" % diff
#            if 0<diff<1:
#                print "delta too small. ignored"
#                diff=0
#                return False
#            if -1<diff<0:
#                print "small negative delta. ignored"
#                diff=0
#                return False
#            if diff>0:
#                self.payment(diff)
#            else:
#                self.fee(-diff)
#            self.abills.admin_log('TV. deposit %s -> %s UAH' % (bill.deposit,self.abonent.bill.balance_get()), datetime.now())
#            bill.deposit = self.abonent.bill.balance_get()
#            bill.sync=bill.deposit
#            bill.save()
#        elif not bill.deposit == self.abonent.bill.balance_get():
#            diff = bill.deposit - self.abonent.bill.balance_get()
#            if -0.1<diff<0.1:
#                print "local change too small. ignored"
#                return False
#            print "local change"
#            self.abills.admin_log('TV. deposit %s -> %s UAH' % (bill.deposit,self.abonent.bill.balance_get()), datetime.now())
#            bill.deposit = self.abonent.bill.balance_get()
#            bill.sync=bill.deposit
#            bill.save()
#        else:
#            print "nothing to do"

