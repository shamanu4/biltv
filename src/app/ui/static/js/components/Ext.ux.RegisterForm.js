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
												'end'
											]
    									}),
    									baseParams : {
        									start:0,
        									limit:1000
    									}
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
												this.register = record.data.id;
												this.setTitle('Реестр #'+record.data.id);
												this.startdate.setValue(record.data.start);
												this.enddate.setValue(record.data.end);
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
												this.registercombo.reset();
												this.register = null;
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
											'username'
										]
    								}),
    								baseParams : {
        								start:0,
        								limit:100
    								}
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
											this.admin = record.data.id;
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
											this.admincombo.reset();
											this.admin = null;
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
									format: 'Y-m-d'
								}),
								this.enddate = new Ext.form.DateField({
									width: 100,
									value: new Date(),
									format: 'Y-m-d'
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
							readOnly: true
						}),
						this.sumfield = new Ext.form.TextField({
							fieldLabel: 'Сумма',
							readOnly: true
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
						})
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
                        		'inner_descr'
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
							end_date:null
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
                		}
    				]
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
								var index = this.registercombo.store.indexOfId(parseInt(this.oid));
								if (index>=0) {
									this.setTitle('Реестр #'+response[index].data.id);
									this.registercombo.setValue(response[index].data.unicode);
									this.register = this.oid;
									this.preload()
								}								
							},
							scope: this
						});
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
				this.resultsgrid.store.setBaseParam('register_id',this.register);
				this.resultsgrid.store.setBaseParam('admin_id',this.admin);
				this.resultsgrid.store.setBaseParam('start_date',this.startdate.getValue());
				this.resultsgrid.store.setBaseParam('end_date',this.enddate.getValue());
				this.resultsgrid.store.load({
					callback: function(response) {
						Ext.get('loading').hide();
            			Ext.get('loading-mask-half').fadeOut('fast');
						var extras = this.resultsgrid.store.reader.jsonData.extras;
						this.countfield.setValue(extras.count);
						this.sumfield.setValue(extras.sum)						
					},
					scope: this
				})
			}
		};
		Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.RegisterForm.superclass.initComponent.apply(this, arguments);
	} 
});

/*
 *  Forms and panels
 */

