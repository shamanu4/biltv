Ext.ux.AddressForm = Ext.extend(Ext.FormPanel, {
    initComponent: function(){
        var config = {
            border : true,
            width: 400,
            height: 180,
            defaults: {
                frame: true,
                split: true,
                listeners: {
                    change : {
                        fn: function(obj) {
                            this.parent_form.children_forms.address.ready2=false
                        },
                        scope: this
                    }
                }
            },
            api: {
                load: AbonApi.address_get,
                submit: AbonApi.address_set
            },
            paramsAsHash: true,
            defaultType: 'textfield',
            items: [
            {
                name: 'address_id',
                hidden: true
            },
			this.form_street_field = {
                fieldLabel: 'Улица',
                name: 'street',
                allowBlank:false,
                xtype: 'ext:ux:street-combo'
            },
			this.form_house_field = {
                fieldLabel: 'Дом',
                name: 'house',
                allowBlank:false,
                xtype: 'ext:ux:house-combo'
            },
			this.form_flat_field = {
                fieldLabel: 'Квартира',
                name: 'flat',
                allowBlank:false,
                vtype:'decimal'
            },
			this.form_ext_field = {
                fieldLabel: 'Номер счёта',
                name: 'ext',
                allowBlank:false
            },
			this.form_phone_field ={
                fieldLabel: 'Дом. тел',
                name: 'phone',
                allowBlank:true
            }
			/*
			this.activated_field = new Ext.form.DateField({
                fieldLabel: 'Подключен',
                name: 'activated',
				xtype: 'datefield',
				format: 'Y-m-d',
                allowBlank: false
            }),
			this.deactivated_field = new Ext.form.DateField({
                fieldLabel: 'Отключен',
                name: 'deactivated',
				xtype: 'datefield',
				format: 'Y-m-d',
                allowBlank: true
            })
            */
			],
			
        /*
            buttons:[{
                text: 'ОК',
                handler: function(){
                    this.submitaction()
                },
                scope: this
            }],
        */
            loadaction: function() {
                this.getForm().load({
                    params: {
                        uid: (this.oid || 0)
                    },
                    success: function(form, action) {    
						this.parent_form.children_forms.address.ready2=true;
                        this.parent_form.children_forms.address.oid = action.result.data['id']
                    },
                    scope: this
                });
            },
            submitaction: function() {                
                this.getForm().submit({                    
                    params: {
                        uid: (this.oid || 0)
                    },
                    failure: function(form, action){
                        this.parent_form.children_forms.address.ready2=false;
                        this.parent_form.children_forms.address.oid=null
                    },
                    success: function(form, action){
                        this.parent_form.children_forms.address.ready2=true;
                        this.parent_form.children_forms.address.oid = action.result.data[0]['id'];
                        this.parent_form.children_forms_ready()
                    },
                    scope: this
                });
            },
            onShow: function() {
            	
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        this.parent_form.children_forms.address.obj=this;
                        if (this.oid) {
                            this.loadaction()
                        }                        
                    },
                    scope: this
                }
            }
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AddressForm.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:address-form', Ext.ux.AddressForm);

