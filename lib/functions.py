# -*- coding: utf-8 -*-

class QuerySetChain(object):
    """
    Chains multiple subquerysets (possibly of different models) and behaves as
    one queryset.  Supports minimal methods needed for use with
    django.core.paginator.
    """

    def __init__(self, *subquerysets):
        self.querysets = subquerysets

    def count(self):
        """
        Performs a .count() for all subquerysets and returns the number of
        records as an integer.
        """
        return sum(qs.count() for qs in self.querysets)

    def _clone(self):
        "Returns a clone of this queryset chain"
        return self.__class__(*self.querysets)

    def _all(self):        
        "Iterates records in all subquerysets"
        from itertools import chain
        return chain(*self.querysets)

    def __getitem__(self, ndx):
        """
        Retrieves an item or slice from the chained set of results from all
        subquerysets.
        """
        from itertools import islice
        if type(ndx) is slice:
            return list(islice(self._all(), ndx.start, ndx.stop, ndx.step or 1))
        else:
            return islice(self._all(), ndx, ndx+1).next()


def int_to_4byte(num):
    import struct

    res = []
    binary = struct.pack('!l',num)
    for char in binary:
        res.append(ord(char))

    return res



def short_to_2byte(num):
    import struct

    res = []
    binary = struct.pack('!H',num)
    for char in binary:
        res.append(ord(char))

    return res



def wrap_list(list):
    res = []
    l = len(list)
    for i in range(l):
        res.append(list[l-i-1])

    return res



def int_to_4byte_wrapped(num):
    return wrap_list(int_to_4byte(num))



def short_to_2byte_wrapped(num):
    return wrap_list(short_to_2byte(num))



def byte_and(list1,list2):
    res =[]
    if not len(list1) == len(list2):
        return res
    for i in range(0,len(list1)):
        res.append(list1[i]&list2[i])
    return res


def byte_or(list1,list2):
    res =[]
    if not len(list1) == len(list2):
        return res                                                         
    for i in range(0,len(list1)):
        res.append(list1[i]|list2[i])
    return res


def byte_xor(list1,list2):
    res =[]
    if not len(list1) == len(list2):
        return res                                                         
    for i in range(0,len(list1)):
        res.append(list1[i]^list2[i])
    return res

def latinaze(str):
    str = str.upper()
    res = []
    en = ['A','B','C','E','H','I','K','M','O','P','T','X','Y','0','1','2','3','4','5','6','7','8','9']
    ru = [u'А',u'В',u'С',u'Е',u'Н',u'І',u'К',u'М',u'О',u'Р',u'Т',u'Х',u'У']
    for char in str:
        if char in en:
            res.append(char)
            continue
        if char in ru:
            index = ru.index(char)
            res.append(en[index])
        else:
            return str
    return ''.join(res)


def date_formatter(date=None):
    import datetime

    if not date:
        date = datetime.datetime.now()

    day = date.day
    weekday = date.weekday()
    month = date.month
    year = date.year
    thisday = datetime.datetime(year, month, day)
    thisweek = datetime.datetime(year, month, day)-datetime.timedelta(weekday)
    thismonth = datetime.datetime(year, month, 1)
    thisyear = datetime.datetime(year, 1, 1)

    return { 'day':thisday, 'week':thisweek, 'month':thismonth, 'year':thisyear }

def add_months(sourcedate,months):
    import datetime
    import calendar
    
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

def seconds2hhmmss(seconds):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

def hamsters_swarm(fa, fb, ts=0, tc=0, tr=0):
    from abon.models import Abonent
    Abonent.hamsters_swarm(fa, fb, ts, tc, tr)

def list2bin(list):
    bin = ""
    for w in list:
        bin += chr(w)
    return bin

def list2hex(list):
    hex = ""
    for w in list:
        hex += "%0.2x " % w
    return hex

def round1000(num):
    a = num*1000
    b = int(a % 1000)
    c = int(a)/1000
    if -2 < b < 0:
        return c/1.0
    if 0 < b < 2:
        return c/1.0
    if b < -998:
        return (c-1)/1.0
    if b > 998:
        return (c+1)/1.0
    return c + b/1000.0