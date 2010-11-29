# -*- coding: utf-8 -*-

from django.db import models

class Model(models.Model):
    
    class Meta:
        abstract = True


    def delete(self, *args, **kwargs):

            self.deleted=1
            self.save()        
            return [True,"deleted"]


    def undelete(self, *args, **kwargs):

            self.deleted=0
            self.save()
            return [True,"restored"]
