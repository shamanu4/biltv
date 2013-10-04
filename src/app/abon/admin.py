# -*- coding: utf-8 -*-

from django.contrib import admin
from abon.models import *

"""
class Group(extended.Model):
class Person(extended.Model):
class Contact(extended.Model):
class City(extended.Model):
class Street(extended.Model):
class House(extended.Model):
class Building(extended.Model):
class Address(extended.Model):
class Bill(extended.Model):
class Abonent(extended.Model):
"""

"""
Group
"""
class GroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(Group, GroupAdmin)

"""
Person
"""
class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person, PersonAdmin)

"""
Contact
"""
class ContactAdmin(admin.ModelAdmin):
    pass
admin.site.register(Contact, ContactAdmin)

"""
City
"""
class CityAdmin(admin.ModelAdmin):
    pass
admin.site.register(City, CityAdmin)

"""
Street
"""
class StreetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Street, StreetAdmin)

"""
House
"""
class HouseAdmin(admin.ModelAdmin):
    pass
admin.site.register(House, HouseAdmin)

"""
Building
"""
class BuildingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Building, BuildingAdmin)

"""
Address
"""
class AddressAdmin(admin.ModelAdmin):
    pass
admin.site.register(Address, AddressAdmin)

"""
Bill
"""
class BillAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bill, BillAdmin)

"""
Credit
"""
class CreditAdmin(admin.ModelAdmin):
    raw_id_fields=('bill',)
    search_fields=('bill__abonents__address__override','bill__abonents__person__lastname')
    list_display=('bill','sum','valid_from','valid_until','manager')
admin.site.register(Credit, CreditAdmin)


"""
Abonent
"""
class AbonentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Abonent, AbonentAdmin)


"""
Illegal
"""
class IllegalAdmin(admin.ModelAdmin):
    pass
admin.site.register(Illegal, IllegalAdmin)


