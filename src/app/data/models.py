# -*- coding: utf-8 -*-
from datetime import date, datetime
from django.db import models

#class Status(models.Model):
#
#    iac = models.ForeignKey("abon.Abonent", to_field="extid", db_column="iac", related_name="intervals")
#    begin = models.DateField()
#    end = models.DateField()
#    start = models.DateField()
#    finish = models.DateField()
#    s1 = models.FloatField()
#    s2 = models.FloatField()
#
#    @classmethod
#    def fix_period_start(cls):
#        from tv.models import Fee
#        from tv.models import FeeType
#        from tv.models import TariffPlan
#
#        ss = cls.objects.filter(start__gte='2006-02-01').filter(start__lt='2011-03-01')
#        ft = FeeType.objects.all()
#        ft = ft[0]
#        ft2 = FeeType.objects.all()
#        ft2 = ft2[4]
#        tp = TariffPlan.objects.all()
#        tp = tp[0]
#
#        for s in ss:
#            m1 = ft.get_sum(date=s.start)['fee']
#            m2 = ft2.get_sum(date=s.start)['fee']
#            m = m2-m1
#            try:
#                bill = s.iac.bill
#                card = s.iac.catv_card
#                print "%s %s | %s | %s %s" % (card,bill,m,m1,m2)
#                f = Fee(bill=bill,card=card,sum=-m,tp=tp,fee_type=ft,inner_descr=u'перенос бази. возврат подключение',timestamp=s.start)
#                f.save()
#                f.make()
#            except:
#                print "EXCEPTION CAUGHT!"
#
#    @classmethod
#    def fix_period_end(cls):
#        from tv.models import Fee
#        from tv.models import FeeType
#        from tv.models import TariffPlan
#
#        ss = cls.objects.filter(finish__lte='2011-03-01')
#        ft = FeeType.objects.all()
#        ft = ft[0]
#        tp = TariffPlan.objects.all()
#        tp = tp[0]
#
#        for s in ss:
#            if not s.finish:
#                continue
#            try:
#                bill = s.iac.bill
#                card = s.iac.catv_card
#                m = ft.get_sum(date=s.finish)['ret']
#                print "%s %s | %s |" % (card,bill,m)
#                f = Fee(bill=bill,card=card,sum=-m,tp=tp,fee_type=ft,inner_descr=u'перенос бази. возврат отключение',timestamp=s.finish)
#                f.save()
#                f.make()
#            except:
#                print "EXCEPTION CAUGHT!"
#
#    @classmethod
#    def fix_all(cls):
#        cls.fix_period_start()
#        cls.fix_period_end()
        

#class Intervals(models.Model):
#
#    ic = models.ForeignKey("abon.Abonent", to_field="extid", db_column="iac", related_name="intervals2")
#    start = models.DateField()
#    end = models.DateField()
#    cost = models.FloatField()
#    months = models.IntegerField()
#
#class Import(models.Model):
#    order = models.CharField(max_length=80)
#    street = models.CharField(max_length=80)
#    house = models.CharField(max_length=80)
#    flat = models.CharField(max_length=80)
#    passport = models.CharField(max_length=80)
#    fio = models.CharField(max_length=80)
#    iac = models.IntegerField()
#    ic = models.IntegerField()
    
#class Proplata(models.Model):
#    iac = models.ForeignKey("abon.Abonent", to_field="extid", db_column="iac", related_name="proplatu")
#    d1 = models.DateField()
#    sum = models.IntegerField()


"""

from data.models import Import
ii = Import.objects.all()
from abon.models import Street,House,Building,Address,Person
from abon.models import Abonent
from tv.models import Payment
addr = Address()
b = Building()

from lib.functions import latinaze

for i in ii:
    build = b.get_or_create(i.street,i.house)
    ad = addr.get_or_create(build,i.flat,i.order)
    p = Person.objects.get_or_create(passport=latinaze(i.passport))
    print "!"
    p = p[0]
    p.lastname=i.fio
    p.save()
    a = Abonent.objects.get_or_create(person=p,address=ad)[0]
    a.extid = i.iac
    a.save()
    #a.proplatu.all()
    pc = Payment.objects.filter(bill=a.bill).count()
    print a.intervals.all()
    if not pc:
        for pr in a.proplatu.all():
            npr = Payment(bill=a.bill,sum=pr.sum,bank_date=pr.d1,inner_descr="MIGRATION")
            npr.save()        
    for service in a.catv_card.services.all():
        service.active=False
        service.save(no_log=True)
    a.launch_hamster(countdown=False)
"""


class House(models.Model):

    name = models.CharField(max_length=10)
    code = models.CharField(max_length=5)
    num = models.PositiveSmallIntegerField()
    korp = models.PositiveSmallIntegerField()
    letter = models.CharField(max_length=1)

    class Meta:
        pass

    def __unicode__(self):
        result = self.name
#        result = self.num
#        if self.korp:
#            result += "/%s" % self.korp
#        if self.letter:
#            result += self.letter
        return result

    @classmethod
    def export(cls):
        from abon.models import House as AbonHouse
        AbonHouse.objects.all().delete()
        data = cls.objects.all()
        for entry in data:
            a = AbonHouse(num=entry.name,code=entry.code)
            a.save()

class Street(models.Model):

    name = models.CharField(max_length=40)
    code = models.CharField(max_length=3)

    class Meta:
        pass

    def __unicode__(self):
        return self.name

    @classmethod
    def export(cls):
        from abon.models import Street as AbonStreet, City as AbonCity
        AbonStreet.objects.all().delete()
        AbonCity.objects.all().delete()
        city = AbonCity(name='default_city')
        city.save()
        data = cls.objects.all()
        for entry in data:
            a = AbonStreet(name=entry.name,code=entry.code,city=city)
            a.save()


class Address(models.Model):

    street = models.ForeignKey(Street)
    house = models.ForeignKey(House)
    loft = models.CharField(max_length=10)
    tel = models.CharField(max_length=20)
    remark = models.TextField()
    faceorder = models.CharField(max_length=13)
    pereoform = models.BooleanField()

    class Meta:
        pass

    def __unicode__(self):
        return "%s, %s" % (self.street.name, self.house.name)

    @classmethod
    def export(cls):
        from abon.models import Address as AbonAddress, Building as AbonBuilding
        AbonAddress.objects.all().delete()
        AbonBuilding.objects.all().delete()
        data = cls.objects.all()
        for entry in data:
            a = AbonAddress.get_or_create_cls(street=entry.street.name,house=entry.house.name,flat=entry.loft,override=entry.faceorder)
            a.comment = "%s\n%s" % (entry.tel or '',entry.remark or '')
            a.save()



class Person(models.Model):

    fio = models.CharField(max_length=60)
    passport = models.CharField(max_length=20)

    class Meta:
        pass

    def __unicode__(self):
        return self.fio

    @classmethod
    def export(cls):
        from abon.models import Person as AbonPerson
        AbonPerson.objects.all().delete()
        data = cls.objects.all()
        for entry in data:
            if entry.passport == "no-passport":
                entry.passport = "no-passport-%s" % entry.pk
            a = AbonPerson(lastname=entry.fio, passport=entry.passport)
            a.save()


class Abonent(models.Model):

    address = models.ForeignKey(Address)
    person = models.ForeignKey(Person)
    active = models.BooleanField()

    class Meta:
        pass

    def __unicode__(self):
        return "%s [%s]" % (self.address.__unicode__(),self.person.__unicode__())

    @classmethod
    def export(cls):
        from abon.models import Abonent as AbonAbonent, Address as AbonAddress, Person as AbonPerson, Bill as AbonBill
        AbonAbonent.objects.all().delete()
        data = cls.objects.all()
        for entry in data:
            try:
                print entry.person
            except:
                print "person does not exists. abonent id %s" % entry.pk
                continue
            try:
                print entry.address
            except:
                print "address does not exists. abonent id: %s" % entry.pk
                continue
            addr = AbonAddress.get_or_create_cls(entry.address.street.name,entry.address.house.name,entry.address.loft,entry.address.faceorder)
            person = AbonPerson.get_or_create_cls(entry.person.fio,entry.person.passport)
            try:
                a = AbonAbonent.objects.get(person=person,address=addr)
            except AbonAbonent.DoesNotExist:
                bill = AbonBill.objects.create()
                a = AbonAbonent(address=addr,person=person,bill=bill,comment=entry.address.remark,extid=entry.pk,disabled=not entry.active)
            a.save()
            if entry.address.tel:
                person.contact_add(0,entry.address.tel)


class Category(models.Model):

    name = models.CharField(max_length=40)

    class Meta:
        pass

    def __unicode__(self):
        return self.name



class Tariff(models.Model):

    category = models.ForeignKey(Category)
    tar = models.FloatField()
    d1 = models.DateField()
    d2 = models.DateField()

    class Meta:
        pass

    def __unicode__(self):
        return str(self.tar)



class AbonentCat(models.Model):

    abonent = models.ForeignKey(Abonent)
    category = models.ForeignKey(Category)
    d1 = models.DateField()
    d2 = models.DateField()

    class Meta:
        pass

    def __unicode__(self):
        return "%s - %s" % (self.abonent.__unicode__(),self.category.__unicode__())

    @classmethod
    def export(cls):
        from abon.models import Abonent as AbonAbonent
        from tv.models import TariffPlan
        from datetime import date
        today = date.today()
        for entry in cls.objects.all():
            try:
                print entry.abonent
            except:
                print "abonent %s does not exist" % entry.abonent_id
                continue
            try:
                a = AbonAbonent.objects.get(extid=entry.abonent.pk)
            except:
                print "abonent %s does not exist" % entry.abonent_id
                continue
            card = a.catv_card
            service = card.services.get()
            try:
                tp = TariffPlan.objects.get(comment=entry.category_id)
            except:
                print "tp id % does not exist" % entry.category_id
                continue
            service.tp =tp
            service.save()
            if entry.abonent.active:
                card.activate(activated=today)

class Proplata(models.Model):

    abonent = models.ForeignKey(Abonent)
    d1 = models.DateField()
    d2 = models.DateField()
    sum = models.FloatField()
    y = models.PositiveSmallIntegerField()
    m = models.PositiveSmallIntegerField()
    v = models.CharField(max_length=20)
    log = models.TextField()

    class Meta:
        pass

    def __unicode__(self):
        return "%s : %s" % (self.abonent.__unicode__(),self.sum)





