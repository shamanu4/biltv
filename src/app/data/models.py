# -*- coding: utf-8 -*-
from datetime import date, datetime
from django.db import models

class Status(models.Model):

    iac = models.ForeignKey("abon.Abonent", to_field="extid", db_column="iac", related_name="intervals")
    begin = models.DateField()
    end = models.DateField()
    start = models.DateField()
    finish = models.DateField()
    s1 = models.FloatField()
    s2 = models.FloatField()
    
    @classmethod
    def fix_period_start(cls):
        from tv.models import Fee
        from tv.models import FeeType
        from tv.models import TariffPlan

        ss = cls.objects.filter(start__gte='2006-02-01').filter(start__lt='2011-03-01')
        ft = FeeType.objects.all()
        ft = ft[0]
        ft2 = FeeType.objects.all()
        ft2 = ft2[4]
        tp = TariffPlan.objects.all()
        tp = tp[0]

        for s in ss:
            m1 = ft.get_sum(date=s.start)['fee']
            m2 = ft2.get_sum(date=s.start)['fee']
            m = m2-m1
            try:
                bill = s.iac.bill
                card = s.iac.catv_card
                print "%s %s | %s | %s %s" % (card,bill,m,m1,m2)
                f = Fee(bill=bill,card=card,sum=-m,tp=tp,fee_type=ft,inner_descr=u'перенос бази. возврат подключение',timestamp=s.start)
                f.save()
                f.make()
            except:
                print "EXCEPTION CAUGHT!"
    
    @classmethod
    def fix_period_end(cls):
        from tv.models import Fee
        from tv.models import FeeType
        from tv.models import TariffPlan

        ss = cls.objects.filter(finish__lte='2011-03-01')
        ft = FeeType.objects.all()
        ft = ft[0]
        tp = TariffPlan.objects.all()
        tp = tp[0]

        for s in ss:
            if not s.finish:
                continue                
            try:
                bill = s.iac.bill
                card = s.iac.catv_card
                m = ft.get_sum(date=s.finish)['ret']
                print "%s %s | %s |" % (card,bill,m)
                f = Fee(bill=bill,card=card,sum=-m,tp=tp,fee_type=ft,inner_descr=u'перенос бази. возврат отключение',timestamp=s.finish)
                f.save()
                f.make()
            except:
                print "EXCEPTION CAUGHT!"
        
    @classmethod
    def fix_all(cls):
        cls.fix_period_start()
        cls.fix_period_end()
        

class Intervals(models.Model):
    
    ic = models.ForeignKey("abon.Abonent", to_field="extid", db_column="iac", related_name="intervals2")
    start = models.DateField()
    end = models.DateField()    
    cost = models.FloatField()
    months = models.IntegerField()
                
class Import(models.Model):
    order = models.CharField(max_length=80)
    street = models.CharField(max_length=80)
    house = models.CharField(max_length=80)
    flat = models.CharField(max_length=80)
    passport = models.CharField(max_length=80)
    fio = models.CharField(max_length=80)
    iac = models.IntegerField()
    ic = models.IntegerField()
    
class Proplata(models.Model):
    iac = models.ForeignKey("abon.Abonent", to_field="extid", db_column="iac", related_name="proplatu")
    d1 = models.DateField()
    sum = models.IntegerField()
