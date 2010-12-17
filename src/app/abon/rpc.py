# -*- coding: utf-8 -*-

from extjs import store_read
from django.db.utils import IntegrityError

class AbonApiClass(object):

    @store_read
    def cities(self,request):
        from abon.models import City
        return City.objects.all()

    def cities_update(self,rdata,request):
        from abon.models import City
        errors = False
        for data in rdata['data']:
            print data
            try:
                c = City.objects.get(pk=data['id'])
            except City.DoesNotExist:
                return dict(success=True, ok=False, msg="city not found")
            else:
                del data['id']
                for property in data:
                    setattr(c,property,data[property])
                    try:
                        c.save()
                    except IntegrityError as error:
                        errors = True
        if not errors:
            return dict(success=True, ok=True, title="Сохранено", msg="saved", data={})
        else:            
            return dict(success=True, ok=False, title="Ошибка записи", msg=error[1].decode('utf8'), data={})
    cities_update._args_len = 1

    def cities_create(self,rdata,request):
        print request.POST
        from abon.models import City
        errors = False
        for data in rdata['data']:
            print data
            if 'id' in data:
                del data['id']
            c = City()
            for property in data:
                setattr(c,property,data[property])
                try:
                    c.save()
                except IntegrityError as errortext:
                    print detail
                    errors = True
        if not errors:
            return dict(success=True, ok=True, title="Сохранено", msg="saved", data={})
        else:
            return dict(success=True, ok=False, title="Ошибка записи", msg=error[1].decode('utf8'), data={})
    cities_create._args_len = 1

    def cities_destroy(self,rdata,request):
        print request.POST