Ext.ux.BalanceForm = Ext.extend(Ext.FormPanel, {
    initComponent: function(){
        var config = {
            border : true,
            width: 300,
            height: 180,
            buttons:[{
                icon: '/static/img/icons/green/16x16/Refresh.png',
                handler: function(){
					this.refresh()
                },
                scope: this
            },{
                icon: '/static/img/icons/green/16x16/Table.png',
                handler: function(){
					this.recalc()
                },
                scope: this
            },{
                icon: '/static/img/icons/red/16x16/ArrowRight.png',
                handler: function(){
                    Engine.menu.cashier.transfer.openForm(this.oid,this.parent_form.id)
                },
                scope: this
            },{
                text: 'оплата',
                handler: function(){
					Engine.menu.cashier.payment.openForm(this.oid,this.parent_form.id)
                },
                scope: this
            },{
                text: 'снятие',
                handler: function(){
                    Engine.menu.cashier.fee.openForm(this.oid,this.parent_form.id)
                },
                scope: this                
            }],
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        this.refresh()
                    },
                    scope: this
                }
            },
            refresh: function() {
            	this.body.dom.innerHTML='<div class="balance_digits_positive">...</div>';
            	AbonApi.balance_get({
                	uid: (this.oid || 0)
                },function (result,e) {
                	if (result.data.balance==null) {
                    	this.body.dom.innerHTML='<div class="balance_digits_negative">...</div>'
                    }
					else if (result.data.balance+result.data.credit<0) {
                    	this.body.dom.innerHTML='<div class="balance_digits_negative">'+result.data.balance+' грн.</div>'
                    } else {
                    	this.body.dom.innerHTML='<div class="balance_digits_positive">'+result.data.balance+' грн.</div>'
                    }
                    if (result.data.credit) {
                    	this.body.dom.innerHTML+='<div class="balance_digits_negative"><small><small><small>Кредит: '+result.data.credit+' грн.</small></small></small></div>'
                    }
            	}.createDelegate(this));
            },
            recalc: function() {
            	AbonApi.balance_set({
                	uid: (this.oid || 0)
                },function (result,e) {
                    this.refresh()
            	}.createDelegate(this));
            },
            scope: this
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AddressForm.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:balance-form', Ext.ux.BalanceForm);

