# -*- coding: utf-8 -*-

def send_cards():
    from app.tv.models import CardDigital
    cc = CardDigital.objects.all().order_by('id')
    for c in cc:
        c.send()

def payments_automake():
    from app.tv.models import PaymentAutoMake
    autoregs = PaymentAutoMake.objects.all()
    for autoreg in autoregs:
        payments = autoreg.payments.filter(maked=False)
        for payment in payments:
            payment.make()

