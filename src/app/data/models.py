# -*- coding: utf-8 -*-
from datetime import date, datetime
from django.db import models

class Status(models.Model):

    iac = models.ForeignKey("abon.Abonent", to_field="extid", db_column="iac", related_name="intervals")
    begin = models.DateField()
    end = models.DateField()
    start = models.DateField()
    finish = models.DateField()
    s1 = models.FloatField()
    s2 = models.FloatField()