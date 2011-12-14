# -*- coding: utf-8 -*-

def send_cards():
    from tv.models import CardDigital
    cc = CardDigital.objects.all().order_by('id')
    for c in cc:
        c.send()