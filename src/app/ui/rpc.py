# -*- coding: utf-8 -*-

from extjs import RpcRouter, store_read
from tv.rpc import TvApiClass
from abon.rpc import AbonApiClass

class MainApiClass(object):

    def is_authenticated(self, request):
        print request.session.session_key
        if request.user.is_authenticated():
            return dict(success=True, authenticated=True, active=request.user.is_active, title='Приветствие', msg='Hello %s!' % request.user)
        else:
            return dict(success=False, authenticated=False)

    is_authenticated._args_len = 0

    def login(self, rdata, request):
        from forms import LoginForm
                
        form = LoginForm(rdata, request.user)
        if form.is_valid():
            return form.save(request)
        else:
            return dict(success=False, title='Сбой авторизации.', msg='authorization data is invaid', errors=form._errors)

    login._form_handler = True

    def logout(self,request):
        from django.contrib.auth import logout

        logout(request)
        # msg handlead at client. title removed to prevent default msg handler
        # return dict(success=True, title='Завершение работы.', msg='logged out.')
        return dict(success=True, msg='logged out.')

    logout._args_len = 0

    def menu(self,request):
        menuitems = []
        user = request.user
        if user.has_perm('tv.manage_trunk'):
            menuitems.append('scrambler')
        if user.has_perm('tv.manage_bills'):
            menuitems.append('cashier')
        menuitems.append('address')

        return dict(success=True, menuitems=menuitems)
    
    menu._args_len = 0



class GridApiClass(object):

    def __init__(self,model,form,filter=None):
        self.filter = filter
        self.model = model
        self.form = form

    @store_read
    def read_one(self,oid):
        return self.model.objects.get(pk=oid)
    
    @store_read
    def read(self,rdata,request):
        if self.filter:
            return self.model.objects.all().filter(self.filter)
        else:
            return self.model.objects.all()

    read._args_len = 1

    def update(self,rdata,request):
        if not self.form:
            return dict(success=False, title="Ошибка записи", msg="Только для чтения", data={})
        result = []
        data = rdata['data']
        try:
            obj = self.model.objects.get(pk=data['id'])
        except self.model.DoesNotExist:
            return dict(success=False, msg="object not found")
        else:
            form = self.form(data)
            if form.is_valid():
                res = form.save(obj)
                ok = res[0]
                result.append(res[1].store_record())
                msg = res[2]
            else:
                ok = False
                msg = form._errors
        if ok:
            return dict(success=True, title="Сохранено", msg="saved", data=result)
        else:
            return dict(success=False, title="Ошибка записи", msg=msg, data={})
    update._args_len = 1

    def create(self,rdata,request):
        if not self.form:
            return dict(success=False, title="Ошибка записи", msg="Только для чтения", data={})
        result = []
        data = rdata['data']
        form = self.form(data)
        if form.is_valid():
            res = form.save()
            ok = res[0]
            result.append(res[1].store_record())
            msg = res[2]
        else:
            ok = False
            msg = form._errors
        if ok:
            return dict(success=True, title="Сохранено", msg="saved", data=result)
        else:
            return dict(success=False, title="Ошибка записи", msg=msg, data={})
    create._args_len = 1

    def destroy(self,rdata,request):
        print request.POST

    def foo(self,rdata,request):
        print rdata

class Router(RpcRouter):
    
    def __init__(self):
        from abon.models import City,Street,House,Building,Abonent
        from tv.models import Card, PaymentRegister, PaymentSource
        from abon.forms import CityForm,StreetForm,HouseNumForm,BuildingForm
        from tv.forms import CardForm, RegisterForm
        from django.db.models import Q
        self.url = 'ui:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'TvApi': TvApiClass(),
            'AbonApi':  AbonApiClass(),
            'CityGrid': GridApiClass(City,CityForm),
            'StreetGrid': GridApiClass(Street,StreetForm),
            'HouseNumGrid': GridApiClass(House,HouseNumForm),
            'BuildingGrid': GridApiClass(Building,BuildingForm),
            'AbonentGrid': GridApiClass(Abonent,None),
            'CardGrid':GridApiClass(Card,CardForm,Q(**{"num__gte":0})),
            'RegisterGrid':GridApiClass(PaymentRegister,RegisterForm),
            'SourceGrid':GridApiClass(PaymentSource,None),
        }                
        self.enable_buffer = 50
