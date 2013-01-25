from django.contrib.auth.models import UserManager, User as BaseUser
from django.db import models
from django.db.models.signals import post_save

class User(BaseUser):

    icq = models.DecimalField(max_digits=9, decimal_places=0, blank=True, null=True)
    objects = UserManager()
    
    class Meta:
        permissions = (
            ("rpc_read_generic_grid", "RPC read generic grid"),
            ("rpc_update_generic_grid", "RPC update generic grid"),
            ("rpc_add_in_generic_grid", "RPC add in generic grid"),
            ("rpc_delete_in_generic_grid", "RPC delete in generic grid"),
            ("rpc_abon_person_get", "RPC abon.person_get"),
            ("rpc_abon_person_set", "RPC abon.person_set"),
            ("rpc_abon_address_get", "RPC abon.address_get"),
            ("rpc_abon_address_set", "RPC abon.address_set"),
            ("rpc_abon_abonent_get", "RPC abon.abonent_get"),
            ("rpc_abon_abonent_get_by_code", "RPC abon.abonent_get_by_code"),
            ("rpc_abon_abonent_set", "RPC abon.abonent_set"),
            ("rpc_abon_enable", "RPC abon.enable"),
            ("rpc_abon_disable", "RPC abon.disable"),
            ("rpc_abon_balance_get", "RPC abon.balance_get"),
            ("rpc_abon_cards_get", "RPC abon.cards_get"),
            ("rpc_abon_abon_history_get", "RPC abon.abon_history_get"),
            ("rpc_abon_cards_set", "RPC abon.cards_set"),
            ("rpc_abon_free_cards_get", "RPC abon.free_cards_get"),
            ("rpc_abon_cards_tp_get", "RPC abon.cards_tp_get"),
            ("rpc_abon_cards_tp_set", "RPC abon.cards_tp_set"),
            ("rpc_abon_payments_get", "RPC abon.payments_get"),
            ("rpc_abon_fees_get", "RPC abon.fees_get"),
            ("rpc_abon_registers_get", "RPC abon.registers_get"),
            ("rpc_abon_registers_get_last", "RPC abon.registers_get_last"),
            ("rpc_abon_make_payment", "RPC abon.make_payment"),
            ("rpc_abon_make_double_payment", "RPC abon.make_double_payment"),
            ("rpc_abon_feetypes_get", "RPC abon.feetypes_get"),
            ("rpc_abon_make_fee", "RPC abon.make_fee"),
            ("rpc_abon_make_transfer", "RPC abon.make_transfer"),
            ("rpc_abon_payment_rollback", "RPC abon.payment_rollback"),
            ("rpc_abon_fee_rollback", "RPC abon.fee_rollback"),
            ("rpc_abon_reg_payments_get", "RPC abon.reg_payments_get"),
            ("rpc_abon_reg_payments_delete", "RPC abon.reg_payments_delete"),
            ("rpc_abon_reg_payments_partially_confirm", "RPC abon.reg_payments_partially_confirm"),
            ("rpc_abon_history_delete", "RPC abon.history_delete"),
            ("rpc_abon_admins_get", "RPC abon.admins_get"),
            ("rpc_abon_comment_get", "RPC abon.comment_get"),
            ("rpc_abon_comment_set", "RPC abon.comment_set"),
            ("rpc_abon_launch_hamster", "RPC abon.launch_hamster"),
            ("rpc_abon_abonent_delete", "RPC abon.abonent_delete"),
            ("rpc_abon_credits_get", "RPC abon.credit_get"),
            ("rpc_abon_credits_set", "RPC abon.credit_set"),
            ("rpc_abon_sched_get", "RPC abon.sched_get"),
            ("rpc_abon_sched_add", "RPC abon.sched_add"),
            ("rpc_abon_sched_update", "RPC abon.sched_update"),
            ("rpc_abon_sched_delete", "RPC abon.sched_delete"),
        )
    
    def store_record(self):
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