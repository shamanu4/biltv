# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime


def ip_to_num(ip_addr):
        sets = map(int, ip_addr.split("."))
        return int(sets[0]*256**3 + sets[1]*256**2 + sets[2]*256 + sets[3])


class Admin(models.Model):
    """
    Abills admin cutted model. we need only name and aid.
    """
    name = models.CharField(max_length=50, db_column='name')
    aid = models.IntegerField(unique=True, primary_key=True, db_column='aid')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'admins'


class Bill(models.Model):

    deposit = models.FloatField(default=0)
    uid = models.IntegerField(blank=True,null=True)
    company_id =models.IntegerField(blank=True,null=True)


    def __unicode__(self):
        return "%s" % self.deposit

    class Meta:
        db_table = 'bills'


class Company(models.Model):

    bill = models.ForeignKey(Bill,related_name='companies')
    name = models.CharField(max_length=100,unique=True)
    credit = models.FloatField(default=0)
    credit_date = models.DateField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'companies'
        ordering = ['name']


class User(models.Model):

    id = models.IntegerField(primary_key=True,db_column='uid')
    login = models.CharField(max_length=20,unique=True,db_column='id')
    disabled = models.BooleanField(db_column='disable')
    company = models.ForeignKey(Company,related_name='clients')

    def __unicode__(self):
        return self.login

    class Meta:
        db_table = 'users'
        ordering = ['login']
    
    @property
    def pi(self):
        try:
            return UserPi.objects.get(id=self.id)
        except UserPi.DoesNotExist:
            return None
        
    def promotion(self,fee):
        self.payment(fee.bonus, u'акція. %s. %s' % (fee.tp.__unicode__(), fee.timestamp ) )        
    
    def promotion_on(self,card,cs,pl,timestamp):
        if self.pi:
            self.pi.card_num = card.num
        self.tp_set(pl.abills_tp, timestamp)
    
    def promotion_off(self,card,cs,pl,timestamp):
        if self.pi:
            self.pi.card_num = card.num
        self.tp_set(pl.abills_tp, timestamp)
    
    def tp_set(self,tp,timestamp=datetime.now()):
        self.admin_log('%s->%s' % (self.dv.tp,tp), timestamp)
        self.dv.tp = tp
        self.dv.save()
    
    def admin_log(self,text,timestamp=datetime.now()):
        a = Admin.objects.get(pk=37)
        al = AdminLog()
        al.actions = text
        al.datetime = timestamp
        al.user = self
        al.admin = a
        al.save()
    
    def payment(self,sum,dsc):
        a = Admin.objects.get(pk=37)
        p = Payment()
        p.sum = sum
        p.dsc = dsc
        p.aid = a
        p.uid = self.id
        p.bill = self.company.bill
        p.save()
        p.make()

class Street(models.Model):

    name = models.CharField(max_length=120,unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = '_street_list'
        ordering = ['name']


class House(models.Model):

    name = models.CharField(max_length=120,unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = '_house_list'
        ordering = ['name']


class UserPi(models.Model):

    id = models.IntegerField(primary_key=True,db_column='uid')
    fio =  models.CharField(max_length=100,unique=True)
    house = models.ForeignKey(House,db_column='_house')
    street = models.ForeignKey(Street,db_column='_street')
    kv = models.CharField(max_length=10,db_column='address_flat')
    card_num = models.IntegerField(db_column='_digital_tv')

    def __unicode__(self):
        return "%s %s %s" % (self.street.name, self.house.name, self.kv)

    class Meta:
        db_table = 'users_pi'
        ordering = ['fio']

    def export(self):
        data = {'exists':True}
        data.update({'fio':self.fio})
        data.update({'street':self.street.name})
        data.update({'house':self.house.name})
        data.update({'kv':self.kv})
        return data


class Payment(models.Model):

    date = models.DateTimeField(default=datetime.now)
    sum = models.FloatField(default=0)
    aid = models.ForeignKey(Admin,db_column='aid')
    uid = models.PositiveIntegerField(db_column='uid')
    bill = models.ForeignKey(Bill,related_name='payments')
    ip = models.IntegerField(default=ip_to_num('127.0.0.1'))
    last_deposit = models.FloatField(default=0)
    dsc = models.CharField(max_length=80,db_column='inner_describe')

    class Meta:
        db_table = 'payments'
        ordering = ['date']

    def __unicode__(self):
        return self.sum

    def ip_to_num(self, ip_addr):
        sets = map(int, ip_addr.split("."))
        return int(sets[0]*256**3 + sets[1]*256**2 + sets[2]*256 + sets[3])

    def num_to_ip(self, number):
        d = number % 256
        c = int(number/256) % 256
        b = int(number/(256**2)) % 256
        a = int(number/(256**3)) % 256
        return "%s.%s.%s.%s" % (a,b,c,d)

    def get_ip(self):
        return self.num_to_ip(self.ip)

    def set_ip(self,ipaddr):
        self.ip = self.ip_to_num(ipaddr)

    def make(self):
        self.last_deposit = self.bill.deposit
        self.save() 
        self.bill.deposit = self.bill.deposit + self.sum
        self.bill.save() 

class Tp(models.Model):

    name = models.CharField(max_length=120,unique=True)

    class Meta:
        db_table = 'tarif_plans'
        ordering = ['name']

    def __unicode__(self):
        return self.name
    
    @classmethod    
    def choices(cls):
        res = []
        for obj in cls.objects.all().order_by('pk'):
            res.append((obj.pk,"%s: %s" % (obj.pk,obj.name)))
        return res



class Dv(models.Model):

    user = models.OneToOneField(User,db_column='uid',related_name="dv",primary_key=True)
    tp = models.ForeignKey(Tp)

    class Meta:
        db_table = 'dv_main'
        ordering = ['user__login']

    def __unicode__(self):
        return "%s - %s" % (self.user.login, self.tp.name)
    

class AdminLog(models.Model):
    actions = models.CharField(max_length=120)
    datetime = models.DateTimeField(default=datetime.now)
    ip = models.IntegerField(default=ip_to_num('127.0.0.1'))
    user = models.ForeignKey(User,db_column='uid')
    admin = models.ForeignKey(Admin,db_column='aid')
    module = models.CharField(max_length=20, default="Dv")
    action_type = models.PositiveSmallIntegerField(default=3)
    
    class Meta:
        db_table = 'admin_actions'
        ordering = ['-datetime']