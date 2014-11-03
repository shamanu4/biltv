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

Ext.ux.traceback = function() {
	
	function createBox(text,token) {
		
		return [
    	'<form action="/traceback/" id="traceback-form" method="POST">',
    		'<input type="hidden" name="csrfmiddlewaretoken" value="'+token+'" />',
    		'<label for="traceback-content">трейсбек:</label>',
    		'<br />',
        	'<textarea id="traceback-content" cols="75" rows="8" name=traceback disabled>',
        		text,         
        	'</textarea>',
        	'<br />',
        	'<label for="traceback-description">',
        		'опишите Ваши действия перед сбоем <br />',
        		'это поможет решить проблему быстрее <br />',
        	'</label>',
        	'<textarea id="traceback-descripton" cols="75" rows="10" name=traceback-descr>',        		         
        	'</textarea>',
    		'<br />',
        '</form>',
    	].join('')
	}
	
	return function(title,text,token) {
		
		new Ext.Window({			
			title: title,
	        plain: true,
	        html:createBox(text,token), 
	        modal: true,
	        width: 600,
	        buttons: [{
	            text: 'отослать отчёт',
	            handler: function() {
	            	$("#traceback-content").removeAttr("disabled");
	            	Ext.get("traceback-form").dom.submit();	          	    	           
	            }
	        }],
	    }).show();
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
            title: 'Панель оператора КТБ',
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
                    'text': 'Реестры',
                    'oid': 0,
                    'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-payment-button',
                    'handler': Engine.menu.cashier.payment.openForm,
                    'text': 'Оплаты',
					'oid': 0,
					'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-registers-form-button',
                    'handler': Engine.menu.cashier.register.openForm,
                    'text': 'Отчёт по оплатам',
                    'oid': 0,
                    'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-report-button',
                    'handler': Engine.menu.cashier.report.launch,
                    'text': 'Отчет по задолженностям',
                    'oid': 0,
                    'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-illegal-button',
                    'handler': Engine.menu.cashier.illegal.openGrid,
                    'text': 'Отчет по нелегалам',
                    'oid': 0,
                    'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-statements-button',
                    'handler': Engine.menu.cashier.statements.launch,
                    'text': 'ПриватБанк Выписки',
                    'oid': 0,
                    'my_owner_ct_id':0
                },
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
    searchAction: function() {
        this.store.baseParams.filter_value = this.searchfield.getValue()
		this.store.load()
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
                         var index = Ext.ux.cities_combo_store.findExact('id',value)
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
                         var index = Ext.ux.streets_combo_store.findExact('id',value)
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
                         var index = Ext.ux.houses_combo_store.findExact('id',value)
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

Ext.ux.IllegalGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'illegal-store',
            ds_model: illegal_ds_model,
            title: 'Нелегалы',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Код", dataIndex: 'code', editor: new Ext.form.TextField()},
                {header: "Дата", dataIndex: 'date', xtype: 'datecolumn', editor: new Ext.form.DateField({format:'Y-m-d'}), format:'Y-m-d'},
                {header: "Погашено", dataIndex: 'deleted', xtype: 'checkcolumn', editable:true},
                {header: "Комментарий", dataIndex: 'comment', editor: new Ext.form.TextField(), width:300},
            ],
});

Ext.ux.AbonentGrid = Ext.extend(Ext.ux.CustomGridNE ,{
	initComponent: function() {
        var config = {
        	store:  new Ext.data.DirectStore({
    			api: {
        			read: AbonentGrid.read,
        			create: AbonentGrid.foo,
        			update: AbonentGrid.foo,
        			destroy: AbonentGrid.foo
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
            			'code',
            			'person',
            			'person__passport',
            			'address',
            			'bill__balance',
            			'comment',
            			'confirmed',
						'disabled',
						'deactivated',
        			]
    			}),    		
        		listful: true,
    			baseParams : {
        			start:0,
        			limit:16,
        			filter_fields:['person__firstname','person__lastname','person__passport','person__sorting',
        			'code','address__building__street__name','address__building__sorting','address__sorting'],
        			filter_value:''
       			}
    		}),
            title: 'Список абонентов',
            closable: true,
            columns: [
                {header: "Id", dataIndex: 'id', width:100, sortable:true},
                {header: "Code", dataIndex: 'code', width:100, sortable:true},
                {header: "ФИО", dataIndex: 'person', width:180, sortable:true},
                {header: "Паспорт", dataIndex: 'person__passport', width:100, sortable:true},
                {header: "Адрес", dataIndex: 'address', width:220, sortable:true},
                {header: "Баланс", dataIndex: 'bill__balance', width:60, sortable:true},
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
                {header: "Отключен", dataIndex: 'deactivated', width:80, sortable:false},
                {header: " ", dataIndex: 'id', width: 28,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        return '<div class="inline_edit_button abonent_edit_button" id="'+value+'" code="'+record.data.code+'" confirmed="'+record.data.confirmed+'" dis="'+record.data.disabled+'"></div>'
                    }
                },
            ],
            addAction: function(){
                Engine.menu.cashier.abonent.openForm()
            },           
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonentGrid.superclass.initComponent.apply(this, arguments);
   },
   listeners: {
                afterrender : {
                    fn: function(obj) {
						this.topToolbar.addSpacer()
						this.topToolbar.addText("№ декодера")
						this.optsearchfield = new Ext.form.TextField({id:"search-by-decoder",width:50,
							listeners: {
                    			specialkey: {
                        			fn: function(field, e){                            
                            			if (e.getKey() == e.ENTER) {                                
                                			this.optSearchAction()
                            			}
                        			},
                        			scope: this
                    			}
                    		}
						})
						this.topToolbar.add(this.optsearchfield)
						this.topToolbar.addButton({
                			icon: '/static/extjs/custom/search_16.png',
                			cls: 'x-btn-text-icon',
                			handler: function() {
                    			this.optSearchAction()
                			},
                			scope: this
            			}),
            			this.topToolbar.addButton({
                			icon: '/static/extjs/custom/delete_16.png',
                			cls: 'x-btn-text-icon',
                			handler: function() {
                    			this.optsearchfield.setValue('')
                    			this.store.baseParams.filter_value = ''
                    			this.store.load()
                			},
                			scope: this
            			})            
                    }
                }
            },
	searchAction: function() {
            	this.store.baseParams.filter_value = this.searchfield.getValue()
                this.store.baseParams.filter_fields = ['person__firstname','person__lastname','person__passport','person__sorting',
        		'code','address__building__street__name','address__building__sorting','address__sorting'],
                this.store.load()
            },
	optSearchAction: function() {
				var v = this.optsearchfield.getValue()
            	this.store.baseParams.filter_value = parseInt(v-0)+''       	
            	this.optsearchfield.setValue(this.store.baseParams.filter_value)
            	this.store.baseParams.filter_fields = ['cards__num__exact']
            	if(this.store.baseParams.filter_value!='NaN') {
                	this.store.load()
                }
            }, 
});

Ext.ux.CardGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'card-store',
            title: 'Карточки',
            ds_model: card_ds_model,
            columns: [
                {header: "Id", dataIndex: 'id', width:100},
                {header: "Num", dataIndex: 'num', width:100, editor: new Ext.form.TextField()},
                {header: "Owner", dataIndex: 'owner', width:300},
                {header: "Active", dataIndex: 'active', width:100, xtype: 'booleancolumn', default:true},
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
                {header: "Id", dataIndex: 'id', width:70, editable:false},
                {header: "Source", dataIndex: 'source', width:165, editable:false, editor: new Ext.ux.SourceCombo(),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (true) {
							this.editable = true
						}
						return value;
					}
                },
                {header: "Total", dataIndex: 'total', width:100, editable:false, editor: new Ext.form.TextField(),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (true) {
							this.editable = true
						}
						return value;
					} 
				},
                {header: "Start", dataIndex: 'start', width:100, editable:false, editor: new Ext.form.DateField({format:'Y-m-d'}),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (true) {
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
				{header: "End", dataIndex: 'end', width:100, editable:false, editor: new Ext.form.DateField({format:'Y-m-d'}),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (true) {
							this.editable = true
						}
						return value;
					}
				},
				{header: "Bank", dataIndex: 'bank', width:100, editable:false, editor: new Ext.form.DateField({format:'Y-m-d'}),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						if (true) {
							this.editable = true
						}
						return value;
					}
				},
				{header: "закрыт", dataIndex: 'closed', width:40, editable:false,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        return '<div class="abonent_disabled_status_'+value+'"></div>'
                    }
                },
				{header: " ", dataIndex: 'id', width: 28,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                    	if(record.data.closed) {
                    	  return ' '		
                    	} else {
                    	  return '<div class="inline_cash_button register_cash_button" id="'+value+'" source="'+record.data.source+'"></div>'	
                    	}                        
                    }
                },
                {header: "платежи", dataIndex: 'payments_total', width:80, editable:false},
                {header: "засчитано", dataIndex: 'payments_maked', width:80, editable:false,
                   renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                      if(!(record.data.payments_maked==record.data.payments_total)) {
                        return '<div class="maked_false_class">'+value+'</div>'  	
                      } else {
                      	return '<div class="maked_true_class">'+value+'</div>'
                      }
                   }
                },
                {header: "сума", dataIndex: 'payments_maked_sum', width:80, editable:false,
                    renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                        if(!(record.data.payments_maked_sum==record.data.total)) {
                            return '<div class="maked_false_class">'+value+'</div>'
                        } else {
                            return '<div class="maked_true_class">'+value+'</div>'
                        }
                    }
                },
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
                    	/* moved to ui-index autoload 
                    	
                        $(".register_edit_button").live('click', function(e) {
                            Engine.menu.cashier.register.openForm(this.id);
                        })
						$(".register_cash_button").live('click', function(e) {
                            Engine.menu.cashier.register.partiallyConfirm(this.id, $(this).attr('source'));
                        })
                        
                        */
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
							title: 'Реестр',
							items: [
								this.registercombo = new Ext.form.ComboBox({
									store: new Ext.data.DirectStore({
    									api: {
        									read: AbonApi.registers_get_last,
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
        									limit:1000,        							
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
												this.startdate.setValue(record.data.start)
												this.enddate.setValue(record.data.end)
												//this.preload()
											},
											scope: this
										}
									}
								}),	
								this.resetregister = new Ext.Button({
									width: 64,
									text: 'сбросить',
									listeners: {
										click: {
											fn: function(button, event) {
												this.registercombo.reset()
												this.register = null
												//this.preload()
											},
											scope: this
										}
									}
								})						
							]
						},					
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
								width: 200,
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
							this.resetadmin = new Ext.Button({
								width: 64,
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
						{
							xtype: 'buttongroup',
							title: 'Интервал',
						 	items: [
								this.startdate = new Ext.form.DateField({
									width: 100,
									value: new Date(),
									format: 'Y-m-d',
								}),
								this.enddate = new Ext.form.DateField({
									width: 100,
									value: new Date(),
									format: 'Y-m-d',
								}),
								this.resetadmin = new Ext.Button({
									width: 64,
									text: 'сегодня',
									listeners: {
										click: {
											fn:function(button, event) {
												this.startdate.setValue(new Date());
												this.enddate.setValue(new Date());												
											},
											scope: this
										}
									}
								})
							] 
						},
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
                    		start_date:null,
							end_date:null,
                		}
					}),
					columns: [
        				{header: "Id", dataIndex: 'id', width:45},
        				{header: "Timestamp", dataIndex: 'timestamp', width:120, sortable: true},
        				{header: "Абонент", dataIndex: 'onwer_code', width:80},
						{header: "ФИО", dataIndex: 'onwer_name', width:160},        				
						{header: "Сума", dataIndex: 'sum', width:40, sortable: true},
						{header: "Оператор", dataIndex: 'admin', width:80, sortable: true},
        				{header: "Банк", dataIndex: 'source__name', width:80, sortable: true},
						{header: "Квитанция", dataIndex: 'bank_date', width:80, sortable: true},
        				{header: "Описание", dataIndex: 'inner_descr', width:180},
						{header: " ", dataIndex: 'id', width: 28,
                    		renderer: function(value, metaData, record, rowIndex, colIndex, store) {
								if(record.data.maked) {
									return ''
								} else {
									return '<div class="inline_delete_button register_delete_payment" id="'+value+'"></div>'	
								}                        		
                    		}
                		},   				
    				],
				})
			],
			listeners: {
            	afterrender: {
                	fn: function(obj) {
						if(!this.oid) {
							return false	
						}							
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
						/*	moved to ui-index autoload
						 
						$(".register_delete_payment").live('click', function(e) {
                            Engine.menu.cashier.register.deletePayment(this.id,this);
                        })
                        
                        */
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
			preload: function() {				
				//if(!this.register) {
				//	Ext.ux.msg('Выберите реестр','',Ext.Msg.ERROR)
				//  return false
				//}
				Ext.get('loading').show();
            	Ext.get('loading-mask-half').show();
				this.resultsgrid.store.setBaseParam('register_id',this.register)
				this.resultsgrid.store.setBaseParam('admin_id',this.admin)
				this.resultsgrid.store.setBaseParam('start_date',this.startdate.getValue())
				this.resultsgrid.store.setBaseParam('end_date',this.enddate.getValue())
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
			},
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
            onShow: function() {
            	this.getForm().items.items[1].focus(false,100)
            },
            listeners: {
                afterrender : {
                    fn: function(obj) {
                        this.parent_form.children_forms.person.obj=this
                        if(this.oid) {
                            this.loadaction()                            
                        }
						this.getForm().items.items[1].focus(false,100)              
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
            onShow: function() {
            	
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
                icon: '/static/img/icons/green/16x16/Refresh.png',
                handler: function(){
					this.refresh()
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
            },{
                text: 'трансфер',
                handler: function(){
                    Engine.menu.cashier.transfer.openForm(this.oid,this.parent_form.id)
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
            	this.body.dom.innerHTML='<div class="balance_digits_positive">...</div>'
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
            scope: this
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
                afterrender: {
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
							var tpstore = sm.grid.parent_form.children_forms.tariffs.obj.store							
                            if (typeof(record.id)=='number') {								
                                tpstore.setBaseParam('card_id',record.id)
								tpstore.load()                                
                            } else {
                                //this.store.load()
                            }
                        },
                        scope: this
                    }
                }
            }),
            columns: [
        		{header: "Id", dataIndex: 'id', width:40},
        		{header: "Num", dataIndex: 'num', width:80, editable: false,
            		renderer: function(value, metaData, record, rowIndex, colIndex, store) {
            			if (value===undefined) {
                    		this.editable=true
                    		var store = Ext.ux.free_card_combo_store
                    		store.load()
                		}
                		if (value<0) {
                    		return '<b>CaTV</b>';
                		} else {
                    		return '<b>'+value+'</b>';
                		}
            		},
            		editor: new Ext.ux.FreeCardCombo(),
        		},
        		{header: "Active", dataIndex: 'active', width:40,
            		renderer: function(value, metaData, record, rowIndex, colIndex, store) {
            			if(record.data.num>0){
            				if (value==true) {
                    			return '<img src="/static/extjs/custom/tick_16.png" class="abon_card_deactivate" val="'+record.data.id+'">';
                			} else {
                    			return '<img src="/static/extjs/custom/block_16.png" class="abon_card_activate" val="'+record.data.id+'">';
                			}
                		} else {
                			if (value==true) {
                    			return '<img src="/static/extjs/custom/tick_16.png">';
                			} else {
                    			return '<img src="/static/extjs/custom/block_16.png">';
                			}
                		}
            		},
            		scope: this
        		},
        		{header: "Activated", dataIndex: 'activated', width:140, editable: true,
        			editor: new Ext.form.DateField({format:"Y-m-d"}),
        		},
        		{header: "", dataIndex: 'id', width:26,        		    
            		renderer: function(value, metaData, record, rowIndex, colIndex, store) {
            			if(record.data.num>0) {
                			return '<img src="/static/extjs/custom/delete_16.png"  class="abon_card_unbind" val="'+record.data.id+'">';
                	    } else {
                	    	return ""
                	    }
            		},
            		scope: this
        		},
    		],
    		abon_card_func: function(func,param) {
        	}
        }        
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCardsGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Карточки',
    ds_model: card_ds_model,
        
});

Ext.reg('ext:ux:abon-cards-grid', Ext.ux.AbonCardsGrid);

Ext.ux.CardTpCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.card_tp_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'name',
            mode: 'local'
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.CardTpCombo.superclass.initComponent.apply(this, arguments);
    }
}),

Ext.reg('ext:ux:free-cards-combo', Ext.ux.FreeCardCombo);


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
                        'extra',
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.cards_tp_get,
                    create: AbonApi.cards_tp_add,
                    update: AbonApi.cards_tp_update,
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
                        	var tpstore = Ext.ux.card_tp_combo_store
                        	tpstore.load()
                            //sm.grid.parent_form.children_forms.tariffs.obj.setTitle('13')
                        },
                    scope: this
                    }
                }
            }),
            columns: [
        		{header: "Id", dataIndex: 'id', width:40},
        		{header: "Tariff", dataIndex: 'tariff', width:145,
        			editor: new Ext.ux.CardTpCombo(),
        		},
        		{header: "Active", dataIndex: 'active', width:40,
            		renderer: function(value, metaData, record, rowIndex, colIndex, store) {
            			if (value==true) {
                    		return '<img src="/static/extjs/custom/tick_16.png" class="abon_tp_deactivate" val="'+record.data.id+'">';
                		} else {
                    		return '<img src="/static/extjs/custom/block_16.png" class="abon_tp_activate" val="'+record.data.id+'">';
                		}
            		}
        		},        		
        		{header: "Activated", dataIndex: 'activated', width:120, editable: true,
        			editor: new Ext.form.DateField({format:"Y-m-d"}),
        		},
        		{header: "", dataIndex: 'id', width:26,
            		renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                		return '<img src="/static/extjs/custom/delete_16.png" class="abon_tp_unbind" val="'+record.data.id+'">';
            		}
        		},
        		{header: "login", dataIndex: 'extra', width:80,
        			editor: new Ext.form.TextField(),
        		},
        		{header: "", dataIndex: 'id', width:26,
            		renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                		return '<img src="/static/extjs/custom/right_16.png" class="abon_tp_move" val="'+record.data.id+'">';
            		}
        		},
    		]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCardsTpGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Карточки',
    ds_model: tariff_ds_model,    
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
                        'register',
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
            pageSize: 12,
    		height: 380,    
            listeners: {
                afterrender : {
                    fn: function(obj) {
                    	/* moved to ui-index autoload
                    	                      	                     
                       	$(".abonent_delete_payment").live('click', function(e) {
                       		Engine.menu.cashier.register.deletePayment(e.currentTarget.getAttribute('val'),e.currentTarget);
                        })
                        $(".abonent_transfer_payment").live('click', function(e) {
                       	    Engine.menu.cashier.register.transferPayment(e.currentTarget.getAttribute('val'),e.currentTarget);
                        })
                        
                        */
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
		{header: "Source", dataIndex: 'source__name', width:110, sortable: true},
        {header: "Register", dataIndex: 'register', width:65, sortable: true},
		{header: "Bank date", dataIndex: 'bank_date', width:80, sortable: true},
        {header: "Descr", dataIndex: 'inner_descr', width:200},
        {header: "", dataIndex: 'id', width:26,
			renderer: function(value, metaData, record, rowIndex, colIndex, store) {
				if(record.data.maked) {
			    	return '<div class="inline_rollback_button abonent_rollback_payment" id="roll_pay_"'+value+'" val="'+value+'"></div>'	
            	} else {
					return '<div class="inline_delete_button abonent_delete_payment" id="del_pay_'+value+'" val="'+value+'"></div>'	
				}                        		
        	}
       },
       {header: "", dataIndex: 'id', width:26,
			renderer: function(value, metaData, record, rowIndex, colIndex, store) {
				return '<div class="inline_transfer_button abonent_transfer_payment" id="trans_pay_'+value+'" val="'+value+'"></div>'	
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
    height: 380
});


Ext.reg('ext:ux:abon-payments-grid', Ext.ux.AbonPaymentsGrid);

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
                        'inner_descr',
                        'rolled_by'
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
            pageSize: 12,
    		height: 380,       
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
                return '<div class="inline_rollback_button abonent_rollback_fee" id="roll_fee_"'+value+'" val="'+value+'"></div>'	
            }
        }
    ],
	viewConfig: {
        forceFit: true,
		getRowClass: function(record, index, rowParams, store) {
            var c = record.get('rolled_by');
            if (c>0) {
                return ''
            }
            var c = record.get('maked');
            if (c) {
				return 'maked_true_class';
			} else {
				return 'maked_false_class';				
			}
        }
    },
    pageSize: 12,
    height: 3800
});

Ext.reg('ext:ux:abon-fees-grid', Ext.ux.AbonFeesGrid);

Ext.ux.AbonHistoryGrid = Ext.extend(Ext.ux.CustomGridNE ,{
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
                        'timestamp',
                        'date',
                        'text',
                        'descr',
                        'cnt'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.abon_history_get,
                    create: AbonApi.foo,
                    update: AbonApi.foo,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:12,
                    foo:'bar',
                    uid:this.oid || 0,
                }
            }),
            pageSize: 12,
    		height: 380,   
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
        Ext.ux.AbonHistoryGrid.superclass.initComponent.apply(this, [config]);
    },    
    columns: [
        {header: "Id", dataIndex: 'id', width:45},
        {header: "Timestamp", dataIndex: 'timestamp', width:180, sortable: true},
        {header: "Дата", dataIndex: 'date', width:150, sortable: true},
        {header: "Text", dataIndex: 'text', width:180},
        {header: "Descr", dataIndex: 'descr', width:300},
        {header: " ", dataIndex: 'cnt', width:26,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {            	
            	if((value>1)&&(!(value % 2))) {
                	return '<div class="inline_delete_button card_history_deldete" id="del_ch_'+record.data.id+'" val="'+record.data.id+'"></div>'
            	} 
            }
        },        
    ],
});

Ext.reg('ext:ux:abon-history-grid', Ext.ux.AbonHistoryGrid);

Ext.ux.AbonCreditsGrid = Ext.extend(Ext.ux.CustomGrid ,{
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
                        'bill',
                        'sum',
                        'valid_from',
                        'valid_until',
                        'valid',
                        'manager'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.abon_credit_get,
                    create: AbonApi.abon_credit_add,
                    update: AbonApi.abon_credit_update,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:10,
                    uid:this.oid,
                }
            }),
            columns: [
                {header: "Id", dataIndex: 'id', width:40},
                {header: "Bill", dataIndex: 'bill', width:65},
                {header: "Sum", dataIndex: 'sum', width:65, editor: new Ext.form.TextField()},
                {header: "Valid from", dataIndex: 'valid_from', width:120,
                    //editor: new Ext.form.DateField({format:"Y-m-d"})
                },
                {header: "Valid until", dataIndex: 'valid_until', width:120,
                    editor: new Ext.form.DateField({format:"Y-m-d"})
                },
                {header: "manager", dataIndex: 'manager', width:80}
            ],
            viewConfig: {
                forceFit: true,
                getRowClass: function(record, index, rowParams, store) {
                    var c = record.get('valid');
                    if (c) {
                        return 'maked_true_class';
                    } else {
                        return '';
                    }
                }
            },
            pageSize: 12,
            height: 380
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCreditsGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Кредиты',
    ds_model: credit_ds_model
});

Ext.reg('ext:ux:abon-credits-grid', Ext.ux.AbonCreditsGrid);


Ext.ux.AbonIllegalGrid = Ext.extend(Ext.ux.CustomGrid ,{
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
                        'date',
                        'comment',
                        'deleted'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.abon_illegal_get,
                    create: AbonApi.abon_illegal_add,
                    update: AbonApi.abon_illegal_update,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:10,
                    uid:this.oid
                }
            }),
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Дата", dataIndex: 'date', xtype: 'datecolumn', editor: new Ext.form.DateField({format:'Y-m-d'}), format:'Y-m-d'},
                {header: "Погашено", dataIndex: 'deleted', xtype: 'checkcolumn', editable:true},
                {header: "Комментарий", dataIndex: 'comment', editor: new Ext.form.TextField(), width:300},
            ],
            viewConfig: {
                forceFit: true,
                getRowClass: function(record, index, rowParams, store) {
                    var c = record.get('deleted');
                    if (c) {
                        return '';
                    } else {
                        return 'maked_false_class';
                    }
                }
            },
            pageSize: 12,
            height: 380
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonIllegalGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Нелегалы',
    ds_model: Ext.data.Record.create([
			'id',
            'date',
            'comment',
            'deleted'
    ])
});

Ext.reg('ext:ux:abon-illegal-grid', Ext.ux.AbonIllegalGrid);



Ext.ux.AbonCommentsPanel = Ext.extend(Ext.Panel ,{
	    initComponent: function() {
        var config = {
            closable: false,
			frame: true,
            defaults: {
                frame: true,
                split: true    
            },            
            items: [
			this.comment_field = new Ext.form.TextArea({
				xtype: 'textarea',
				width: 900,
			}),
			{
            	xtype: 'tbbutton',
            	cls: 'x-btn-text-icon',
            	icon: '/static/extjs/custom/tick_16.png',
            	text: 'Сохранить',
				listeners: {
                	click : {
                    	fn: function(obj) {
							AbonApi.comment_set({
                            	uid: (this.oid || 0),
								comment: this.comment_field.getValue()
                        	});
                    	},
                    	scope: this
                	},
            	},
			}],
			listeners: {
                afterrender : {
                    fn: function(obj) {
						AbonApi.comment_get({
                            uid: (this.oid || 0),							
                        },this.getCommentCallback.createDelegate(this));
                    },
                    scope: this
                },
            },
			getCommentCallback: function(response) {
				this.comment_field.setValue(response.data.comment)
			},
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
                    },{                            
                        title: 'История',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                        	xtype: 'ext:ux:abon-history-grid',
                        	oid: this.oid
                        }]
                    },{
                        title: 'Кредиты',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype: 'ext:ux:abon-credits-grid',
                            oid: this.oid
                        }]
                    },{
                        title: 'Нелегалы',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype: 'ext:ux:abon-illegal-grid',
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
            items: [
			this.person_form = {
                title: 'Абонент',
                xtype: 'ext:ux:person-form',
                oid: this.oid,
                parent_form: this
            },
			this.address_form = {
                title: 'Адрес',
                xtype: 'ext:ux:address-form',
                oid: this.oid,
                parent_form: this
            },
			this.balance_form = {
                title: 'Баланс',
                xtype: 'ext:ux:balance-form',
                oid: this.oid,
                parent_form: this
            },
			this.mid_toolbar = {
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
                                    if((this.confirmed=="true")||(this.confirmed=="true")) {
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
                        colspan: 3,
                        xtype: 'tbtext',
						width: 100,
                        listeners: {
                            afterrender : {
                                fn: function(obj) {
                                    this.children_forms.disabled.obj=obj
                                    if((this.dis=="false")||(this.dis==false)) {
                                        obj.setText("Подключен")
										obj.addClass("bold_green")										
                                    } else {
                                    	obj.setText("Отключен")
										obj.addClass("bold_red")
                                    }
                                },
                                scope: this
                            }
                        },
                        scope: this
                    },{
                        xtype: 'tbseparator'
                    },
					this.disable_enable_btn = {
                        xtype: 'tbbutton',
                        cls: 'x-btn-text-icon',
                        icon: '/static/extjs/custom/tick_16.png',
                        text: 'loading...',
                        colspan: 3,
                        width: 100,
                        handler: function(){
                            (function(){this.disable_enable();}).defer(500,this);
                        },
						listeners: {
                            afterrender : {
                                fn: function(obj) {
                                	if((this.dis=="false")||(this.dis==false)) {
                                        obj.setText("Отключить")
										obj.setIcon("/static/extjs/custom/delete_16.png")                                        
                                    } else {
										obj.setText("Подключить")
										obj.setIcon("/static/extjs/custom/tick_16.png")
									}
                                },
                                scope: this
                            }
                        },
                        scope: this                        
                    },{
                        xtype: 'tbseparator'
                    },
                    this.refresh_button = {
                    	xtype: 'tbbutton',
                		icon: '/static/img/icons/green/16x16/Refresh.png',
                		handler: function(){
							this.refresh()
                		},
                		scope: this
            		},{
                        xtype: 'tbseparator'
                    },
                    /*
                    this.recalculate_button = {
                    	xtype: 'tbbutton',
                		icon: '/static/img/icons/green/16x16/Tool.png',
                		handler: function(){
							this.recalculate()
                		},
                		scope: this
            		},{
                        xtype: 'tbseparator'
                    }
                    */
                   this.delete_button = {
                    	xtype: 'tbbutton',
                		icon: '/static/img/icons/red/16x16/Cancel.png',
                		handler: function(){
                			if(confirm('Удалить абонента?')) {
								this.abon_delete()
							}
                		},
                		scope: this
            		},{
                        xtype: 'tbseparator'
                    }
            	]
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
					//disabled: this.children_forms.disabled.obj.checked,
					//activated: this.children_forms.address.obj.activated_field.value,
					//deactivated: this.children_forms.address.obj.deactivated_field.value                       
                },this.submitcallback.createDelegate(this));
            },
            submitcallback: function(result,e) {                
                if(result.success) {                    
                    //Ext.ux.abonent_store.load()
					this.setTitle("абон: "+(result.data[0]['code'] || '<новый>'))
					if (!this.oid) {
						this.hide()
						this.ownerCt.remove(this.id)			
						Engine.menu.cashier.abonent.openForm(result.data[0]['id'], result.data[0]['code'], result.data[0]['confirmed'], result.data[0]['disabled']);
					}					
                }
            },
            refresh: function() {
            	AbonApi.abonent_get({
					uid: (this.oid || 0)
				},this.refreshcallback.createDelegate(this));
            },
            refreshcallback: function(result,e) {                
                if(result.success) {                    
                    this.setTitle("абон: "+(result.data[0]['code'] || '<новый>'))						
					this.hide()
					this.ownerCt.remove(this.id)			
					Engine.menu.cashier.abonent.openForm(result.data[0]['id'], result.data[0]['code'], result.data[0]['confirmed'], result.data[0]['disabled']);					
                }
            },
            recalculate: function() {
            	if (confirm("пересчитать баланс абонента?")) {
            		Ext.get('loading').show();
            		Ext.get('loading-mask-half').show();
					AbonApi.launch_hamster({
						uid: (this.oid || 0)
					},this.recalculatecallback.createDelegate(this));
				}
            },
			recalculatecallback: function(result,e) {
				Ext.get('loading').hide();
            	Ext.get('loading-mask-half').fadeOut('fast');
                if(result.success) {       
                	this.refresh()             
                }
            },
            abon_delete: function() {
            	AbonApi.abonent_delete({
					uid: (this.oid || 0)
				},this.deletecallback.createDelegate(this));
            },
            deletecallback: function(result,e) {
			    if(result.success) {       
                	this.hide()
					this.ownerCt.remove(this.id)	             
                }
            },            
            disable_enable:function() {
				if((this.dis=="false")||(this.dis==false)) {
					this.abon_disable()					
				} else {
					this.abon_enable()
				}
			},
			abon_enable: function() {
				Engine.menu.cashier.abon_enable.openForm(this.oid,this.id)
			},
			abon_disable: function() {
				Engine.menu.cashier.abon_disable.openForm(this.oid,this.id)
			},
			children_forms_ready: function() {
                if((this.children_forms.person.ready2)&&(this.children_forms.address.ready2)) {
                    this.submitaction()
                } else {
                	//Ext.ux.msg('Ошибка ввода',"заполните обязательные поля",Ext.Msg.ERROR)
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
                    	obj.getEl().on('keypress', function(e,o) {
               				if(e.ctrlKey) {
								if(e.button==111) {
									// Ctrl+P 
									Engine.menu.cashier.payment.openForm(this.oid)									
								}
								else if(e.button==101) {
									// Ctrl+F 
									Engine.menu.cashier.fee.openForm(this.oid)
								}
								else if(e.button==113) {
									// Ctrl+R
									this.refresh()
								}
								else if(e.button==114) {
									// Ctrl+S
									(function(){this.submitprep();}).defer(500,this);
								}
								else if(e.button==96) {
									// Ctrl+A
									this.disable_enable()
								}
								else if(e.button==116) {
									// Ctrl+U
									this.children_forms.person.obj.items.items[1].focus()									
								}
								else if(e.button==104) {
									// Ctrl+I
									this.children_forms.address.obj.items.items[1].focus()									
								}
							}            				               				
      					}, obj);
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
                },
                show: {
                    fn: function(obj) {
                    	if(this.children_forms.person.obj && this.children_forms.address.obj) {
                        	this.children_forms.person.obj.onShow()
                        	this.children_forms.address.obj.onShow()
                    	} else {
                      		(function(){
                      			if(this.children_forms.person.obj && this.children_forms.address.obj) {
									this.children_forms.person.obj.onShow()
                        			this.children_forms.address.obj.onShow()
                        		}                    		
							}).defer(1000,this);
                    	}
                    },
                    scope: this
                },                
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
							//forceSelection: true,
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
                            		code: (this.searchfield.getValue() || 0),                            		
                        		},this.preload.createDelegate(this));
                			},
                			scope: this
            			},
            			this.personfield = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonApi.abonent_get_by_code,
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
        							fields: [
            							'id',
            							'person',
            							'disabled',						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,
        							filter_disabled: 1     							
    							},
    						}),
							valueField: 'id',
            				displayField: 'person',
							forceSelection: true,
							emptyText: 'Абонент',
							editable: false,
    						triggerAction: 'all',
							listeners: {
								change: {
									fn: function(combo,newval,oldval) {
										var record_new = combo.store.getAt(combo.store.findExact('id',newval))
										//var record_old = combo.store.getAt(combo.store.findExact('id',oldval))
										this.addressfield.setText(record_new.json.address)
										if(record_new.data.disabled) {
											Ext.ux.msg('Внимание!',"абонент отключен", Ext.Msg.INFO);
											combo.addClass('combo-bg-red')
										} else {
											combo.removeClass('combo-bg-red')
										}
										this.abonent = newval
										this.oid=0								
									},
									scope: this
								}
							}
						})
					]
					
				},{
					xtype: 'panel',
					width:  500,
					layout: 'form',
					columnWidth: 1,
					items: [
						this.addressfield = new Ext.form.Label({
							fieldLabel: 'адресc:',
							text: '...'
						})
					]
				},{
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
        							limit:1000,        							
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
                            this.submitaction()
                        },
                        scope: this                        
                    }]
				}			
			],
            listeners: {
            	afterrender : {
                    fn: function(obj) {
                    	obj.getEl().on('keypress', function(e,o) {
               				if(e.ctrlKey) {
								if(e.button==114) {
									// Ctrl+S
									(function(){this.submitaction();}).defer(500,this);
								}
							}            				               				
      					}, obj);			
                    },
                    scope: this
                },
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
					//this.personfield.setText(response.data[0]['person'])
					this.personfield.setRawValue('')
					this.personfield.store.setBaseParam('code',response.data[0]['code'])
					this.personfield.store.load({
						callback: this.afterload.createDelegate(this),
					})
				}
				this.searchfield.focus()
			},
			afterload: function(response) {
				if(this.personfield.store.data.length) {
					this.personfield.setValue(parseInt(this.oid) || this.personfield.store.getAt(0).id)				
					this.abonent = parseInt(this.oid) || this.personfield.store.getAt(0).id
					this.oid=0
					this.personfield.fireEvent('change',this.personfield,this.abonent)
				} else {
					Ext.ux.msg('Сбой загрузки формы',"абонент не найден или отключен", Ext.Msg.ERROR);
				}
			},
			submitaction: function() {
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
			payment_callback: function(response) {
				this.searchfield.setRawValue('');
				this.personfield.setRawValue('');
				this.abonent = 0;
				if(this.my_owner_ct_id) {
					Ext.getCmp(this.my_owner_ct_id).refresh()
					(function(){
						this.hide()
						this.ownerCt.remove(this.id);	
					}).defer(300,this);
				}			
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
						this.personfield = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonApi.abonent_get_by_code,
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
        							//pizdec
        							fields: [
            							'id',
            							'person',
            							'disabled',						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,        							
    							},
    						}),
							valueField: 'id',
            				displayField: 'person',
							forceSelection: true,
							emptyText: 'Абонент',
							editable: false,
    						triggerAction: 'all',    							
							listeners: {
								change: {
									fn: function(combo,newval,oldval) {
										var record_new = combo.store.getAt(combo.store.findExact('id',newval))
										var record_old = combo.store.getAt(combo.store.findExact('id',oldval))
										if(record_new.data.disabled) {
											alert("Внимание! Абонент отключен")
											combo.addClass('combo-bg-red')
										} else {
											combo.removeClass('combo-bg-red')
										}
										this.abonent = newval		
										this.oid=0								
									},
									scope: this
								}
							}
						}),														
					]
				},{
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
							//forceSelection: true,
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
						this.allowzero = new Ext.form.Checkbox({
							fieldLabel: 'Разрешить 0',							
						}),		
						this.autopay = new Ext.form.Checkbox({
							fieldLabel: 'Автопополнение',							
						}),							
						this.autoactivate = new Ext.form.Checkbox({
							fieldLabel: 'Включить абонента',							
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
                            this.submitaction()
                        },
                        scope: this                        
                    }]
				}			
			],
            listeners: {
            	afterrender : {
                    fn: function(obj) {
                    	obj.getEl().on('keypress', function(e,o) {
               				if(e.ctrlKey) {
								if(e.button==114) {
									// Ctrl+S
									(function(){this.submitaction();}).defer(500,this);
								}
							}            				               				
      					}, obj);			
                    },
                    scope: this
                },
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
            submitaction: function() {
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
							if ((parseFloat(this.sum.getValue() || 0) <= 0)&&(!this.allowzero.getValue())) {
								Ext.ux.msg('Ошибка ввода',"введите правильную сумму",Ext.Msg.ERROR)
								return false
							}
							AbonApi.make_fee({
								type: this.feetype,
								abonent: this.abonent,
								bankdate: this.bankdate.getValue(),
								sum: parseFloat(this.sum.getValue()),	
								descr: this.descr.getValue(),
								autopay: this.autopay.getValue(),
								autoactivate: this.autoactivate.getValue()								
							},this.fee_callback.createDelegate(this));
            },
			preload: function(response) {
				if(response.success) {						
					this.searchfield.setValue(response.data[0]['code'])					
					//this.personfield.setText(response.data[0]['person'])
					this.allowzero.setValue(false);
					this.personfield.setRawValue('')
					this.personfield.store.setBaseParam('code',response.data[0]['code'])
					this.personfield.store.load({
						callback: this.afterload.createDelegate(this),
					})					
				}
				this.searchfield.focus()
			},
			afterload: function(response) {
				this.personfield.setValue(parseInt(this.oid) || this.personfield.store.getAt(0).id)				
				this.abonent = parseInt(this.oid) || this.personfield.store.getAt(0).id
				this.oid=0
			},
			fee_callback: function(response) {
				this.searchfield.setRawValue('');
				this.personfield.setRawValue('');
				this.abonent = 0;
				this.allowzero.setValue(false);				
				if(this.my_owner_ct_id) {
					Ext.getCmp(this.my_owner_ct_id).refresh()
					(function(){
						this.hide()
						this.ownerCt.remove(this.id);	
					}).defer(300,this);
				}
			},
			register: 0,
			abonent: 0
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.FeeForm.superclass.initComponent.apply(this, arguments);
    }    
})

Ext.ux.DisableForm = Ext.extend(Ext.Panel ,{
	initComponent: function() {
        var config = {
            closable: true,
            title: 'Отключить',
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
						this.personfield = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonApi.abonent_get_by_code,
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
        							//pizdec
        							fields: [
            							'id',
            							'person',
            							'disabled',						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,        							
    							},
    						}),
							valueField: 'id',
            				displayField: 'person',
							forceSelection: true,
							emptyText: 'Абонент',
							editable: false,
    						triggerAction: 'all',    							
							listeners: {
								change: {
									fn: function(combo,newval,oldval) {
										var record_new = combo.store.getAt(combo.store.findExact('id',newval))
										var record_old = combo.store.getAt(combo.store.findExact('id',oldval))
										if(record_new.data.disabled) {
											alert("Внимание! Абонент отключен")
											combo.addClass('combo-bg-red')
										} else {
											combo.removeClass('combo-bg-red')
										}
										this.abonent = newval		
										this.oid=0								
									},
									scope: this
								}
							}
						}),														
					]
				},{
					xtype: 'form',
					width:  500,
					items: [
						this.date = new Ext.form.DateField({
							fieldLabel: 'Дата отключения',
							format: 'Y-m-d'
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
                            if(this.abonent<1) {
								Ext.ux.msg('Ошибка ввода',"выберите абонента",Ext.Msg.ERROR)
								return false
							}
							if (!this.date.getValue()) {
								Ext.ux.msg('Ошибка ввода',"введите правильную дату",Ext.Msg.ERROR)
								return false
							}
							AbonApi.disable({
								abonent: this.abonent,								
								date: this.date.getValue(),
								descr: this.descr.getValue()
							},this.abon_disable_callback.createDelegate(this));
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
					//this.personfield.setText(response.data[0]['person'])
					this.personfield.setRawValue('')
					this.personfield.store.setBaseParam('code',response.data[0]['code'])
					this.personfield.store.load({
						callback: this.afterload.createDelegate(this),
					})					
				}
				this.searchfield.focus()
			},
			afterload: function(response) {
				this.personfield.setValue(parseInt(this.oid) || this.personfield.store.getAt(0).id)				
				this.abonent = parseInt(this.oid) || this.personfield.store.getAt(0).id
				this.oid=0
			},
			abon_disable_callback: function(response) {
				this.searchfield.setRawValue('');
				this.personfield.setRawValue('');
				this.abonent = 0;					
				(function(){
					this.hide()
					this.ownerCt.remove(this.id);	
				}).defer(300,this);
				Ext.getCmp(this.my_owner_ct_id).refresh()												
			},
			register: 0,
			abonent: 0
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.DisableForm.superclass.initComponent.apply(this, arguments);
    }    
})

Ext.ux.EnableForm = Ext.extend(Ext.Panel ,{
	initComponent: function() {
        var config = {
            closable: true,
            title: 'Включить',
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
						this.personfield = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonApi.abonent_get_by_code,
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
        							//pizdec
        							fields: [
            							'id',
            							'person',
            							'disabled',						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,        							
    							},
    						}),
							valueField: 'id',
            				displayField: 'person',
							forceSelection: true,
							emptyText: 'Абонент',
							editable: false,
    						triggerAction: 'all',    							
							listeners: {
								change: {
									fn: function(combo,newval,oldval) {
										var record_new = combo.store.getAt(combo.store.findExact('id',newval))
										var record_old = combo.store.getAt(combo.store.findExact('id',oldval))
										if(record_new.data.disabled) {
											alert("Внимание! Абонент отключен")
											combo.addClass('combo-bg-red')
										} else {
											combo.removeClass('combo-bg-red')
										}
										this.abonent = newval		
										this.oid=0								
									},
									scope: this
								}
							}
						}),														
					]
				},{
					xtype: 'form',
					width:  500,
					items: [
						this.date = new Ext.form.DateField({
							fieldLabel: 'Дата включения',
							format: 'Y-m-d'
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
                            if(this.abonent<1) {
								Ext.ux.msg('Ошибка ввода',"выберите абонента",Ext.Msg.ERROR)
								return false
							}
							if (!this.date.getValue()) {
								Ext.ux.msg('Ошибка ввода',"введите правильную дату",Ext.Msg.ERROR)
								return false
							}
							AbonApi.enable({
								abonent: this.abonent,								
								date: this.date.getValue(),
								descr: this.descr.getValue()
							},this.abon_enable_callback.createDelegate(this));
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
					//this.personfield.setText(response.data[0]['person'])
					this.personfield.setRawValue('')
					this.personfield.store.setBaseParam('code',response.data[0]['code'])
					this.personfield.store.load({
						callback: this.afterload.createDelegate(this),
					})					
				}
				this.searchfield.focus()
			},
			afterload: function(response) {
				this.personfield.setValue(parseInt(this.oid) || this.personfield.store.getAt(0).id)				
				this.abonent = parseInt(this.oid) || this.personfield.store.getAt(0).id
				this.oid=0
			},
			abon_enable_callback: function(response) {
				this.searchfield.setRawValue('');
				this.personfield.setRawValue('');
				this.abonent = 0;
				(function(){
					this.hide()
					this.ownerCt.remove(this.id);	
				}).defer(300,this);
				Ext.getCmp(this.my_owner_ct_id).refresh();		
			},
			register: 0,
			abonent: 0
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.EnableForm.superclass.initComponent.apply(this, arguments);
    }    
})

Ext.ux.TransferForm = Ext.extend(Ext.Panel ,{
	initComponent: function() {
        var config = {
            closable: true,
            title: 'Трансфер',
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
            items: 
            [            
            	{
					xtype: 'panel',
					width:  500,
				    layout: 'table',
            		layoutConfig: {
                		columns: 2
            		},
					items: [
						new Ext.form.Label({
							text: 'от кого:',
							style: {
								'font-weight': 'bold'
							}
						}),
						this.transfer_from = new Ext.form.Label({
							text: '<...>',
							style: {
								'margin-left': '10px',
								'font-size': '18px'
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
						this.personfield = new Ext.form.ComboBox({
							store: new Ext.data.DirectStore({
    							api: {
        							read: AbonApi.abonent_get_by_code,
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
        							//pizdec
        							fields: [
            							'id',
            							'person',
            							'disabled',						
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,        							
    							},
    						}),
							valueField: 'id',
            				displayField: 'person',
							forceSelection: true,
							emptyText: 'Абонент',
							editable: false,
    						triggerAction: 'all',    							
							listeners: {
								change: {
									fn: function(combo,newval,oldval) {
										this.abonent_to = newval		
										this.oid=0								
									},
									scope: this
								}
							}
						}),														
					]
				},{
					xtype: 'form',
					width:  500,
					items: [
						this.date = new Ext.form.DateField({
							fieldLabel: 'Дата',
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
                            this.submitaction()
                        },
                        scope: this                        
                    }]
				}			
			],
            listeners: {
            	afterrender : {
                    fn: function(obj) {
                    	obj.getEl().on('keypress', function(e,o) {
               				if(e.ctrlKey) {
								if(e.button==114) {
									// Ctrl+S
									(function(){this.submitaction();}).defer(500,this);
								}
							}            				               				
      					}, obj);			
                    },
                    scope: this
                },
                activate: {
                    fn: function(obj) {
						if (parseInt(this.oid)>0) {
							this.abonent_from = this.oid
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
            submitaction: function() {
            				if(this.abonent_from<1) {
								Ext.ux.msg('Ошибка',"закройте форму и попробуйте еще раз",Ext.Msg.ERROR)
								return false
							}
                            if(this.abonent_to<1) {
								Ext.ux.msg('Ошибка ввода',"выберите абонента",Ext.Msg.ERROR)
								return false
							}
							if (!this.date.getValue()) {
								Ext.ux.msg('Ошибка ввода',"введите правильную дату",Ext.Msg.ERROR)
								return false
							}
							if(this.abonent_to==this.abonent_from) {
								Ext.ux.msg('Ошибка ввода',"нельзя передать сумму на тот же счёт",Ext.Msg.ERROR)
								return false
							}
							if (parseFloat(this.sum.getValue() || 0) <= 0) {
								Ext.ux.msg('Ошибка ввода',"введите правильную сумму",Ext.Msg.ERROR)
								return false
							}
							AbonApi.make_transfer({
								abonent_from: this.abonent_from,
								abonent_to: this.abonent_to,
								date: this.date.getValue(),
								sum: parseFloat(this.sum.getValue()),	
								descr: this.descr.getValue()
							},this.transfer_callback.createDelegate(this));
            },
			preload: function(response) {
				if(response.success) {
					if (this.oid) {		
						this.transfer_from.setText(response.data[0]['person']+' | '+response.data[0]['code'])				
					}
					this.searchfield.setValue(response.data[0]['code'])	
					this.personfield.setRawValue('')
					this.personfield.store.setBaseParam('code',response.data[0]['code'])
					this.personfield.store.load({
						callback: this.afterload.createDelegate(this),
					})					
				}
				this.searchfield.focus()
			},
			afterload: function(response) {
				this.personfield.setValue(parseInt(this.oid) || this.personfield.store.getAt(0).id)				
				this.abonent_to = parseInt(this.oid) || this.personfield.store.getAt(0).id
				this.oid=0
			},
			transfer_callback: function(response) {
				this.searchfield.setRawValue('');
				this.personfield.setRawValue('');
				this.abonent = 0;
				if(this.my_owner_ct_id) {
					Ext.getCmp(this.my_owner_ct_id).refresh()
					(function(){
						this.hide()
						this.ownerCt.remove(this.id);	
					}).defer(300,this);
				}
			},
			abonent_from: 0,
			abonent_to: 0
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.FeeForm.superclass.initComponent.apply(this, arguments);
    }    
})

Ext.ux.AbonTpMoveCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
        	//cs_id:0,
        	fieldLabel:'Перенести на',
            store: new Ext.data.DirectStore({
    		    api: {
    		        read: AbonApi.card_get_for_move,
    		        create: AbonApi.foo,
    		        update: AbonApi.foo,
    		        destroy: AbonApi.foo
    		    },
    		    restful: true,
    		    autoLoad: true,
    		    reader: new Ext.data.JsonReader({
    		        root: 'data',
    		        totalProperty: 'total',
    		        //idProperty: 'id',
    		        fields: [
    		            'id',
    		            'num',
    		        ]
    		    }),
    		    baseParams : {        
    		        service_id:0
    		    },
    		    listeners: {
                    load: {
                        fn: function(store,records,options){                            
                            for(i in records) {                            	
                            	if(records[i].data.num < 0) {
                            		records[i].data.num = 'CaTV'
                            	}
                            }
                        },
                        scope: this
                    }
                }
    		}),
            editable: false,            
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'num',
            mode: 'local'
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.SourceCombo.superclass.initComponent.apply(this, arguments);
        this.store.setBaseParam('service_id',this.cs_id)
    }
});

Ext.ux.AbonTpMoveForm = Ext.ux.AbonInfoPanel = Ext.extend(Ext.Window ,{
    initComponent: function() {
        var config = {
        	//cs_id: 0,
            closable: true,
            title: 'Перенос тарифа',
            layout: 'form',
            border: true,
            modal: true,
            width: 350,
            height: 80,
            items: [
            	this.card_combo = new Ext.ux.AbonTpMoveCombo({cs_id:this.cs_id})
            ],
            bbar: [
            	this.submit_button = new Ext.Button({
            		text: 'перенести',
            		handler: function() {
            			card_id = parseInt(this.card_combo.getValue())
            			if(!card_id) {
            				alert('выберите карту')
            			} else {
            				Engine.menu.cashier.abon_card_func.tp_move(this.cs_id,card_id)
            				this.close()
            			}
            		},
            		scope: this
            	}),
            	new Ext.Toolbar.Separator(),
            	this.cancel_button = new Ext.Button({
            		text: 'отменить',
            		handler: function() {
            			this.close()
            		},
            		scope: this
            	})
            
            ]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonTpMoveForm.superclass.initComponent.apply(this, arguments);        
    }
});
alert

