# -*- coding: utf-8 -*-

from django.contrib import admin
from logger.models import Log

"""
Log
"""
class LogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Log, LogAdmin)