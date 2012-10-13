# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from tv.models import *
from django.db.models import Q

"""
Trunk
"""
class TrunkChannelRelationshipInlineForm(forms.ModelForm):
    class Meta:
        model = TrunkChannelRelationship

    def __init__(self, *args, **kwargs):
        super(TrunkChannelRelationshipInlineForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            rel = kwargs['instance']            
        else:
            rel=None
        self.fields['channel'].queryset = Channel.objects.filter(Q(bound=None)|Q(trunkchannelrelationship=rel))

class TrunkChannelRelationshipInline(admin.TabularInline):
    model = TrunkChannelRelationship
    form = TrunkChannelRelationshipInlineForm
    extra = 16
    max_num = 16

class TrunkAdmin(admin.ModelAdmin):
    inlines = (TrunkChannelRelationshipInline,)
admin.site.register(Trunk, TrunkAdmin)


"""
Channel
"""
class ChannelAdmin(admin.ModelAdmin):
    pass
admin.site.register(Channel, ChannelAdmin)



"""
TrunkChannelRelationship
"""
def make_encoded(modeladmin, request, queryset):
    queryset.update(encoded=True)
make_encoded.short_description = "Encode selected channels"

def make_decoded(modeladmin, request, queryset):
    queryset.update(encoded=False)
make_decoded.short_description = "Decode selected channels"

class TrunkChannelRelationshipAdmin(admin.ModelAdmin):
    actions = [make_encoded,make_decoded]
admin.site.register(TrunkChannelRelationship, TrunkChannelRelationshipAdmin)



"""
TariffPlanFeeRelationship
"""
class TariffPlanFeeRelationshipAdmin(admin.ModelAdmin):
    pass
admin.site.register(TariffPlanFeeRelationship, TariffPlanFeeRelationshipAdmin)


"""
FeeType
"""
class FeeTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(FeeType, FeeTypeAdmin)


"""
TariffPlan
"""

class TariffPlanChannelRelationshipInlineForm(forms.ModelForm):
    class Meta:
        model = TariffPlanChannelRelationship

class TariffPlanChannelRelationshipInline(admin.TabularInline):
    model = TariffPlanChannelRelationship
    form = TariffPlanChannelRelationshipInlineForm
    extra = 1

class TariffPlanFeeRelationshipInlineForm(forms.ModelForm):
    class Meta:
        model = TariffPlanFeeRelationship

class TariffPlanFeeRelationshipInline(admin.TabularInline):
    model = TariffPlanFeeRelationship
    form = TariffPlanFeeRelationshipInlineForm
    extra = 1

class TariffPlanAdmin(admin.ModelAdmin):
    inlines = (TariffPlanChannelRelationshipInline,TariffPlanFeeRelationshipInline)
    list_display=('__unicode__','allow_restore','fallback_tp')
admin.site.register(TariffPlan, TariffPlanAdmin)


"""
TariffPlanChannelRelationship
"""
class TariffPlanChannelRelationshipAdmin(admin.ModelAdmin):
    pass
admin.site.register(TariffPlanChannelRelationship, TariffPlanChannelRelationshipAdmin)


"""
Card
"""
class CardServiceInlineForm(forms.ModelForm):
    class Meta:
        model = CardService
        fields = ('tp', 'active')
        
class CardServiceInline(admin.TabularInline):
    model = CardService    
    form = CardServiceInlineForm
    extra = 1

class CardAdmin(admin.ModelAdmin):
    raw_id_fields=('owner',)
    search_fields=('num',)
    list_display=('num','active','owner')
    inlines = (CardServiceInline,)
    
    def queryset(self, request):
        qs = super(CardAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(num__gte=0)

    
admin.site.register(Card, CardAdmin)


"""
CardService
"""
class CardServiceAdmin(admin.ModelAdmin):
    raw_id_fields=('card',)
admin.site.register(CardService, CardServiceAdmin)

"""
CardHistory
"""
class CardHistoryAdmin(admin.ModelAdmin):
    raw_id_fields=('owner','card')
admin.site.register(CardHistory, CardHistoryAdmin)


"""
Fee
"""
class FeeAdmin(admin.ModelAdmin):
    raw_id_fields=(
        'bill',
        'rolled_by',
    )
admin.site.register(Fee, FeeAdmin)

"""
FeeIntervals
"""
class FeeIntervalsAdmin(admin.ModelAdmin):
    pass
admin.site.register(FeeIntervals, FeeIntervalsAdmin)

"""
FeeRanges
"""
class FeeRangesAdmin(admin.ModelAdmin):
    pass
admin.site.register(FeeRanges, FeeRangesAdmin)

"""
FeeCustomRanges
"""
class FeeCustomRangesAdmin(admin.ModelAdmin):
    list_filter=('fee_type','interval')
admin.site.register(FeeCustomRanges, FeeCustomRangesAdmin)

"""
Payment
"""
class PaymentAdmin(admin.ModelAdmin):
    raw_id_fields=(
        'bill',
        'rolled_by',
        'register',
    )
admin.site.register(Payment, PaymentAdmin)

"""
PaymentSource
"""
class PaymentSourceAdmin(admin.ModelAdmin):
    pass
admin.site.register(PaymentSource, PaymentSourceAdmin)

"""
PaymentRegister
"""
class PaymentRegisterAdmin(admin.ModelAdmin):
    pass
admin.site.register(PaymentRegister, PaymentRegisterAdmin)

"""
PromotionLink
"""
class PromotionLinkAdmin(admin.ModelAdmin):
    list_display=('tp','abills_tp')
admin.site.register(PromotionLink, PromotionLinkAdmin)

"""
PaymentAutoMake
"""
class PaymentAutoMakeAdmin(admin.ModelAdmin):
    pass
admin.site.register(PaymentAutoMake, PaymentAutoMakeAdmin)
