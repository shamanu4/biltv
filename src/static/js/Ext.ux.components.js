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
        } else if (type=="ext-mb-invisible") {
            var delay = 0
        } else {
            var delay = 3
        }
        if(!msgCt){
            msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true)
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
                    'id': 'menu-scrambler-card-button',
                    'handler': Engine.menu.scrambler.card.openGrid,
                    'text': 'Карточки'                    
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
            this.searchfield = new Ext.form.TextField({
                listeners: {
                    specialkey: {
                        fn: function(field, e){                            
                            if (e.getKey() == e.ENTER) {                                
                                this.searchAction()
                            }
                        },
                        scope: this
                    }
                }
            }),
            new Ext.Toolbar.Spacer(),
            {
                icon: '/static/extjs/custom/search_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchAction()
                },
                scope: this
            },{
                icon: '/static/extjs/custom/delete_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {                    
                    this.searchfield.setValue('')
                    this.store.baseParams.filter_value = ''
                    this.store.load()
                },
                scope: this
            },
            ],
            bbar: new Ext.PagingToolbar({
                pageSize: this.pageSize || 16,
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
            },
            searchAction: function() {
                this.store.baseParams.filter_value = this.searchfield.getValue()
                this.store.load()
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
    initComponent: function(options) {
        options = options || {}
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
             this.searchfield = new Ext.form.TextField({
                listeners: {
                    specialkey: {
                        fn: function(field, e){
                            if (e.getKey() == e.ENTER) {
                                this.searchAction()
                            }
                        },
                        scope: this
                    }                
                }
            }),
            new Ext.Toolbar.Spacer(),
            {
                icon: '/static/extjs/custom/search_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchAction()
                },
                scope: this
            },{
                icon: '/static/extjs/custom/delete_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchfield.setValue('')
                    this.store.baseParams.filter_value = ''
                    this.store.load()
                },
                scope: this
            },
            ],
            bbar: new Ext.PagingToolbar({
                pageSize:  this.pageSize || 16,
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
            searchAction: function() {
                this.store.baseParams.filter_value = this.searchfield.getValue()
                this.store.load()
            }
          /*  sm: new Ext.grid.RowSelectionModel({
                singleSelect: true,
                listeners: {
                    rowselect: {
                        fn: function(sm,index,record) {
                            //if(this.current_row != index) {
                            //    this.unsaved_row = this.current_row
                            //    this.current_row = index
                            //    this.store.save()
                            //    this.store.commitChanges();
                            //}
                        },
                        scope: this
                    }
                }
            })
          */
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.apply(this, options);
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

Ext.reg('ext:ux:city-grid', Ext.ux.CityGrid);

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
            closable: true,
            columns: [
                {header: "Id", dataIndex: 'id', width:100, sortable:true},
                {header: "Code", dataIndex: 'code', width:100, sortable:true},
                {header: "Person", dataIndex: 'person', width:300, sortable:true},
                {header: "Passport", dataIndex: 'person__passport', width:100, sortable:true},
                {header: "Address", dataIndex: 'address', width:300, sortable:true},
                //{header: "Comment", dataIndex: 'comment'},
                {header: "OK", dataIndex: 'confirmed', width: 36, sortable:true,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        return '<div class="abonent_ok_status_'+value+'"></div>'
                    }
                },
                {header: " ", dataIndex: 'id', width: 28,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        return '<div class="inline_edit_button abonent_edit_button" id="'+value+'" code="'+record.data.code+'" confirmed="'+record.data.confirmed+'"></div>'
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
                            Engine.menu.cashier.abonent.openForm(this.id,$(this).attr('code'),$(this).attr('confirmed'));
                        })
                    }
                }
            }
});

Ext.ux.CardGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'card-store',
            title: 'Карточки',
            ds_model: card_ds_model,
            columns: [
                {header: "Id", dataIndex: 'id', width:100},
                {header: "Num", dataIndex: 'num', width:100, editor: new Ext.form.TextField()},
                {header: "Owner", dataIndex: 'owner', width:300},
                {header: "Active", dataIndex: 'active', width:100, xtype: 'booleancolumn'},
                {header: "Activated", dataIndex: 'activated', width:150},
            ]         
});

/*
 *  Forms and panels
 */

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
                fieldLabel: 'Особовий рахунок',
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

Ext.ux.BalanceForm = Ext.extend(Ext.FormPanel, {
    initComponent: function(){
        var config = {
            border : true,
            width: 300,
            height: 180,
            buttons:[{
                text: 'Внести оплату',
                handler: function(){
                    alert("not implemented yet")
                },
                scope: this
            },{
                text: 'зняти',
                handler: function(){
                    alert("not implemented yet")
                },
                scope: this
            }],
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        AbonApi.balance_get({
                            uid: (this.oid || 0)
                        },function (result,e) {
                            if (result.data.balance==null) {
                                this.body.dom.innerHTML='<div class="balance_digits_negative">...</div>'
                            }
                            else if (result.data.balance<0) {
                                this.body.dom.innerHTML='<div class="balance_digits_negative">'+result.data.balance+' грн.</div>'
                            } else {
                                this.body.dom.innerHTML='<div class="balance_digits_positive">'+result.data.balance+' грн.</div>'
                            }
                        }.createDelegate(this));
                    },
                    scope: this
                }
            }
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AddressForm.superclass.initComponent.apply(this, arguments);
    }
})

Ext.reg('ext:ux:balance-form', Ext.ux.BalanceForm);

Ext.ux.FreeCardCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.free_card_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'num',
            mode: 'local'
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.FreeCardCombo.superclass.initComponent.apply(this, arguments);
    }
}),

Ext.reg('ext:ux:free-cards-combo', Ext.ux.FreeCardCombo);

Ext.ux.AbonCardsGrid = Ext.extend(Ext.ux.CustomGrid ,{
    initComponent: function(){        
        var config = {
            store: new Ext.data.DirectStore({
                restful: true,
                autoLoad: true,
                autoSave: false,
                reader: new Ext.data.JsonReader({
                    root: 'data',
                    totalProperty: 'total',
                    fields: [
                        'id',
                        'num',
                        'active',
                        'activated',
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.cards_get,
                    create: AbonApi.cards_set,
                    update: AbonApi.foo,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:10,
                    uid:this.oid,
                    filter_fields:['num'],
                    filter_value:''
                }
            }),
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        obj.parent_form.children_forms.cards.obj=obj
                    },
                    scope: this
                }
            },
            sm: new Ext.grid.RowSelectionModel({
                singleSelect: true,
                listeners: {
                    rowselect: {
                        fn: function(sm,index,record) {                            
                            var store = Ext.ux.free_card_combo_store
                            if (typeof(record.id)=='number') {
                                store.setBaseParam('card_id',record.id)
                                store.load()
                            } else {
                                //this.store.load()
                            }
                        },
                        scope: this
                    }
                }
            })
        }        
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCardsGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Карточки',
    ds_model: card_ds_model,
    columns: [
        {header: "Id", dataIndex: 'id', width:40},
        {header: "Num", dataIndex: 'num', width:80,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                if (value===undefined) {
                    this.editable=true
                }
                if (value<0) {
                    return '<b>CaTV</b>';
                } else {
                    return value;
                }
            },
            editor: new Ext.ux.FreeCardCombo(),
            editable: false
        },
        {header: "Active", dataIndex: 'active', width:40,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                if (value==true) {
                    return '<img src="/static/extjs/custom/tick_16.png">';
                } else {
                    return '<img src="/static/extjs/custom/block_16.png">';
                }
            }
        },
        {header: "Activated", dataIndex: 'activated', width:120},
        {header: "", dataIndex: 'id', width:26,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                return '<img src="/static/extjs/custom/delete_16.png">';
            }
        }
    ]    
});

Ext.reg('ext:ux:abon-cards-grid', Ext.ux.AbonCardsGrid);

Ext.ux.AbonCardsTpGrid = Ext.extend(Ext.ux.CustomGrid ,{
    initComponent: function(){
        var config = {
            store: new Ext.data.DirectStore({
                restful: true,
                autoLoad: true,
                autoSave: false,
                reader: new Ext.data.JsonReader({
                    root: 'data',
                    totalProperty: 'total',
                    fields: [
                        'id',
                        'tariff',
                        'active',
                        'activated',
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.cards_tp_get,
                    create: AbonApi.cards_tp_set,
                    update: AbonApi.foo,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:10,
                    uid:this.oid,
                    card_id:0,
                    filter_fields:['num'],
                    filter_value:''
                }
            }),
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        obj.parent_form.children_forms.tariffs.obj=obj
                    },
                    scope: this
                }
            },
            sm: new Ext.grid.RowSelectionModel({
                singleSelect: true,
                listeners: {
                    rowselect: {
                        fn: function(sm,index,record) {
                            //sm.grid.parent_form.children_forms.tariffs.obj.setTitle('13')
                        },
                    scope: this
                    }
                }
            })
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCardsGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Карточки',
    ds_model: card_ds_model,
    columns: [
        {header: "Id", dataIndex: 'id', width:40},
        {header: "Tariff", dataIndex: 'tariff', width:120},
        {header: "Active", dataIndex: 'active', width:40,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                if (value==true) {
                    return '<img src="/static/extjs/custom/tick_16.png">';
                } else {
                    return '<img src="/static/extjs/custom/block_16.png">';
                }
            }
        },
        {header: "Activated", dataIndex: 'activated', width:120},
    ]
});

Ext.reg('ext:ux:abon-cards-tp-grid', Ext.ux.AbonCardsTpGrid);

Ext.ux.AbonPaymentsGrid = Ext.extend(Ext.ux.CustomGridNE ,{
    initComponent: function(){
        var config = {
            store: new Ext.data.DirectStore({
                restful: true,
                autoLoad: true,
                autoSave: false,
                remoteSort: true,
                reader: new Ext.data.JsonReader({
                    root: 'data',
                    totalProperty: 'total',
                    fields: [
                        'id',
                        'bill',
                        'timestamp',
                        'sum',
                        'prev',
                        'maked',
                        'descr',
                        'inner_descr'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.payments_get,
                    create: AbonApi.foo,
                    update: AbonApi.foo,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:12,
                    foo:'bar',
                    uid:this.oid,
                    filter_fields:['num'],
                    filter_value:''
                }
            }),            
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        //obj.parent_form.children_forms.cards.obj=obj
                    },
                    scope: this
                }
            }
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCardsGrid.superclass.initComponent.apply(this, [config]);
    },    
    columns: [
        {header: "Id", dataIndex: 'id', width:40},
        {header: "Bill", dataIndex: 'bill', width:40},
        {header: "Timestamp", dataIndex: 'timestamp', width:90, sortable: true},
        {header: "Sum", dataIndex: 'sum', width:50, sortable: true},
        {header: "Prev", dataIndex: 'prev', width:50},
        {header: "Maked", dataIndex: 'maked', width:40},
        {header: "Descr", dataIndex: 'inner_descr', width:100},
        {header: "", dataIndex: 'id', width:26,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                return '<img src="/static/extjs/custom/delete_16.png">';
            }
        }
    ],
    pageSize: 12,
    height: 450
});

Ext.reg('ext:ux:abon-payments-grid', Ext.ux.AbonPaymentsGrid);

Ext.ux.AbonInfoPanel = Ext.extend(Ext.Panel ,{
    initComponent: function() {
        var config = {
            closable: true,
            title: 'Информация',
            border : true,
            defaults: {
                frame: true,
                split: true    
            },
            tbar: new Ext.ux.TabPanel({
                width: 1000,
                height: 480,
                items: [{
                    title: 'Тарифы',
                    xtype: 'panel',
                    layout: 'column',
                    items: [
                        {
                            title: 'Карточки',
                            xtype: 'ext:ux:abon-cards-grid',
                            columnWidth: .5,
                            height: 280,
                            oid: this.oid,
                            parent_form: function(scope){return scope;}(this)
                        },{                            
                            title: 'Тарифы',
                            xtype: 'ext:ux:abon-cards-tp-grid',
                            columnWidth: .5,
                            height: 280,
                            oid: this.oid,
                            parent_form: function(scope){return scope;}(this)
                        }]
                    },{
                        title: 'Оплаты',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype:'ext:ux:abon-payments-grid',
                            oid: this.oid
                        }]
                    },{
                        title: 'Снятия денег',
                        xtype: 'panel',
                        oid: this.oid,
                        parent_form: this
                    }]
            }),
            children_forms:{
                cards : {
                    obj: null
                },
                tariffs: {
                    obj: null
                }
            }
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonentForm.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:abon-info-panel', Ext.ux.AbonInfoPanel);

Ext.ux.AbonentForm = Ext.extend(Ext.Panel ,{
    initComponent: function() {
        var config = {
            closable: true,
            title: 'абонент '+(this.oid || 'новый'),
            layout: 'table',
            layoutConfig: {
                columns: 3
            },
            border : true,
            defaults: {
                frame: true,
                split: true,
                bodyStyle: 'padding:15px'
            },
            items: [{
                title: 'Абонент',
                xtype: 'ext:ux:person-form',
                oid: this.oid,
                parent_form: this
            },{
                title: 'Адреса',
                xtype: 'ext:ux:address-form',
                oid: this.oid,
                parent_form: this
            },{
                title: 'Баланс',
                xtype: 'ext:ux:balance-form',
                oid: this.oid,
                parent_form: this
            },{
                xtype: 'toolbar',
                colspan: 3,
                items: [{
                        xtype: 'tbbutton',
                        cls: 'x-btn-text-icon',
                        icon: '/static/extjs/custom/tick_16.png',
                        text: 'Сохранить',
                        colspan: 3,
                        width: 100,
                        handler: function(){
                            (function(){this.submitprep();}).defer(500,this);
                        },
                        scope: this                        
                    },{
                        xtype: 'tbseparator'
                    },{
                        boxLabel: 'Проверено',
                        colspan: 3,
                        xtype: 'checkbox',
                        width: 100,
                        handler: function(obj){
                            //debugger;
                        },
                        listeners: {
                            afterrender : {
                                fn: function(obj) {
                                    this.children_forms.abonent.obj=obj
                                    if(this.confirmed=="true") {
                                        obj.setValue(true)
                                    }
                                },
                                scope: this
                            }
                        },
                        scope: this
                    }]
            },{
                colspan: 3,
                xtype: 'ext:ux:abon-info-panel',
                oid: this.oid,
                parent_form: this
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
                    address_id: this.children_forms.address.oid,
                    confirmed: this.children_forms.abonent.obj.checked
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
                },
                abonent: {
                    obj: null
                }
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        this.setTitle("абон: "+(this.code || '<новый>'))
                    },
                    scope: this
                },
                beforeclose: {
                    fn: function(obj) {
                        obj.hide()
                    }
                }
            }
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonentForm.superclass.initComponent.apply(this, arguments);
    }    
});