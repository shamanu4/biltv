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
						'deactivated'
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
                }
            ],
            addAction: function(){
                Engine.menu.cashier.abonent.openForm()
            }
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonentGrid.superclass.initComponent.apply(this, arguments);
    },
    listeners: {
                afterrender : {
                    fn: function(obj) {
						this.topToolbar.addSpacer();
						this.topToolbar.addText("№ декодера");
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
						});
						this.topToolbar.add(this.optsearchfield);
						this.topToolbar.addButton({
                			icon: '/static/extjs/custom/search_16.png',
                			cls: 'x-btn-text-icon',
                			handler: function() {
                    			this.optSearchAction()
                			},
                			scope: this
            			});
            			this.topToolbar.addButton({
                			icon: '/static/extjs/custom/delete_16.png',
                			cls: 'x-btn-text-icon',
                			handler: function() {
                    			this.optsearchfield.setValue('');
                    			this.store.baseParams.filter_value = '';
                    			this.store.load()
                			},
                			scope: this
            			})            
                    }
                }
            },
    searchAction: function() {
            	this.store.baseParams.filter_value = this.searchfield.getValue();
                this.store.baseParams.filter_fields = ['person__firstname','person__lastname','person__passport','person__sorting',
        		'code','address__building__street__name','address__building__sorting','address__sorting'];
                this.store.load()
            },
	optSearchAction: function() {
				var v = this.optsearchfield.getValue();
            	this.store.baseParams.filter_value = parseInt(v-0)+'';
            	this.optsearchfield.setValue(this.store.baseParams.filter_value);
            	this.store.baseParams.filter_fields = ['cards__num__exact'];
            	if(this.store.baseParams.filter_value!='NaN') {
                	this.store.load()
                }
            }
});

