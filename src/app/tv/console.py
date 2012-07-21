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
        payments = autoreg.register.payments.filter(maked=False)
        for payment in payments:
            payment.make()

def fees_check():
    from app.tv.models import Fee, CardService
    for fee in Fee.objects.filter(maked__exact=False,deleted__exact=False,rolled_by__exact=None):
        print fee
        if not fee.card or not fee.tp:
            fee.make()
        else:
            try:
                cs = CardService.objects.get(card=fee.card,tp=fee.tp)
            except CardService.DoesNotExist:
                pass
            else:
                cs.activate(activated=fee.timestamp.date())
                fee.delete()

