# -*- coding: utf-8 -*-

from extjs import RpcRouter
from tv.rpc import TvApiClass

class MainApiClass(object):
    
    def hello(self, name, request):

        return {
            'msg': 'Hello %s!' % name
        }
    
    hello._args_len = 1

    def is_authenticated(self, request):
        print request.session.session_key
        if request.user.is_authenticated():
            return {
                'authenticated': True,
                'active': request.user.is_active,
                'msg': 'Hello %s!' % request.user
            }
        else:
            return {
                'authenticated': False
            }

    is_authenticated._args_len = 0

    def login(self, rdata, request):
        from forms import LoginForm

        form = LoginForm(rdata, request.user)
        if form.is_valid():
            return form.save(request)
        else:
            return dict(success=False, errors=form._errors)

    login._form_handler = True

    def logout(self,request):
        from django.contrib.auth import logout

        logout(request)
        return dict(success=True, msg='logged out')

    logout._args_len = 0

    def menu(self,request):
        from ui.components import MenuSection
        menuitems = []
        user = request.user

        if user.has_perm('tv.manage_trunk'):
            menuitems.append(MenuSection['scrambler'])
        if user.has_perm('tv.manage_bills'):
            menuitems.append(MenuSection['cashier'])

        return dict(success=True, menuitems=menuitems)
    
    menu._args_len = 0


class Router(RpcRouter):
    
    def __init__(self):
        self.url = 'ui:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'TvApi': TvApiClass(),
        }
        self.enable_buffer = 50
