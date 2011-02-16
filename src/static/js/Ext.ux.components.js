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
            delay = 10;
        } else {
            delay = 3
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
    frame:true,
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

Ext.ux.CustomGrid = Ext.extend(Ext.grid.EditorGridPanel,{
    store: null,
    ds_model: null,
    columns: [],
    height: 300,
    instance: null,
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
                pageSize: 10,
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
                         index = Ext.ux.cities_combo_store.find('id',value)
                         if (index>=0) {
                            return Ext.ux.cities_combo_store.getAt(index).data.name
                         } else {
                            return 'undefined'
                         }
                    },                    
                    scope: this
                },
                {header: "Name", dataIndex: 'name', editor: new Ext.form.TextField()},
                {header: "Label", dataIndex: 'label', editor: new Ext.form.TextField()},
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
                         index = Ext.ux.streets_combo_store.find('id',value)
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
                         index = Ext.ux.houses_combo_store.find('id',value)
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

Ext.ux.AbonentGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'abonents-store',
            ds_model: null,
            title: 'Список абонентов',
            columns: [
            ]
});