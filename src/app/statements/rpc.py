# -*- coding: utf-8 -*-

from lib.extjs import RpcRouter, store_read, check_perm

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
        if user.has_perm('abon.manage_bills'):
            menuitems.append('cashier')
        menuitems.append('address')

        return dict(success=True, menuitems=menuitems)

    menu._args_len = 0



class Router(RpcRouter):
    def __init__(self):
        self.url = 'statements:router'
        self.actions = {
            'MainApi': MainApiClass(),
        }
        self.enable_buffer = 50
