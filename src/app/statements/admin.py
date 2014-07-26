# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from .models import Statement, Entry, Category, Filter
from django.contrib import admin


"""
Statement
"""
class StatementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Statement, StatementAdmin)


"""
Entry
"""
class EntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Entry, EntryAdmin)


"""
Category
"""
class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)


"""
Filter
"""
class FilterAdmin(admin.ModelAdmin):
    pass
admin.site.register(Filter, FilterAdmin)
