# -*- coding: utf-8 -*-

from django.utils import datetime_safe
import time, datetime
import json

def str2date(value):
    return datetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M:%S')[:6])


class DatetimeJSONEncoder(json.JSONEncoder):

    class DateInt(int):
        def __str__(self):
            return 'new Date(%s)' % (self*1000)

    def default(self, o):

        if isinstance(o, datetime.datetime):
            d = datetime_safe.new_datetime(o)
            return self.DateInt(int(time.mktime(d.timetuple())))
        else:
            return super(DatetimeJSONEncoder, self).default(o)


class DatetimeJSONEncoderQt(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, datetime.time):
            return o.strftime('%H:%M:%S')
        elif hasattr(o, '__unicode__'):
            return o.__unicode__()
        else:
            return super(DatetimeJSONEncoderQt, self).default(o)

