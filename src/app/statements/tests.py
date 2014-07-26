# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from unittest import TestCase
from StringIO import StringIO
import json

from django.core.management import call_command
from statements.models import Statement, Entry, Category, Filter, TYPE_CATV, TYPE_INET
from tv.models import PaymentSource


PATH = "/home/maxim/projects/biltv2/src/app/statements/tmp/c2ball.xls"


class ParserTestCase(TestCase):
    statement = None
    ps = None
    cat_liqpay_catv = None
    cat_liqpay_inet = None
    cat_bankname = None
    f_liqpay_catv = None
    f_liqpay_inet = None

    @classmethod
    def setUpClass(cls):
        content = StringIO()
        call_command('import_xls', PATH, stdout=content)
        j = json.loads(content.getvalue())
        assert (type(j['statement']) == dict)
        call_command('import_xls', PATH, '2014-07-01', process=1)
        cls.statement = Statement.objects.get(pk=1)
        e = Entry.objects.get(pk=1)
        assert (e.statement == cls.statement)
        cls.ps = PaymentSource.objects.create(name="BankName")
        cls.cat_liqpay_catv = Category.objects.create(name="liqpay catv", svc_type=TYPE_CATV, auto_processed=True)
        cls.cat_liqpay_inet = Category.objects.create(name="liqpay inet", svc_type=TYPE_INET, auto_processed=True)
        cls.cat_bankname = Category.objects.create(name="BankName1", svc_type=TYPE_INET, auto_processed=False,
                                                   source=cls.ps)
        assert (Category.objects.count() == 3)
        cls.f_liqpay_catv = Filter.objects.create(name="f_liqpay_catv", enabled=True, category=cls.cat_liqpay_catv,
                                                  json=json.dumps({'descr__istartswith': 'LIQPAY',
                                                                   'descr__icontains': 'Television'}))
        cls.f_liqpay_inet = Filter.objects.create(name="f_liqpay_catv", enabled=True, category=cls.cat_liqpay_inet,
                                                  json=json.dumps(
                                                      {'descr__istartswith': 'LIQPAY', 'descr__icontains': 'Internet'}))
        cls.f_liqpay_bank = Filter.objects.create(name="f_liqpay_catv", enabled=True, category=cls.cat_bankname,
                                                  json=json.dumps({'mfo__exact': 380805}))

    def test_01_filter_process_catv(self):
        self.f_liqpay_catv.process(self.statement)

    def test_02_filter_process_inet(self):
        self.f_liqpay_inet.process(self.statement)

    def test_03_filter_results_catv(self):
        for line in self.cat_liqpay_catv.lines.all():
            self.assertEqual(line.processed, line.category.auto_processed)
            self.assertEqual(line.category, self.cat_liqpay_catv)

    def test_04_filter_results_inet(self):
        for line in self.cat_liqpay_inet.lines.all():
            self.assertEqual(line.processed, line.category.auto_processed)
            self.assertEqual(line.category, self.cat_liqpay_inet)

    def test_05_filter_process_bank(self):
        self.f_liqpay_bank.process(self.statement)

    def test_06_filter_results_bank(self):
        for line in self.cat_bankname.lines.all():
            self.assertEqual(line.processed, line.category.auto_processed)
            self.assertEqual(line.category, self.cat_bankname)



