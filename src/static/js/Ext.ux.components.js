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
            var delay = 1
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
                    'id': 'menu-cashier-register-button',
                    'handler': Engine.menu.cashier.register.openGrid,
                    'text': 'Реестры'
                },{
                    'id': 'menu-cashier-payment-button',
                    'handler': Engine.menu.cashier.payment.openForm,
                    'text': 'Оплаты',
					'oid': 0
                },{
                    'id': 'menu-cashier-registers-form-button',
                    'handler': Engine.menu.cashier.register.openForm,
                    'text': 'Отчёт по оплатам',
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
	closable: true,
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
                {header: "Person", dataIndex: 'person', width:260, sortable:true},
                {header: "Passport", dataIndex: 'person__passport', width:100, sortable:true},
                {header: "Address", dataIndex: 'address', width:280, sortable:true},
                //{header: "Comment", dataIndex: 'comment'},
                {header: "OK", dataIndex: 'confirmed', width: 36, sortable:true,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        return '<div class="abonent_ok_status_'+value+'"></div>'
                    }
                },
				{header: "Откл.", dataIndex: 'disabled', width: 56, sortable:true,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        return '<div class="abonent_disabled_status_'+value+'"></div>'
                    }
                },
                {header: " ", dataIndex: 'id', width: 28,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        return '<div class="inline_edit_button abonent_edit_button" id="'+value+'" code="'+record.data.code+'" confirmed="'+record.data.confirmed+'" dis="'+record.data.disabled+'"></div>'
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
                            Engine.menu.cashier.abonent.openForm(this.id,$(this).attr('code'),$(this).attr('confirmed'),$(this).attr('dis'));
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

Ext.ux.SourceCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.sources_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'name',
            mode: 'local'
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.SourceCombo.superclass.initComponent.apply(this, arguments);
    }
});

Ext.ux.RegisterGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'register-store',
            title: 'Реестры',
            ds_model: register_ds_model,
            columns: [
                {header: "Id", dataIndex: 'id', width:100, editable:false},
                {header: "Source", dataIndex: 'source', width:100, editable:false, editor: new Ext.ux.SourceCombo(),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (value === undefined) {
							this.editable = true
						}
						return value;
					}
                },
                {header: "Total", dataIndex: 'total', width:100, editable:false, editor: new Ext.form.TextField(),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (value === undefined) {
							this.editable = true
						}
						return value;
					} 
				},
                {header: "Start", dataIndex: 'start', width:180, editable:false, editor: new Ext.form.DateField({format:'Y-m-d'}),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (value === undefined) {
							this.editable = true
						}
						return value;
					},
                	listeners: {
                    	change : {
                        	fn: function(obj) {
                            	tfoo=1
								debugger;
                        	},
                        	scope: this
                    	}
                	}
				},
				{header: "End", dataIndex: 'end', width:180, editable:false, editor: new Ext.form.DateField({format:'Y-m-d'}),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (value === undefined) {
							this.editable = true
						}
						return value;
					}
				},
				{header: "Closed", dataIndex: 'closed', width:100, editable:false},
				{header: " ", dataIndex: 'id', width: 28,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        return '<div class="inline_edit_button register_edit_button" id="'+value+'" code="'+record.data.code+'" confirmed="'+record.data.confirmed+'" dis="'+record.data.disabled+'"></div>'
                    }
                },
            ],
            addAction: function(){
                Engine.menu.cashier.abonent.openForm()
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        $(".register_edit_button").live('click', function(e) {
                            Engine.menu.cashier.register.openForm(this.id);
                        })
                    }
                }
            }
});



Ext.ux.RegisterForm = Ext.extend(Ext.Panel, {
    initComponent: function(){
		var config = {
			title: 'Реестр',
			closable: true,
			layout: 'anchor',
			register: null,	
			admin: null,	
			items: [
				this.filterform = new Ext.FormPanel({
					frame: true,
					items: [
						{
							xtype: 'buttongroup',
							title: 'Оператор',
							items: [
							this.admincombo = new Ext.form.ComboBox({
								store: new Ext.data.DirectStore({
    								api: {
        								read: AbonApi.admins_get,
        								create: AbonApi.foo,
        								update: AbonApi.foo,
        								destroy: AbonApi.foo
    								},
    								remoteSort: true,
    								restful: true,
    								autoLoad: false,
    								autoSave: false,
    								reader: new Ext.data.JsonReader({
        								root: 'data',
        								totalProperty: 'total',
        								//idProperty: 'id',
        								fields: [
            								'id',
											'username',          						
										]
    								}),
    								baseParams : {
        								start:0,
        								limit:100,        							
    								},
    							}),
								valueField: 'username',
            					displayField: 'username',
								triggerAction: 'all',
								editable: false,							
								forceSelection: true,
								fieldLabel: 'Оператор',
								listeners: {
									select: {
										fn: function(combo,record,index) {
											this.admin = record.data.id
											//this.preload()
										},
										scope: this
									}
								}
							}),
							this.resetbutton = new Ext.Button({
								text: 'сбросить',
								listeners: {
									click: {
										fn: function(button, event) {
											this.admincombo.reset()
											this.admin = null
											//this.preload()
										},
										scope: this
									}
								}
							})
						]},
						this.registercombo = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonApi.registers_get,
        							create: AbonApi.foo,
        							update: AbonApi.foo,
        							destroy: AbonApi.foo
    							},
    							remoteSort: true,
    							restful: true,
    							autoLoad: false,
    							autoSave: false,
    							reader: new Ext.data.JsonReader({
        							root: 'data',
        							totalProperty: 'total',
        							//idProperty: 'id',
        							fields: [
            							'id',
										'unicode',
            							'source',
										'total',
										'current',
										'start',
										'end',            						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:100,        							
    							},
    						}),
							width: 380,
							valueField: 'unicode',
            				displayField: 'unicode',
							triggerAction: 'all',
							editable: false,							
							forceSelection: true,
							fieldLabel: 'Реестр',
							listeners: {
								select: {
									fn: function(combo,record,index) {
										this.register = record.data.id
										this.setTitle('Реестр #'+record.data.id)
										//this.preload()
									},
									scope: this
								}
							}
						}),
						this.countfield = new Ext.form.TextField({
							fieldLabel: 'Количество',
							readOnly: true,
						}),
						this.sumfield = new Ext.form.TextField({
							fieldLabel: 'Сумма',
							readOnly: true,
						}),
						this.refreshbutton = new Ext.Button({
							text: 'обновить',
							listeners: {
								click: {
									fn: function(button, event) {
										this.preload()
									},
									scope: this
								}
							}
						}),
					]					
				}),
				this.resultsgrid = new Ext.grid.GridPanel({
					height: 400,
					width: 1100,
					store: new Ext.data.DirectStore({
                		restful: true,
                		autoLoad: false,
                		reader: new Ext.data.JsonReader({
                    		root: 'data',
                    		totalProperty: 'total',
                    		fields: [
                     			'id',
                        		'bill',
                        		'timestamp',
                        		'sum',
                        		'prev',
								'onwer_code',
								'onwer_name',
								'admin',
                        		'maked',
								'source__name',
								'bank_date',
                        		'descr',
                        		'inner_descr',								
                    		]
                		}),
                		api: {
                    		read: AbonApi.reg_payments_get,
                    		create: AbonApi.foo,
                    		update: AbonApi.foo,
                    		destroy: AbonApi.foo
                		},
                		baseParams : {
                    		register_id:this.register,
                    		admin_id:this.admin,
                    		start_date:this.start_date,
							end_date:this.start_date,
                		}
					}),
					columns: [
        				{header: "Id", dataIndex: 'id', width:45},
        				{header: "Timestamp", dataIndex: 'timestamp', width:125, sortable: true},
        				{header: "Абонент", dataIndex: 'onwer_code', width:125},
						{header: "ФИО", dataIndex: 'onwer_name', width:180},        				
						{header: "Сума", dataIndex: 'sum', width:50, sortable: true},
						{header: "Оператор", dataIndex: 'admin', width:100, sortable: true},
        				{header: "Банк", dataIndex: 'source__name', width:120, sortable: true},
						{header: "Дата квитанции", dataIndex: 'bank_date', width:120, sortable: true},
        				{header: "Описание", dataIndex: 'inner_descr', width:200},        				
    				],
				})
			],
			listeners: {
            	afterrender: {
                	fn: function(obj) {
						this.loading.hide()
                    	this.registercombo.store.load({							
							callback: function(response) {
								index = this.registercombo.store.indexOfId(parseInt(this.oid))								
								if (index>=0) {
									this.setTitle('Реестр #'+response[index].data.id)
									this.registercombo.setValue(response[index].data.unicode)
									this.register = this.oid									
									this.preload()
								}								
							},
							scope: this
						})		
                    },
                    scope: this
                }
            },
			preload: function() {				
				if(!this.register) {
					Ext.ux.msg('Выберите реестр','',Ext.Msg.ERROR)
					return falsey
				}
				Ext.get('loading').show();
            	Ext.get('loading-mask-half').show();
				this.resultsgrid.store.setBaseParam('register_id',this.register)
				this.resultsgrid.store.setBaseParam('admin_id',this.admin)
				this.resultsgrid.store.load({
					callback: function(response) {
						Ext.get('loading').hide();
            			Ext.get('loading-mask-half').fadeOut('fast');
						extras = this.resultsgrid.store.reader.jsonData.extras
						this.countfield.setValue(extras.count)
						this.sumfield.setValue(extras.sum)						
					},
					scope: this
				})
			}			
		}		
		Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.RegisterForm.superclass.initComponent.apply(this, arguments);
	} 
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
        return /^\d{1,5}$/.test(v);
    },
    decimalText: 'Должно быть числом 0-99999',
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
                fieldLabel: 'Номер счёта',
                name: 'ext',
                allowBlank:false
            },
			this.activated_field = new Ext.form.DateField({
                fieldLabel: 'Подключен',
                name: 'activated',
				xtype: 'datefield',
				format: 'Y-m-d',
                allowBlank: false
            })],
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
					Engine.menu.cashier.payment.openForm(this.oid)
                },
                scope: this
            },{
                text: 'зняти',
                handler: function(){
                    Engine.menu.cashier.fee.openForm(this.oid)
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
                autoLoad: false,
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
							var tpstore = sm.grid.parent_form.children_forms.tariffs.obj.store
                            if (typeof(record.id)=='number') {								
                                tpstore.setBaseParam('card_id',record.id)
								tpstore.load()
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
                autoLoad: false,
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
                autoLoad: false,
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
						'source__name',
						'bank_date',
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
                    uid:this.oid || 0,
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
            },
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCardsGrid.superclass.initComponent.apply(this, [config]);
    },    
    columns: [
        {header: "Id", dataIndex: 'id', width:40},
        {header: "Bill", dataIndex: 'bill', width:40},
        {header: "Timestamp", dataIndex: 'timestamp', width:120, sortable: true},
        {header: "Sum", dataIndex: 'sum', width:50, sortable: true},
        {header: "Prev", dataIndex: 'prev', width:50},
		{header: "Source", dataIndex: 'source__name', width:120, sortable: true},
		{header: "Bank date", dataIndex: 'bank_date', width:120, sortable: true},
        {header: "Descr", dataIndex: 'inner_descr', width:200},
        {header: "", dataIndex: 'id', width:26,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                return '<img src="/static/extjs/custom/delete_16.png">';
            }
        }
    ],
	viewConfig: {
        forceFit: true,
		getRowClass: function(record, index, rowParams, store) {
            var c = record.get('maked');
            if (c) {
				return 'maked_true_class';
			} else {
				return 'maked_false_class';				
			}
        }
    },
    pageSize: 12,
    height: 450
});


Ext.reg('ext:ux:abon-payments-grid', Ext.ux.AbonPaymentsGrid);

Ext.reg('ext:ux:abon-cards-tp-grid', Ext.ux.AbonCardsTpGrid);

Ext.ux.AbonFeesGrid = Ext.extend(Ext.ux.CustomGridNE ,{
    initComponent: function(){
        var config = {
            store: new Ext.data.DirectStore({
                restful: true,
                autoLoad: false,
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
                    read: AbonApi.fees_get,
                    create: AbonApi.foo,
                    update: AbonApi.foo,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:12,
                    foo:'bar',
                    uid:this.oid || 0,
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
        {header: "Timestamp", dataIndex: 'timestamp', width:180, sortable: true},
        {header: "Sum", dataIndex: 'sum', width:50, sortable: true},
        {header: "Prev", dataIndex: 'prev', width:50},
        {header: "Descr", dataIndex: 'inner_descr', width:200},
        {header: "", dataIndex: 'id', width:26,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                return '<img src="/static/extjs/custom/delete_16.png">';
            }
        }
    ],
	viewConfig: {
        forceFit: true,
		getRowClass: function(record, index, rowParams, store) {
            var c = record.get('maked');
            if (c) {
				return 'maked_true_class';
			} else {
				return 'maked_false_class';				
			}
        }
    },
    pageSize: 12,
    height: 450
});

Ext.reg('ext:ux:abon-fees-grid', Ext.ux.AbonFeesGrid);

Ext.ux.AbonCommentsPanel = Ext.extend(Ext.Panel ,{
	    initComponent: function() {
        var config = {
            closable: false,
			frame: true,
            defaults: {
                frame: true,
                split: true    
            },            
            items: [{
					xtype: 'textarea',
					width: 900,
			},{
                        xtype: 'tbbutton',
                        cls: 'x-btn-text-icon',
                        icon: '/static/extjs/custom/tick_16.png',
                        text: 'Сохранить',
			}]            
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCommentsPanel.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:abon-comments-panel', Ext.ux.AbonCommentsPanel );

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
                        title: 'Снятия',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype:'ext:ux:abon-fees-grid',
                            oid: this.oid
                        }]
                    },{
                        title: 'Дополнительно',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype:'ext:ux:abon-comments-panel',
                            oid: this.oid
                        }]
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
                                    this.children_forms.confirmed.obj=obj
                                    if(this.confirmed=="true") {
                                        obj.setValue(true)
                                    }
                                },
                                scope: this
                            }
                        },
                        scope: this
                    },{
                        xtype: 'tbseparator'
                    },{
                        boxLabel: 'Отключен',
                        colspan: 3,
                        xtype: 'checkbox',
                        width: 100,
                        handler: function(obj){
                            //debugger;
                        },
                        listeners: {
                            afterrender : {
                                fn: function(obj) {
                                    this.children_forms.disabled.obj=obj
                                    if(this.dis=="true") {
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
                    confirmed: this.children_forms.confirmed.obj.checked,
					disabled: this.children_forms.disabled.obj.checked,
					activated: this.children_forms.address.obj.activated_field.value                
                },this.submitcallback.createDelegate(this));
            },
            submitcallback: function(result,e) {                
                if(result.success) {                    
                    Ext.ux.abonent_store.load()
					this.setTitle("абон: "+(result.data[0]['code'] || '<новый>'))
					if (!this.oid) {
						this.destroy();
						Engine.menu.cashier.abonent.openForm(result.data[0]['id'], result.data[0]['code'], result.data[0]['confirmed'], result.data[0]['disabled']);
					}					
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
                confirmed: {
                    obj: null
                },
				disabled: {
                    obj: null
                }
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        AbonApi.abonent_get({
                            uid: (this.oid || 0)
                        },this.submitcallback.createDelegate(this));
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

Ext.ux.PaymentForm = Ext.extend(Ext.Panel ,{
	initComponent: function() {
        var config = {
            closable: true,
            title: 'Оплаты',
            layout: 'table',
            layoutConfig: {
                columns: 1
            },
            border : true,
            defaults: {
                frame: true,
                split: true,
                bodyStyle: 'padding:15px'
            },
            items: [
				{
					xtype: 'panel',
					width:  500,
					layout: 'column',
					columnWidth: 1,
					items: [
						this.registercombo = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonApi.registers_get,
        							create: AbonApi.foo,
        							update: AbonApi.foo,
        							destroy: AbonApi.foo
    							},
    							remoteSort: true,
    							restful: true,
    							autoLoad: false,
    							autoSave: false,
    							reader: new Ext.data.JsonReader({
        							root: 'data',
        							totalProperty: 'total',
        							//idProperty: 'id',
        							fields: [
            							'id',
										'unicode',
            							'source',
										'total',
										'current',
										'start',
										'end',            						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:100,        							
    							},
    						}),
							width: 400,
							valueField: 'unicode',
            				displayField: 'unicode',
							triggerAction: 'all',
							editable: false,							
							forceSelection: true,
							emptyText: 'Реестр',
							listeners: {
								select: {
									fn: function(combo,record,index) {
										this.register = record.data.id
									},
									scope: this
								}
							}
						}),												
					]					
				},
				{
					xtype: 'panel',
					width:  500,
					layout: 'column',
					columnWidth: 1,
					items: [
						this.searchfield = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonentGrid.read,
        							create: AbonApi.foo,
        							update: AbonApi.foo,
        							destroy: AbonApi.foo
    							},
    							restful: true,
    							autoLoad: false,
    							autoSave: false,
    							reader: new Ext.data.JsonReader({
        							root: 'data',
        							totalProperty: 'total',
        							//idProperty: 'id',
        							fields: [
            							'id',
            							'code',						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,
        							filter_fields:['code'],
        							filter_value:''
    							},
    						}),
							valueField: 'code',
            				displayField: 'code',
							triggerAction: 'all',							
							minChars: 1,
							hideTrigger: true,
							forceSelection: true,
							emptyText: 'Личный счёт',
							listeners: {
								change: {
									fn: function(combo,newval,oldval) {
										AbonApi.abonent_get({
                            				code: (this.searchfield.getValue() || 0)
                        				},this.preload.createDelegate(this));
									},
									scope: this
								}
							}
						}),						
						{
                			icon: '/static/extjs/custom/search_16.png',
                			cls: 'x-btn-text-icon',
							xtype: 'button',
                			handler: function() {
                    			AbonApi.abonent_get({
                            		code: (this.searchfield.getValue() || 0)
                        		},this.preload.createDelegate(this));
                			},
                			scope: this
            			},
						this.personfield = new Ext.form.Label({
							text: '...',
							width: 200
						}),
						this.addressfield = new Ext.form.Label({
							text: '...',
							width: 200
						}),								
						
					]
				},{
					xtype: 'form',
					width:  500,
					items: [
						this.bankdate = new Ext.form.DateField({
							fieldLabel: 'Дата квитанции',
							format: 'Y-m-d'
						}),
						this.sum = new Ext.form.NumberField({
							fieldLabel: 'Сумма',
							baseChars: '1234567890.'
						}),
						this.descr = new Ext.form.TextField({
							fieldLabel: 'Описание',							
						}),					
					],
					bbar:[{					
                        xtype: 'tbbutton',
                        cls: 'x-btn-text-icon',
                        icon: '/static/extjs/custom/tick_16.png',
                        text: 'Сохранить',
                        colspan: 3,
                        width: 100,
                        handler: function(){
                            if(this.register<1) {
								Ext.ux.msg('Ошибка ввода',"выберите реестр оплат",Ext.Msg.ERROR)
								return false
							}
							if(this.abonent<1) {
								Ext.ux.msg('Ошибка ввода',"выберите абонента",Ext.Msg.ERROR)
								return false
							}
							if (!this.bankdate.getValue()) {
								Ext.ux.msg('Ошибка ввода',"введите правильную дату",Ext.Msg.ERROR)
								return false
							}
							if (parseFloat(this.sum.getValue() || 0) <= 0) {
								Ext.ux.msg('Ошибка ввода',"введите правильную сумму",Ext.Msg.ERROR)
								return false
							}
							AbonApi.make_payment({
								register: this.register,
								abonent: this.abonent,
								bankdate: this.bankdate.getValue(),
								sum: parseFloat(this.sum.getValue()),	
								descr: this.descr.getValue()
							},this.payment_callback.createDelegate(this));
                        },
                        scope: this                        
                    }]
				}			
			],
            listeners: {
                activate: {
                    fn: function(obj) {
						if (parseInt(this.oid)>0) {
							AbonApi.abonent_get({
                            	uid: (parseInt(this.oid) || 0)
                        	},this.preload.createDelegate(this));
						}
                    },
                    scope: this
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
			preload: function(response) {
				if(response.success) {						
					this.searchfield.setValue(response.data[0]['code'])					
					this.personfield.setText(response.data[0]['person'])
					this.addressfield.setText(response.data[0]['address'])
					this.abonent = response.data[0]['id']
				}
			},
			payment_callback: function(response) {
				this.searchfield.setRawValue('')
				this.personfield.setRawValue('')
				this.addressfield.setRawValue('')
				this.abonent = 0				
			},
			register: 0,
			abonent: 0
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.PaymentForm.superclass.initComponent.apply(this, arguments);
    }    
})

Ext.ux.FeeForm = Ext.extend(Ext.Panel ,{
	initComponent: function() {
        var config = {
            closable: true,
            title: 'Снятия',
            layout: 'table',
            layoutConfig: {
                columns: 1
            },
            border : true,
            defaults: {
                frame: true,
                split: true,
                bodyStyle: 'padding:15px'
            },
            items: [
				{
					xtype: 'panel',
					width:  500,
					layout: 'column',
					columnWidth: 1,
					items: [
						this.feetypecombo = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonApi.feetypes_get,
        							create: AbonApi.foo,
        							update: AbonApi.foo,
        							destroy: AbonApi.foo
    							},
    							remoteSort: true,
    							restful: true,
    							autoLoad: false,
    							autoSave: false,
    							reader: new Ext.data.JsonReader({
        							root: 'data',
        							totalProperty: 'total',
        							//idProperty: 'id',
        							fields: [
            							'id',
										'unicode',
										'sum'					
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:100,        							
    							},
    						}),
							width: 400,
							valueField: 'unicode',
            				displayField: 'unicode',
							triggerAction: 'all',
							editable: false,							
							forceSelection: true,
							emptyText: 'Тип услуги',
							listeners: {
								select: {
									fn: function(combo,record,index) {
										this.sum.setValue(record.data.sum)
										this.feetype = record.data.id
									},
									scope: this
								}
							}
						}),												
					]					
				},
				{
					xtype: 'panel',
					width:  500,
					layout: 'column',
					columnWidth: 1,
					items: [
						this.searchfield = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonentGrid.read,
        							create: AbonApi.foo,
        							update: AbonApi.foo,
        							destroy: AbonApi.foo
    							},
    							restful: true,
    							autoLoad: false,
    							autoSave: false,
    							reader: new Ext.data.JsonReader({
        							root: 'data',
        							totalProperty: 'total',
        							//idProperty: 'id',
        							fields: [
            							'id',
            							'code',						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,
        							filter_fields:['code'],
        							filter_value:''
    							},
    						}),
							valueField: 'code',
            				displayField: 'code',
							triggerAction: 'all',							
							minChars: 1,
							hideTrigger: true,
							forceSelection: true,
							emptyText: 'Личный счёт',
							listeners: {
								change: {
									fn: function(combo,newval,oldval) {
										AbonApi.abonent_get({
                            				code: (this.searchfield.getValue() || 0)
                        				},this.preload.createDelegate(this));
									},
									scope: this
								}
							}
						}),						
						{
                			icon: '/static/extjs/custom/search_16.png',
                			cls: 'x-btn-text-icon',
							xtype: 'button',
                			handler: function() {
                    			AbonApi.abonent_get({
                            		code: (this.searchfield.getValue() || 0)
                        		},this.preload.createDelegate(this));
                			},
                			scope: this
            			},
						this.personfield = new Ext.form.Label({
							text: '...',
							width: 200
						}),
						this.addressfield = new Ext.form.Label({
							text: '...',
							width: 200
						}),								
						
					]
				},{
					xtype: 'form',
					width:  500,
					items: [
						this.bankdate = new Ext.form.DateField({
							fieldLabel: 'Дата снятия',
							format: 'Y-m-d'
						}),
						this.sum = new Ext.form.NumberField({
							fieldLabel: 'Сумма',
							baseChars: '1234567890.'
						}),
						this.descr = new Ext.form.TextField({
							fieldLabel: 'Описание',							
						}),					
					],
					bbar:[{					
                        xtype: 'tbbutton',
                        cls: 'x-btn-text-icon',
                        icon: '/static/extjs/custom/tick_16.png',
                        text: 'Сохранить',
                        colspan: 3,
                        width: 100,
                        handler: function(){
                            if(this.feetype<1) {
								Ext.ux.msg('Ошибка ввода',"выберите тип снятия",Ext.Msg.ERROR)
								return false
							}
							if(this.abonent<1) {
								Ext.ux.msg('Ошибка ввода',"выберите абонента",Ext.Msg.ERROR)
								return false
							}
							if (!this.bankdate.getValue()) {
								Ext.ux.msg('Ошибка ввода',"введите правильную дату",Ext.Msg.ERROR)
								return false
							}
							if (parseFloat(this.sum.getValue() || 0) <= 0) {
								Ext.ux.msg('Ошибка ввода',"введите правильную сумму",Ext.Msg.ERROR)
								return false
							}
							AbonApi.make_fee({
								type: this.feetype,
								abonent: this.abonent,
								bankdate: this.bankdate.getValue(),
								sum: parseFloat(this.sum.getValue()),	
								descr: this.descr.getValue()
							},this.fee_callback.createDelegate(this));
                        },
                        scope: this                        
                    }]
				}			
			],
            listeners: {
                activate: {
                    fn: function(obj) {
						if (parseInt(this.oid)>0) {
							AbonApi.abonent_get({
                            	uid: (parseInt(this.oid) || 0)
                        	},this.preload.createDelegate(this));
						}
                    },
                    scope: this
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
			preload: function(response) {
				if(response.success) {	
					this.searchfield.setValue(response.data[0]['code'])					
					this.personfield.setText(response.data[0]['person'])
					this.addressfield.setText(response.data[0]['address'])
					this.abonent = response.data[0]['id']
				}
			},
			fee_callback: function(response) {
				this.searchfield.setValue('')
				this.personfield.setText('...')
				this.addressfield.setText('...')				
			},
			register: 0,
			abonent: 0
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.FeeForm.superclass.initComponent.apply(this, arguments);
    }    
})