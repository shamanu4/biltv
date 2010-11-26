# -*- coding: utf-8 -*-

from django.db import models

class Model(models.Model):
    
    class Meta:
        abstract = True


    def delete(self, **kwargs):

        for related_model in self.related_models:

            if getattr(self,related_model).filter(deleted=0).count() > 0:
                if 'recursive' in kwargs and kwargs['recursive']:
                    for obj in getattr(self,related_model).filter(deleted=0):
                        obj.delete(**kwargs)
                    self.deleted=1
                    self.save()
                    return [True,"recursively deleted"]
                else:
                    return [False,"related objects found"]

            self.deleted=1
            self.save()
        
            return [True,"deleted"]


    def undelete(self, **kwargs):

        if 'recursive' in kwargs and kwargs['recursive']:
            for related_model in  self.related_models:
                for obj in getattr(self,related_model).filter(deleted=1):
                    obj.undelete(**kwargs)
                self.deleted=0
                self.save()
                return [True,"recursively restored"]
        else:
            self.deleted=0
            self.save()
            return [True,"restored"]
