# -*- coding: utf-8 -*-

from extjs import RpcRouter, store_read
from tv.rpc import TvApiClass
from abon.rpc import AbonApiClass
from django.db.utils import IntegrityError

class MainApiClass(object):
    
    def hello(self, name, request):

        return {
            'title': 'Приветствие',
            'msg': 'Hello %s!' % name,            
            'success': True,
            'ok': True
        }
    
    hello._args_len = 1

    def is_authenticated(self, request):
        print request.session.session_key
        if request.user.is_authenticated():
            return {
                'authenticated': True,
                'active': request.user.is_active,
                'title': 'Приветствие',
                'msg': 'Hello %s!' % request.user,
                'success': True,
                'ok': True
            }
        else:
            return {
                'authenticated': False,
                'success': True,
                'ok':False
            }

    is_authenticated._args_len = 0

    def login(self, rdata, request):
        from forms import LoginForm

        form = LoginForm(rdata, request.user)
        if form.is_valid():
            return form.save(request)
        else:
            return dict(success=True, ok=False, title='Сбой авторизации.', msg='authorization data is invaid', errors=form._errors)

    login._form_handler = True

    def logout(self,request):
        from django.contrib.auth import logout

        logout(request)
        # msg handlead at client. title removed to prevent default msg handler
        # return dict(success=True, ok=True, title='Завершение работы.', msg='logged out.')
        return dict(success=True, ok=True, msg='logged out.')

    logout._args_len = 0

    def menu(self,request):
        from ui.components import MenuSection
        menuitems = []
        user = request.user
        if user.has_perm('tv.manage_trunk'):
            menuitems.append('scrambler')
        if user.has_perm('tv.manage_bills'):
            menuitems.append('cashier')
        menuitems.append('address')

        return dict(success=True, ok=True, menuitems=menuitems)
    
    menu._args_len = 0



class GridApiClass(object):

    def __init__(self,model):
        self.model = model

    @store_read
    def read(self,rdata,request):
        return self.model.objects.all()
    read._args_len = 1

    def update(self,rdata,request):
        errors = False
        for data in rdata['data']:
            print data
            try:
                c = self.model.objects.get(pk=data['id'])
            except self.model.DoesNotExist:
                return dict(success=True, ok=False, msg="object not found")
            else:
                del data['id']
                for property in data:
                    setattr(c,property,data[property])
                    try:
                        c.save()
                    except IntegrityError as error:
                        errors = True
        if not errors:
            print 'update ok'
            print dict(success=True, ok=True, title="Сохранено", msg="saved", data={})
            return dict(success=True, ok=True, title="Сохранено", msg="saved", data={})
        else:
            print 'update fail'
            print dict(success=True, ok=False, title="Ошибка записи", msg=error[1].decode('utf8'), data={})
            return dict(success=True, ok=False, title="Ошибка записи", msg=error[1].decode('utf8'), data={})
    update._args_len = 1

    def create(self,rdata,request):
        errors = False
        for data in rdata['data']:
            print data
            if 'id' in data:
                del data['id']
            c = self.model()
            for property in data:
                setattr(c,property,data[property])
                print c
                print c.__dict__
                try:
                    c.save()
                except IntegrityError as error:                    
                    errors = True
        if not errors:
            return dict(success=True, ok=True, title="Сохранено", msg="saved", data={})
        else:
            return dict(success=True, ok=False, title="Ошибка записи", msg=error[1].decode('utf8'), data={})
    create._args_len = 1

    def destroy(self,rdata,request):
        print request.POST


class Router(RpcRouter):
    
    def __init__(self):
        from abon.models import City
        self.url = 'ui:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'TvApi': TvApiClass(),
            'CityGrid': GridApiClass(City),
        }                
        self.enable_buffer = 50
