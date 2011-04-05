from django.contrib.auth.models import UserManager, User as BaseUser
from django.db import models
from django.db.models.signals import post_save

class User(BaseUser):

    icq = models.DecimalField(max_digits=9, decimal_places=0, blank=True, null=True)

    objects = UserManager()
    
    def store_record(self):
        print self
        print self.__dict__
        obj = {}
        obj['id'] = self.pk
        obj['username'] = self.first_name or self.username 
        return obj

def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = User(**values)
        user.save()
        
post_save.connect(create_custom_user, BaseUser)