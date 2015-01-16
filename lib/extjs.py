# -*- coding: utf-8 -*-

import sys
import traceback
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from inspect import getargspec
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
from django.db.models.query import QuerySet
from lib.functions import QuerySetChain
from django.db.models import Q
from django.utils.functional import update_wrapper
from functools import wraps
from django.conf import settings
from datetime import datetime, date
import redis
import json
import xlsxwriter


def check_perm(perm):
    def decorator(func):
        def inner_decorator(*args, **kwargs):
            if 'request' in kwargs:
                request = kwargs['request']
                try:
                    if request.user.has_perm(perm):
                        return func(*args, **kwargs)
                    else:
                        return dict(success=False, title=u'Доступ запрещен', msg=u'user %s has not permission %s' % (request.user,perm), errors='' )
                except Exception as inst:
                    return dict(success=False, title=u'Ошибка доступа', msg=u'perm: %s;\n exception: %s;' % (perm,inst), errors=traceback.format_exc())
            else:
                return dict(success=False, title=u'Доступ запрещен', msg=u'invalid arguments while permission (%s) check. (no request)' % perm, errors='' )
        return wraps(func)(inner_decorator) 
    return decorator


def extract_val(val):
    val = True if val in ['true', 'True'] else val
    val = False if val in ['false', 'False'] else val
    return val


def xls(data):
    r = redis.StrictRedis()
    filename = "xls_%s.xlsx" % str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    total = len(data)
    cur = 0

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook("%s/xls/%s" % (settings.MEDIA_ROOT, filename))
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 18)
    worksheet.set_column('C:C', 24)
    worksheet.set_column('D:D', 6)
    worksheet.set_column('E:E', 3)
    worksheet.set_column('F:F', 7)
    worksheet.set_column('G:G', 7)

    bold = workbook.add_format({'bold': 1, 'font_size': 10})
    small = workbook.add_format({'font_size': 10})
    merge_small = workbook.add_format({'font_size': 8, 'font_color': "#505050"})
    date_format = workbook.add_format({'num_format': 'd-m-yy', 'font_size': 10})

    worksheet.write('A1', u'code', bold)
    worksheet.write('B1', u'ФИО', bold)
    worksheet.write('C1', u'Адрес', bold)
    worksheet.write('D1', u'Баланс', bold)
    worksheet.write('E1', u'Откл', bold)
    worksheet.write('F1', u'Подключен', bold)
    worksheet.write('G1', u'Отключен', bold)

    cx = 1

    for line in data:
        cur += 1
        cx += 1
        worksheet.write('A%s' % cx, line['code'], small)
        worksheet.write('B%s' % cx, line['person'], small)
        worksheet.write('C%s' % cx, line['address'], small)
        worksheet.write('D%s' % cx, line['bill__balance2'], small)
        if line['disabled']:
            worksheet.write('E%s' % cx, "x")
        else:
            worksheet.write('E%s' % cx, "")
        if type(line['activated']) == date:
            worksheet.write_datetime('F%s' % cx, line['activated'], date_format)
        else:
            worksheet.write('F%s' % cx, line['activated'], small)
        if type(line['deactivated']) == date:
            worksheet.write_datetime('G%s' % cx, line['deactivated'], date_format)
        else:
            worksheet.write('G%s' % cx, line['deactivated'], small)
        if line['comment']:
            cx += 1
            comment = line['comment'].replace('\n','    ')
            worksheet.merge_range('A%s:G%s' % (cx, cx), comment, merge_small)
        if not cur % 10:
            r.publish('xls', json.dumps({"ready": False, "msg": u"загрузка [%s/%s]" % (cur, total)}))
    r.publish('xls', json.dumps({"ready": True, "url": "%sxls/%s" % (settings.MEDIA_URL, filename)}))


def store_read(func):
    def wrapper(*args, **kwargs):
        from lib.functions import latinaze
        import re
        r = redis.StrictRedis()
        spec_lookup = re.compile("^.*\_{2}(i?exact|i?contains|(l|g)te|i?(start|end)swith)$")
        result = func(*args, **kwargs)
        rdata = args[1]
        if isinstance(result, tuple):
            result, extras = result
            success = True
        else:
            success = True
            extras = {}
        total=0
        if isinstance(result, list):
            result = [obj.store_record() for obj in result]
            total = len(result)
            if 'start' in rdata and 'limit' in rdata:
                result = result[rdata['start']:rdata['start']+rdata['limit']]
        if isinstance(result, QuerySet) or isinstance(result, QuerySetChain):
            if 'xls' in rdata and rdata['xls']:
                r.publish('xls', json.dumps({"ready": False, "msg": u"обработка данных..."}))
            if 'filter_fields' in rdata and 'filter_value' in rdata:
                query=None
                if 'query' in rdata:
                    for node in rdata['filter_fields']:
                        val=unicode(rdata['query'])
                        wild = val.split('*')                 
                        query2 = None
                        for v in wild:
                            v = extract_val(v)
                            if not v == '':
                                if spec_lookup.match(node):
                                    if query2:                            
                                        query2 = query2 & Q(**{"%s" % str(node):v})
                                    else:
                                        query2 = Q(**{"%s" % str(node):v})
                                else:
                                    if query2:                            
                                        query2 = query2 & Q(**{"%s__icontains" % str(node):v})
                                    else:
                                        query2 = Q(**{"%s__istartswith" % str(node):v})
                        if query:
                            query = query | query2
                        else:
                            query = query2
                if not rdata['filter_value']=='':                    
                    for node in rdata['filter_fields']:
                        if 'passport' in node:
                            val=latinaze(rdata['filter_value'])
                        else:
                            val=unicode(rdata['filter_value'])
                        wild = val.split('*')
                        query2 = None
                        for v in wild:
                            v = extract_val(v)
                            if not v == '':
                                if spec_lookup.match(node):
                                    if query2:
                                        query2 = query2 & Q(**{"%s" % str(node):v})
                                    else:
                                        query2 = Q(**{"%s" % str(node):v})
                                else:
                                    if query2:
                                        query2 = query2 & Q(**{"%s__icontains" % str(node):v})
                                    else:
                                        query2 = Q(**{"%s__icontains" % str(node):v})
                        if query:
                            query = query | query2
                        else:
                            query = query2
                if query:
                    result = result.filter(query)
            if 'filter' in rdata:
                for item in rdata['filter']:
                    val = unicode(rdata['filter'][item])
                    val = extract_val(val)
                    result = result.filter(**{str(item):val})
            if 'sort' in rdata:
                if 'dir' in rdata and rdata['dir']=='DESC':
                    result = result.order_by('-%s' % rdata['sort'])
                else:
                    result = result.order_by('%s' % rdata['sort'])
            total = result.count()
            if 'start' in rdata and 'limit' in rdata:
                result = result[rdata['start']:rdata['start']+rdata['limit']]
            if 'xls' in rdata and rdata['xls']:
                rs = []
                total = len(result)
                cur = 0
                result = result.order_by('address__override')
                for obj in result:
                    cur += 1
                    if not cur % 10:
                        r.publish('xls', json.dumps({"ready": False, "msg": u"обработка [%s/%s]" % (cur, total)}))
                    rs.append(obj.store_record())
                xls(rs)
                result = []
            else:
                result = [obj.store_record() for obj in result]
        return dict(data=result, success=success, total=total, extras=extras)
    return update_wrapper(wrapper, func)

class RpcRouterJSONEncoder(simplejson.JSONEncoder):

    def __init__(self, url_args, url_kwargs, *args, **kwargs):
        self.url_args = url_args
        self.url_kwargs = url_kwargs
        super(RpcRouterJSONEncoder, self).__init__(*args, **kwargs)

    def _encode_action(self, o):
        output = []
        for method in dir(o):
            if not method.startswith('_'):
                f = getattr(o, method)
                data = dict(name=method, len=getattr(f, '_args_len', 0))
                if getattr(f, '_form_handler', False):
                    data['formHandler'] = True
                output.append(data)
        return output

    def default(self, o):
        if isinstance(o, RpcRouter):
            output = {
                'type': 'remoting',
                'url': reverse(o.url, args=self.url_args, kwargs=self.url_kwargs),
                'enableBuffer': o.enable_buffer,
                'actions': {}
            }
            for name, action in o.actions.items():
                output['actions'][name] = self._encode_action(action)
            return output
        else:
            return super(RpcRouterJSONEncoder, self).default(o)

class RpcRouter(object):

    def __init__(self, url, actions={}, enable_buffer=True):
        self.url = url
        self.actions = actions
        self.enable_buffer = enable_buffer

    def api(self, request, *args, **kwargs):
        obj = simplejson.dumps(self, cls=RpcRouterJSONEncoder, url_args=args, url_kwargs=kwargs)
        return HttpResponse('Ext.Direct.addProvider(%s)' % obj)

    def __call__(self, request, *args, **kwargs):
        user = request.user
        POST = request.POST
        
        if POST.get('extAction'):
            #Forms not supported yet
            requests = {
                'action': POST.get('extAction'),
                'method': POST.get('extMethod'),
                'data': [POST],
                'upload': POST.get('extUpload') == 'true',
                'tid': POST.get('extTID')
            }

            if requests['upload']:
                requests['data'].append(request.FILES)
                output = simplejson.dumps(self.call_action(requests, user))
                return HttpResponse('<script>document.domain=document.domain;</script><textarea>%s</textarea>' \
                                    % output)
        else:
            requests = simplejson.loads(request.POST.keys()[0])

        if not isinstance(requests, list):
                requests = [requests]

        output = [self.call_action(rd, request, *args, **kwargs) for rd in requests]

        return HttpResponse(simplejson.dumps(output, cls=DjangoJSONEncoder), mimetype="application/json")

    def action_extra_kwargs(self, action, request, *args, **kwargs):
        if hasattr(action, '_extra_kwargs'):
            return action._extra_kwargs(request, *args, **kwargs)
        return {}

    def extra_kwargs(self, request, *args, **kwargs):
        return {
            #'user': request.user
            'request' : request
        }

    def call_action(self, rd, request, *args, **kwargs):
        method = rd['method']

        if not rd['action'] in self.actions:
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'result': {'error': 'Undefined action class'}
            }

        action = self.actions[rd['action']]
        args = rd.get('data') or []
        func = getattr(action, method)

        extra_kwargs = self.extra_kwargs(request, *args, **kwargs)
        extra_kwargs.update(self.action_extra_kwargs(action, request, *args, **kwargs))

        func_args, varargs, varkw, func_defaults = getargspec(func)
        if 'self' in func_args:
            func_args.remove('self')
        for name in extra_kwargs.keys():
            if name in func_args:
                func_args.remove(name)
        required_args_count = len(func_args) - len(func_defaults or [])
        if (required_args_count - len(args)) > 0 or (not varargs and len(args) > required_args_count):
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'result': {'error': 'Function %s. Incorrect arguments number %s. Declared: %s' % (method,len(args),required_args_count)}
            }

        return {
            'tid': rd['tid'],
            'type': 'rpc',
            'action': rd['action'],
            'method': method,
            'result': func(*args, **extra_kwargs)
        }