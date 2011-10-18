# -*- coding: utf-8 -*-

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

def check_perm(perm):
    def decorator(func):
        def inner_decorator(*args, **kwargs):
            if 'request' in kwargs:
                request = kwargs['request']
                try:
                    if request.user.has_perm(perm):
                        return func(*args, **kwargs)
                    else:
                        return dict(success=False, title='Доступ запрещен', msg=u'user %s has not permission %s' % (request.user,perm), errors='' )
                except:
                    return dict(success=False, title='Доступ запрещен', msg=u'invalid arguments while permission check', errors='' )
        return wraps(func)(inner_decorator) 
    return decorator

def store_read(func):
    def wrapper(*args, **kwargs):
        from lib.functions import latinaze
        result = func(*args, **kwargs)
        rdata = args[1]
        if isinstance(result, tuple):
            result, extras = result
            success = True
        else:
            success = True
            extras = {}
        total=0
        if isinstance(result, QuerySet) or isinstance(result, QuerySetChain):                        
            if 'filter_fields' in rdata and 'filter_value' in rdata:
                query=None
                if 'query' in rdata:
                    for node in rdata['filter_fields']:
                        val=rdata['query']                    
                        if query:
                            query = query | Q(**{"%s__istartswith" % str(node):val})
                        else:
                            query = Q(**{"%s__istartswith" % str(node):val})
                if not rdata['filter_value']=='':                    
                    for node in rdata['filter_fields']:
                        if 'passport' in node:
                            val=latinaze(rdata['filter_value'])
                        else:
                            val=rdata['filter_value']
                        if query:
                            query = query | Q(**{"%s__icontains" % str(node):val})
                        else:
                            query = Q(**{"%s__icontains" % str(node):val})
                if query:
                    result = result.filter(query)
            if 'filter' in rdata:
                if not rdata['filter']=='':
                    result = result.filter(rdata['filter'])
            if 'sort' in rdata:
                if 'dir' in rdata and rdata['dir']=='DESC':
                    result = result.order_by('-%s' % rdata['sort'])
                else:
                    result = result.order_by('%s' % rdata['sort'])
            total = result.count()
            if 'start' in rdata and 'limit' in rdata:
                result = result[rdata['start']:rdata['start']+rdata['limit']]            
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