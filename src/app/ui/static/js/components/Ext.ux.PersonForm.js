Ext.ux.PersonForm = Ext.extend(Ext.FormPanel, {
    initComponent: function(){
        var config = {
            border : true,
            width: 300,
            height: 180,
            defaults: {
                frame: true,
                split: true,
                listeners: {
                    change : {
                        fn: function(obj) {
                            this.parent_form.children_forms.person.ready2=false
                        },
                        scope: this
                    }
                }
            },
            api: {
                load: AbonApi.person_get,
                submit: AbonApi.person_set
            },            
            paramsAsHash: true,
            defaultType: 'textfield',
            items: [
            {                
                name: 'person_id',
                hidden: true
            },
			this.form_passport_field = {
                fieldLabel: 'Паспорт',
                name: 'passport',
                allowBlank:false,
                listeners: {
                    change : {
                        fn: function(obj) {                             
                             this.passportseek(obj.getActionEl().getValue())
                        },
                        scope: this
                    }
                }
            },
			this.form_lastname_field ={
                fieldLabel: 'Фамилия',
                name: 'lastname',
                allowBlank:false
            },
			this.form_firstname_field ={
                fieldLabel: 'Имя',
                name: 'firstname',
                allowBlank:false
            },
			this.form_middlename_field ={
                fieldLabel: 'Отчество',
                name: 'middlename',
                allowBlank:false
            },
			this.form_mobile_phone_field ={
                fieldLabel: 'Моб. тел',
                name: 'phone',
                allowBlank:true
            }],
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
                    success: function(form, action){
                        this.parent_form.children_forms.person.ready2 = true;
                        this.parent_form.children_forms.person.oid = action.result.data['id']
                    },
                    scope: this
                });
                this.parent_form.children_forms.person.ready2=true
            },
            passportseek: function(passport) {
                this.getForm().load({
                    params: {
                        passport: (passport || 0)
                    },
                    success: function(form, action){
                        this.parent_form.children_forms.person.ready2 = true;
                        this.parent_form.children_forms.person.oid = action.result.data['id']
                    },
                    failure: function(form, action){
                        this.parent_form.children_forms.person.ready2=false;
                        this.parent_form.children_forms.person.oid=null
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
                        this.parent_form.children_forms.person.ready2=false;
                        this.parent_form.children_forms.person.oid=null
                    },
                    success: function(form, action){
                        this.parent_form.children_forms.person.ready2=true;
                        this.parent_form.children_forms.person.oid = action.result.data[0]['id'];
                        this.parent_form.children_forms_ready()
                    },
                    scope: this
                });
            },
            onShow: function() {
            	this.getForm().items.items[1].focus(false,100)
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        this.parent_form.children_forms.person.obj=this;
                        if(this.oid) {
                            this.loadaction()                            
                        }
						this.getForm().items.items[1].focus(false,100)              
                    },
                    scope: this
                }               
            }
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.PersonForm.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:person-form', Ext.ux.PersonForm );

