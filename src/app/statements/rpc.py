# -*- coding: utf-8 -*-

from lib.extjs import RpcRouter, store_read, check_perm
from ui.rpc import GridApiClass
from .forms import EntryForm
from ui.forms import LoginForm
from .models import Entry, Statement, Category
from django.db.models import Q


class MainApiClass(object):
    def is_authenticated(self, request):
        print request.session.session_key
        if request.user.is_authenticated():
            return dict(success=True, authenticated=True, active=request.user.is_active, title='Приветствие',
                        msg='Hello %s!' % request.user)
        else:
            return dict(success=False, authenticated=False)
    is_authenticated._args_len = 0

    def login(self, rdata, request):
        form = LoginForm(rdata, request.user)
        if form.is_valid():
            return form.save(request)
        else:
            return dict(success=False, title='Сбой авторизации.', msg='authorization data is invaid',
                        errors=form._errors)
    login._form_handler = True

    def logout(self, request):
        from django.contrib.auth import logout

        logout(request)
        # msg handlead at client. title removed to prevent default msg handler
        # return dict(success=True, title='Завершение работы.', msg='logged out.')
        return dict(success=True, msg='logged out.')
    logout._args_len = 0

    @store_read
    @check_perm('accounts.rpc_update_generic_grid')
    def get_categories(self, day, request):
        try:
            st = Statement.objects.get(day=day)
        except Statement.DoesNotExist:
            return []
        else:
            return Category.objects.filter(lines__statement=st).distinct()
    get_categories._args_len = 1

    @store_read
    @check_perm('accounts.rpc_update_generic_grid')
    def get_available_categories(self, rdata, request):
        day = rdata.get('day', None)
        if not day:
            return []
        try:
            st = Statement.objects.get(day=day)
        except Statement.DoesNotExist:
            return []
        else:
            existent = map(lambda x: x.pk, Category.objects.filter(lines__statement=st).distinct())
            return Category.objects.filter(~Q(pk__in=existent))
    get_available_categories._args_len = 1

    @check_perm('accounts.rpc_update_generic_grid')
    def set_entry_category(self, entry_id, category_id, request):
        try:
            e = Entry.objects.get(pk=entry_id)
        except Entry.DoesNotExist:
            return dict(success=False, title='Ошибка', msg=str('no entry with id %s' % entry_id))
        else:
            if e.processed:
                return dict(success=False, title='Ошибка', msg=str('Entry with id %s already processed' % entry_id))
            if category_id>0:
                try:
                    c = Category.objects.get(pk=category_id)
                except Category.DoesNotExist:
                    return dict(success=False, title='Ошибка', msg=str('no category with id %s' % category_id))
                else:
                    e.category = c
                    e.save()
            else:
                e.category = None
                e.save()
            return dict(success=True)
    set_entry_category._args_len = 2

    @check_perm('accounts.rpc_update_generic_grid')
    def create_register(self, category_id, request):
        try:
            c = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return dict(success=False, title='Ошибка', msg=str('no category with id %s' % category_id))
        else:
            if not c.can_create_register():
                return dict(success=False, title='Ошибка', msg=str('category with id %s cant create register' % category_id))
            else:
                register = c.create_register()
                return dict(success=True, title="Создан реестр №%s" % register.pk, msg=str("created register #%s" % register.pk))
    create_register._args_len = 1

    @check_perm('accounts.rpc_update_generic_grid')
    def update_stats(self, category_id, statement_id, request):
        if category_id>0:
            try:
                c = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                return dict(success=False, title='Ошибка', msg=str('no category with id %s' % category_id))
            else:
                return c.store_record()
        elif statement_id>0:
            try:
                st = Statement.objects.get(pk=statement_id)
            except Statement.DoesNotExist:
                return dict(success=False, title='Ошибка', msg=str('no statement with id %s' % statement_id))
            else:
                pass
    update_stats._args_len = 2


class Router(RpcRouter):
    def __init__(self):
        self.url = 'statements:router'
        self.actions = {
            'MainApi': MainApiClass(),
            'EntryGrid': GridApiClass(Entry, EntryForm),
        }
        self.enable_buffer = 50
