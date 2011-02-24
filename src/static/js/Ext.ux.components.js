Ext.ux.msg = function(){
    var msgCt;
    function createBox(title, text, type){
        return ['<div class="msg">',
                '<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
                '<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc">',
                '<div class="ext-mb-icon ', type ,'">',
                '<h3>', title, '</h3>', text,
                '</div></div></div></div>',
                '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
                '</div>'].join('');
    }

    return function(title, text, type, callback){
        if(type=="ext-mb-error") {
            var delay = 10;
        } else {
            var delay = 3
        }
        if(!msgCt){
            msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
        }
        msgCt.alignTo(document, 't-t');
        var m = Ext.DomHelper.append(msgCt, {html:createBox(title, text, type)}, true);
        if(Ext.isFunction(callback)) {
            m.slideIn('t').pause(delay).ghost("t", {remove:true,callback:callback});
        } else {
            m.slideIn('t').pause(delay).ghost("t", {remove:true});
        }
    }
}();


Ext.ux.LoginForm = Ext.extend(Ext.form.FormPanel,{
    frame:
        true,
    // configs for FormPanel
    width: 300,
    height: 160,
    padding: 10,
    initComponent: function(){
        var config = {
            buttons:[{
                text: 'ОК',
                handler: function(){
                    this.submitaction()
                },
                scope: this
            }],

            submitaction: function() {
                this.getForm().submit({
                    failure: function(form, action){
                        if(this.getForm().isValid()) {
                            // Ext.ux.msg('Ошибка авторизации', action.result.msg, Ext.Msg.ERROR);
                        } else {
                            Ext.ux.msg('Ошибка ввода', 'обязательные поля не заполнены', Ext.Msg.ERROR);
                        }
                        this.ownerCt.loginFailed()
                        this.getForm().reset()
                    },
                    success: function(form, action){
                        // Ext.ux.msg('Авторизация успешная', action.result.msg, Ext.Msg.INFO);
                        this.ownerCt.loginSuccess()
                        this.ownerCt.close()
                    },
                    scope: this
                });
            },

            keys: [
                {
                    key: [Ext.EventObject.ENTER], handler: function() {                      
                        this.submitaction()
                    },
                    scope: this
                }
            ],

            defaults: {anchor: '100%'},
            defaultType: 'textfield',
            items: [{
                fieldLabel: 'Логин',
                allowBlank: false,
                name: 'username'
            },{
                fieldLabel: 'Пароль',
                allowBlank: false,
                name: 'password',
                inputType: 'password'
            }],

            // configs for BasicForm
            api: {
                submit: MainApi.login
            },
            clientValidation: true,
            paramsAsHash: true
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.LoginForm.superclass.initComponent.apply(this, arguments);
    }//initComponent    
});


Ext.ux.LoginWindow = Ext.extend(Ext.Window,{
    initComponent: function(){
        var config = {
            title: '"ТРК "TIM" вход в защищённую зону',
            layout: 'fit',
            height: 140,
            width: 260,
            closable: false,
            resizable: false,
            draggable: false,
            items: [new Ext.ux.LoginForm()]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.LoginWindow.superclass.initComponent.apply(this, arguments);
    },
    loginSuccess: function() {},
    loginFailed: function() {}
});


Ext.ux.TabPanel = Ext.extend(Ext.TabPanel,{
    initComponent: function(){
        var config = {
            frame:true
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.TabPanel.superclass.initComponent.apply(this, arguments);
    }
});

Ext.ux.menu = {
    'scrambler': [
        {
            'xtype': 'tbseparator'
        },{
            'id': 'menu-scrambler-button',
            'xtype': 'tbbutton',
            'text': 'Скрамблер',
            'menu': [
                {
                    'text': 'Каналы',
                    'handler': Engine.menu.address.city.openGrid,
                    'text': 'Города'
                },{
                    'text': 'Стволы'
                },
            ]
        }
    ],
    'cashier': [
        {
            'xtype': 'tbseparator'
        },{
            'id': 'menu-cashier-button',
            'xtype': 'tbbutton',
            'text': 'Касса',
            'menu': [
                {
                    'id': 'menu-cashier-abonent-button',
                    'handler': Engine.menu.cashier.abonent.openGrid,
                    'text': 'Пользователи'
                },{
                    'text': 'Item Two'
                },{
                    'text': 'Item Three'
                }
            ]
        }
    ],
    'address': [
        {
            'xtype': 'tbseparator'
        },{
            'id': 'menu-address-button',
            'xtype': 'tbbutton',
            'text': 'Адрес',
            'menu': [
                {
                    'id': 'menu-address-city-button',
                    'handler': Engine.menu.address.city.openGrid,
                    'text': 'Города'
                },{
                    'id': 'menu-address-street-button',
                    'handler': Engine.menu.address.street.openGrid,
                    'text': 'Улицы'
                },{
                    'id': 'menu-address-house-button',
                    'handler': Engine.menu.address.house.openGrid,
                    'text': 'Номера домов'
                },{
                    'id': 'menu-address-building-button',
                    'handler': Engine.menu.address.building.openGrid,
                    'text': 'Дома'
                }
            ]
        }
    ]
}

Ext.ux.MenuBar = Ext.extend(Ext.Toolbar,{
    initComponent: function(){
        var config = {
            items: [
                {
                    id: 'menu-exit-button',
                    xtype: 'tbbutton',
                    disabled: true,
                    text: 'Выход',
                    handler: Engine.auth.doLogout
                }
            ]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.MenuBar.superclass.initComponent.apply(this, arguments);
    }
});


Ext.ux.CustomGridNE = Ext.extend(Ext.grid.EditorGridPanel,{
    store: null,
    ds_model: null,
    columns: [],
    height: 500,
    boxMaxWidth: 1000,
    instance: null,
    viewConfig: {
        //forceFit:true
    },
    onRender:function() {
        Ext.ux.CustomGrid.superclass.onRender.apply(this, arguments);
        this.store.client=this;
        this.store.load();
    },
    addAction: function() {
        // overrides in instance
    },
    initComponent: function(){
        var config = {
            frame:true,
            closable: true,
            tbar: [
            {
                text: 'Add',
                icon: '/static/extjs/custom/plus_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.addAction()
                },
                scope: this
            },
            new Ext.Toolbar.Spacer(),
            this.searchfield = new Ext.form.TextField(),
            new Ext.Toolbar.Spacer(),
            {
                icon: '/static/extjs/custom/search_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.store.baseParams.filter_value = this.searchfield.getValue()
                    this.store.reload()
                },
                scope: this
            },{
                icon: '/static/extjs/custom/delete_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchfield.setValue('')
                    this.store.baseParams.filter_value = ''
                    this.store.reload()
                },
                scope: this
            },
            ],
            bbar: new Ext.PagingToolbar({
                pageSize: 16,
                store: this.store
            }),
            listeners: {
                    afterrender: {
                        fn: function(obj) {
                            //this.searchfield.addListener('click',function() { alert(2);debugger; });
                            //debugger;
                        }
                    },
                    beforeclose: {
                        fn: function(obj) {
                            obj.hide()
                        }
                    },
                    beforedestroy: {
                        fn: function(e) {
                            return false;
                        }
                    }
            }            
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.CustomGrid.superclass.initComponent.apply(this, arguments);
    }
});

Ext.ux.CustomGrid = Ext.extend(Ext.grid.EditorGridPanel,{
    store: null,
    ds_model: null,
    columns: [],
    height: 500,
    boxMaxWidth: 1000,
    instance: null,
    viewConfig: {
        //forceFit:true
    },
    onRender:function() {
        Ext.ux.CustomGrid.superclass.onRender.apply(this, arguments);
        this.store.client=this;
        this.store.load();
    },
    onWrite: function(result) {
        if(result.success) {
            //this.store.commitChanges();
        } else {
            this.selModel.selectRow(this.unsaved_row)
        }
    },
    initComponent: function(){
        var config = {
            frame:true,
            closable: true,
            current_row: 0,
            unsaved_row: 0,            
            tbar: [{
                text: 'Apply',
                icon: '/static/extjs/custom/tick_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {		    
                    this.store.save()
                    //this.store.commitChanges();
                },
                scope: this
            },{
                text: 'Add',
                icon: '/static/extjs/custom/plus_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.store.insert(
                        0,
                        new this.ds_model()
                    );
                    this.startEditing(0,1);
                },
                scope: this
            },{
                text: 'Cancel',
                icon: '/static/extjs/custom/block_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.store.reload()
                },
                scope: this
            },
            new Ext.Toolbar.Spacer(),
            this.searchfield = new Ext.form.TextField(),
            new Ext.Toolbar.Spacer(),
            {
                icon: '/static/extjs/custom/search_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.store.baseParams.filter_value = this.searchfield.getValue()
                    this.store.reload()                  
                },
                scope: this
            },{
                icon: '/static/extjs/custom/delete_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchfield.setValue('')
                    this.store.baseParams.filter_value = ''
                    this.store.reload()
                },
                scope: this
            },
            ],
            bbar: new Ext.PagingToolbar({
                pageSize: 16,
                store: this.store
            }),
            listeners: {
                    beforeclose: {
                        fn: function(obj) {
                            obj.hide()
                        }
                    },
                    beforedestroy: {
                        fn: function(e) {
                            return false;
                        }
                    }
            },
            sm: new Ext.grid.RowSelectionModel({
                singleSelect: true,
                listeners: {
                    rowselect: {
                        fn: function(sm,index,record) {                            
                            //if(this.current_row != index) {
                            //    this.unsaved_row = this.current_row
                            //    this.current_row = index
                            //    this.store.save()
                            //    //this.store.commitChanges();
                            //}
                        },
                        scope: this
                    }
                }
            })
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.CustomGrid.superclass.initComponent.apply(this, arguments);
    }
});

Ext.ux.CityGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'cities-store',
            ds_model: cities_ds_model,
            title: 'Города',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Name", dataIndex: 'name', editor: new Ext.form.TextField()},
                {header: "Label", dataIndex: 'label', editor: new Ext.form.TextField()},
                {header: "Comment", dataIndex: 'comment', editor: new Ext.form.TextField()},
            ]
});

Ext.ux.StreetGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'streets-store',
            ds_model: streets_ds_model,
            title: 'Улицы',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "City", dataIndex: 'city',
                    editor: new Ext.form.ComboBox({
                        store: Ext.ux.cities_combo_store,
                        editable: true,
                        lazyRender: false,
                        triggerAction: 'all',
                        valueField: 'id',
                        displayField: 'name',
                        mode: 'local'
                    }),
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                         var index = Ext.ux.cities_combo_store.find('id',value)
                         if (index>=0) {
                            return Ext.ux.cities_combo_store.getAt(index).data.name
                         } else {
                            return 'undefined'
                         }
                    },                    
                    scope: this
                },
                {header: "Name", dataIndex: 'name', editor: new Ext.form.TextField()},
                {header: "Code", dataIndex: 'code', editor: new Ext.form.TextField()},
                {header: "Comment", dataIndex: 'comment', editor: new Ext.form.TextField()},
            ]
});

Ext.ux.HouseNumGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'house-num-store',
            ds_model: house_num_ds_model,
            title: 'Номера домов',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Num", dataIndex: 'num', editor: new Ext.form.TextField()},
                {header: "Code", dataIndex: 'code', editor: new Ext.form.TextField()},
                {header: "Comment", dataIndex: 'comment', editor: new Ext.form.TextField()},
            ]
});

Ext.ux.BuildingGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'building-store',
            ds_model: building_ds_model,
            title: 'Дома',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Street", dataIndex: 'street',
                    editor: new Ext.form.ComboBox({
                        store: Ext.ux.streets_combo_store,
                        editable: true,
                        lazyRender: false,
                        triggerAction: 'all',
                        valueField: 'id',
                        displayField: 'name',
                        mode: 'local'
                    }),
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                         var index = Ext.ux.streets_combo_store.find('id',value)
                         if (index>=0) {
                            return Ext.ux.streets_combo_store.getAt(index).data.name
                         } else {
                            return 'undefined'
                         }
                    },
                    scope: this
                },
                {header: "House", dataIndex: 'house',
                    editor: new Ext.form.ComboBox({
                        store: Ext.ux.houses_combo_store,
                        editable: true,
                        lazyRender: false,
                        triggerAction: 'all',
                        valueField: 'id',
                        displayField: 'num',
                        mode: 'local'
                    }),
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                         var index = Ext.ux.houses_combo_store.find('id',value)
                         if (index>=0) {
                            return Ext.ux.houses_combo_store.getAt(index).data.num
                         } else {
                            return 'undefined'
                         }
                    },
                    scope: this
                },                
                {header: "Comment", dataIndex: 'comment', editor: new Ext.form.TextField()},
            ]
});

Ext.ux.AbonentGrid = Ext.extend(Ext.ux.CustomGridNE ,{
            store: 'abonent-store',
            title: 'Список абонентов',
            columns: [
                {header: "Id", dataIndex: 'id', width:100},
                {header: "Code", dataIndex: 'code', width:100},
                {header: "Person", dataIndex: 'person', width:300},
                {header: "Passport", dataIndex: 'passport', width:100},
                {header: "Address", dataIndex: 'address', width:300},
                //{header: "Comment", dataIndex: 'comment'},
                {header: " ", dataIndex: 'id', width: 28,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {                        
                        return '<div class="inline_edit_button abonent_edit_button" id="'+value+'" code="'+record.data.code+'"></div>'
                    }
                },
            ],
            addAction: function(){
                Engine.menu.cashier.abonent.openForm()
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        $(".abonent_edit_button").live('click', function(e) {
                            Engine.menu.cashier.abonent.openForm(this.id,$(this).attr('code'));
                        })
                    }
                }
            }
});

/*
 *  Forms and panels
 */

Ext.ux.PersonForm = Ext.extend(Ext.FormPanel, {
    initComponent: function(){
        var config = {
            border : true,
            width: 500,
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
            },{
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
            },{
                fieldLabel: 'Фамилия',
                name: 'lastname',
                allowBlank:false
            },{
                fieldLabel: 'Имя',
                name: 'firstname',
                allowBlank:false
            },{
                fieldLabel: 'Отчество',
                name: 'middlename',
                allowBlank:false
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
                        this.parent_form.children_forms.person.ready2 = true
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
                        this.parent_form.children_forms.person.ready2 = true
                        this.parent_form.children_forms.person.oid = action.result.data['id']
                    },
                    failure: function(form, action){
                        this.parent_form.children_forms.person.ready2=false
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
                        this.parent_form.children_forms.person.ready2=false
                        this.parent_form.children_forms.person.oid=null
                    },
                    success: function(form, action){
                        this.parent_form.children_forms.person.ready2=true
                        this.parent_form.children_forms.person.oid = action.result.data[0]['id']
                        this.parent_form.children_forms_ready()
                    },
                    scope: this
                });
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        this.parent_form.children_forms.person.obj=this
                        if(this.oid) {
                            this.loadaction()                            
                        }                        
                    },
                    scope: this
                }
            }
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.PersonForm.superclass.initComponent.apply(this, arguments);
    }
})

Ext.reg('ext:ux:person-form', Ext.ux.PersonForm );


Ext.ux.StreetCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.streets_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'name',
            mode: 'local'
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.StreetCombo.superclass.initComponent.apply(this, arguments);
    }
}),

Ext.reg('ext:ux:street-combo', Ext.ux.StreetCombo);


Ext.ux.HouseCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.houses_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'num',
            mode: 'local'
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.HouseCombo.superclass.initComponent.apply(this, arguments);
    }
}),

Ext.reg('ext:ux:house-combo', Ext.ux.HouseCombo);

Ext.apply(Ext.form.VTypes, {
    decimal:  function(v) {
        return /^\d{1,3}$/.test(v);
    },
    decimalText: 'Должно быть числом 0-999',
    decimalMask: /[\d]/i
});

Ext.ux.AddressForm = Ext.extend(Ext.FormPanel, {
    initComponent: function(){
        var config = {
            border : true,
            width: 500,
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
            },{
                fieldLabel: 'Улица',
                name: 'street',
                allowBlank:false,
                xtype: 'ext:ux:street-combo'
            },{
                fieldLabel: 'Дом',
                name: 'house',
                allowBlank:false,
                xtype: 'ext:ux:house-combo'
            },{
                fieldLabel: 'Квартира',
                name: 'flat',
                allowBlank:false,
                vtype:'decimal'
            },{
                fieldLabel: 'Ext',
                name: 'ext',
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
                    success: function(form, action) {                        
                        this.parent_form.children_forms.address.ready2=true
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
                        this.parent_form.children_forms.address.ready2=false
                        this.parent_form.children_forms.address.oid=null
                    },
                    success: function(form, action){
                        this.parent_form.children_forms.address.ready2=true
                        this.parent_form.children_forms.address.oid = action.result.data[0]['id']
                        this.parent_form.children_forms_ready()
                    },
                    scope: this
                });
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        this.parent_form.children_forms.address.obj=this
                        if (this.oid) {
                            this.loadaction()
                        }                        
                    },
                    scope: this
                }
            }
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AddressForm.superclass.initComponent.apply(this, arguments);
    }
})

Ext.reg('ext:ux:address-form', Ext.ux.AddressForm);

Ext.ux.AbonentForm = Ext.extend(Ext.Panel ,{
    initComponent: function() {
        var config = {
            closable: true,
            title: 'абонент '+(this.oid || 'новый'),
            layout: 'anchor',
            border : true,
            defaults: {
                frame: true,
                split: true,
                bodyStyle: 'padding:15px'
            },
            items: [{
                title: 'Абонент',
                region: 'west',
                xtype: 'ext:ux:person-form',
                oid: this.oid,
                parent_form: this
            },{
                title: 'Адреса',
                region: 'west',
                xtype: 'ext:ux:address-form',
                oid: this.oid,
                parent_form: this
            },{
                text: 'ОК',
                xtype: 'button',
                width: 100,
                handler: function(){
                    (function(){this.submitprep();}).defer(500,this);
                },
                scope: this
            }],
            submitprep: function() {
                this.children_forms_ready()
                if(!this.children_forms.person.ready2) {
                    this.children_forms.person.obj.submitaction()                    
                }
                if(!this.children_forms.address.ready2) {
                    this.children_forms.address.obj.submitaction()
                }                
            },
            submitaction: function() {
                AbonApi.abonent_set({
                    uid: (this.oid || 0),
                    person_id: this.children_forms.person.oid,
                    address_id: this.children_forms.address.oid                   
                },this.submitcallback.createDelegate(this));
            },
            submitcallback: function(result,e) {                
                if(result.success) {
                    this.oid = result.data[0]['id']
                    this.setTitle("абон: "+(result.data[0]['code'] || '<новый>'))
                    Ext.ux.abonent_store.load()                    
                    //this.destroy();
                }
            },
            children_forms_ready: function() {
                if((this.children_forms.person.ready2)&&(this.children_forms.address.ready2)) {
                    this.submitaction()
                }
            },
            children_forms:{
                person : {
                    ready2: false,
                    oid: null,
                    obj: null
                },
                address: {
                    ready2: false,
                    oid: null,
                    obj: null
                }                
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        this.setTitle("абон: "+(this.code || '<новый>'))
                    },
                    scope: this
                }
            }
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonentForm.superclass.initComponent.apply(this, arguments);
    }    
});