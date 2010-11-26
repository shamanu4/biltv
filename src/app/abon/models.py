# -*- coding: utf-8 -*-

from datetime import date, datetime
from django.db import models
from lib import extended

class Group(extended.Model):

    name = models.CharField(max_length=40, unique=True)
    comment = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

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

    class Meta:
        ordering = ['name']


class Person(extended.Model):

    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    middlename = models.CharField(max_length=40)
    passport = models.CharField(max_length=20, unique=True)
    registration = models.DateField(default=date.today())
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return "%s (%s)" % (self.sorting,self.passport)

    class Meta:
        ordering = ['sorting']

    def save(self, *args, **kwargs):
        from functions import latinaze
        self.passport=latinaze(self.passport)
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()
        self.middlename = self.middlename.capitalize()
        self.sorting = self.fio()
        for abonent in self.abonents:
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


class Contact(extended.Model):

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


class City(extended.Model):
    name = models.CharField(max_length=40, unique=True)
    label = models.CharField(blank=True, default='', max_length=40)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    """
    <label> must be ended with space. <label> and <street> contacted without delimeter.
    """

    def __unicode__(self):
        return self.name


    class Meta:
        ordering = ['name']


    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(self.__class__, self).save(*args,**kwargs)



class Street(extended.Model):

    city = models.ForeignKey(City, default=1, related_name='streets')
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=5, unique=True)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s%s" % (self.city.label, self.name)

    class Meta:
        ordering = ['name']
        unique_together = (("city", "name",),)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(self.__class__, self).save(*args,**kwargs)



class House(extended.Model):

    num = models.CharField(max_length=10, unique=True)
    code = models.CharField(max_length=5, unique=True)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.num

    class Meta:
        ordering = ['num']

    def save(self, *args, **kwargs):
        self.num = self.num.upper()
        super(self.__class__, self).save(*args,**kwargs)



class Building(extended.Model):

    street = models.ForeignKey(Street, related_name='houses')
    house = models.ForeignKey(House, related_name='houses')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=100, unique=True)

    def __unicode__(self):
        return "%s" % (self.sorting,)


    class Meta:
        ordering = ['sorting']
        unique_together = (("street", "house",),)


    def save(self, *args, **kwargs):
        self.sorting = "%s%s, %s" % (self.street.city.label, self.street.name, self.house.num)
        super(self.__class__, self).save(*args,**kwargs)



class Address(extended.Model):
    building = models.ForeignKey(Building, related_name='addresses')
    flat = models.CharField(max_length=10)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=100, unique=True)

    def __unicode__(self):
        return "%s" % (self.sorting,)


    class Meta:
        ordering = ['sorting']
        unique_together = (("building", "flat",),)


    def save(self, *args, **kwargs):
        self.flat = self.flat.lower()
        self.sorting = "%s, kv %s" % (self.building.sorting, self.flat)
        super(self.__class__, self).save(*args,**kwargs)



class Bill(extended.Model):

    balance = models.FloatField()
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
        return int_to_4byte_wrapped(self.balance_int)

    @property
    def bin_flags(self):
        res = []
        trunks = Trunk.objects.all()
        for t in trunks:
            res.extend(t.user_mask)
        return res


class Abonent(extended.Model):
    person = models.ForeignKey(Person, related_name='abonents')
    address = models.ForeignKey(Address, related_name='abonents')
    group = models.ForeignKey(Group, default=1, related_name='members')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sorting = models.CharField(blank=True, max_length=150)
    bill = models.ForeignKey(Bill)

    @property
    def bin_id(self):
        return int_to_4byte_wrapped(self.pk)

    @property
    def bin_card(self):
        return int_to_4byte_wrapped((self.card_id-1)*2)

    def __unicode__(self):
        return "%s" % (self.sorting,)

    class Meta:
        ordering = ['sorting']
        unique_together = (("person", "address",),)


    def save(self, *args, **kwargs):
        self.sorting = "%s, [ %s ]" % (self.address.sorting, self.person.fio_short())
        super(self.__class__, self).save(*args,**kwargs)


class AbonentCardRelationship(models.Model):
    from tv.models import Card

    abonent = models.ForeignKey(Abonent)
    card = models.ForeignKey(Card, unique=True)
    activated = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "%s - %s" % (self.abonent, self.card)

    def delete(self, *args, **kwargs):
        self.card.deactivate()
        super(self.__class__, self).delete(*args,**kwargs)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args,**kwargs)
        self.card.activate()

