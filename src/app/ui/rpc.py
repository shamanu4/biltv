# -*- coding: utf-8 -*-

from extjs import RpcRouter, store_read
from tv.rpc import TvApiClass
from abon.rpc import AbonApiClass
from django.db.utils import IntegrityError
from django.db.models import Model

class MainApiClass(object):

    def is_authenticated(self, request):
        print request.session.session_key
        if request.user.is_authenticated():
            return dict(success=True, ok=True, authenticated=True, active=request.user.is_active, title='Приветствие', msg='Hello %s!' % request.user)
        else:
            return dict(success=False, ok=False, authenticated=False)

    is_authenticated._args_len = 0

    def login(self, rdata, request):
        from forms import LoginForm

        form = LoginForm(rdata, request.user)
        if form.is_valid():
            return form.save(request)
        else:
            return dict(success=False, ok=False, title='Сбой авторизации.', msg='authorization data is invaid', errors=form._errors)

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
    def read_one(self,oid):
        return self.model.objects.get(pk=oid)
    
    @store_read
    def read(self,rdata,request):
        return self.model.objects.all()
    read._args_len = 1

    def update(self,rdata,request):
        errors = False
        print rdata
        for data in rdata['data']:
            print data
            try:
                obj = self.model.objects.get(pk=data['id'])
            except self.model.DoesNotExist:
                print 'object not found'
                return dict(success=False, ok=False, msg="object not found")
            else:
                print obj
                print data
                if 'id' in data:
                    del data['id']
                for property in data:
                    print "%s=%s" % (property,data[property])
                    if not hasattr(obj, property):
                        continue;
                    if isinstance(getattr(obj,property),Model):
                        try:
                            data[property] = getattr(obj,property).__class__.objects.get(pk=data[property])
                        except getattr(obj,property).__class__.DoesNotExist:
                            errors = True
                    setattr(obj,property,data[property])
                if not errors:
                    try:
                        obj.save()
                    except IntegrityError as error:
                        errors = True
        if not errors:
            print 'update ok'
            return dict(success=True, ok=True, title="Сохранено", msg="saved", data={})
        else:
            print 'update fail'
            if error:
                msg = error[1].decode('utf8')
            else:
                msg = ""
            return dict(success=False, ok=False, title="Ошибка записи", msg=msg, data={})
    update._args_len = 1

    def create(self,rdata,request):
        errors = False
        nulldata = True
        result = []
        for data in rdata['data']:
            obj = self.model()
            print data
            if 'id' in data:
                del data['id']
            for property in data:
                print "%s=%s" % (property,data[property])
                if not hasattr(obj, property):
                    print "NO attr!"
                    for field in obj._meta.local_fields:
                        if field.name == property:
                            if hasattr(field,'related'):
                                parent = field.related.parent_model
                                try:
                                    rel = parent.objects.get(pk=data[property])
                                except parent.DoesNotExist:
                                    errors = True
                                else:
                                    setattr(obj,property,rel)
            if not errors and not nulldata:
                try:
                    obj.save()
                except IntegrityError as error:
                    errors = True
        if nulldata:
            return dict(success=False, ok=False, title="Ошибка записи",  msg="не заполнены обязательные поля", data={})
        if not errors:
            return dict(success=True, ok=True, title="Сохранено", msg="saved", data=result)
        else:
            return dict(success=False, ok=False, title="Ошибка записи", msg=error[1].decode('utf8'), data={})
    create._args_len = 1

    def destroy(self,rdata,request):
        print request.POST


class Router(RpcRouter):
    
    def __init__(self):
        from abon.models import City,Street
        self.url = 'ui:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'TvApi': TvApiClass(),
            'CityGrid': GridApiClass(City),
            'StreetGrid': GridApiClass(Street),
        }                
        self.enable_buffer = 50
