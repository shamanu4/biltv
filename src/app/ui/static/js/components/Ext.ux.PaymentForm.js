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
            							'code'
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,
        							filter_fields:['code'],
        							filter_value:''
    							}
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
        							fields: [
            							'id',
            							'person',
            							'disabled'
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8,
        							filter_disabled: 1     							
    							}
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
										var record_new = combo.store.getAt(combo.store.findExact('id',newval));
										//var record_old = combo.store.getAt(combo.store.findExact('id',oldval))
										this.addressfield.setText(record_new.json.address);
										if(record_new.data.disabled) {
											Ext.ux.msg('Внимание!',"абонент отключен", Ext.Msg.INFO);
											combo.addClass('combo-bg-red')
										} else {
											combo.removeClass('combo-bg-red')
										}
										this.abonent = newval;
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
										'end'
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:1000
    							}
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
						})
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
							fieldLabel: 'Описание'
						})
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
					this.searchfield.setValue(response.data[0]['code']);
					//this.personfield.setText(response.data[0]['person'])
					this.personfield.setRawValue('');
					this.personfield.store.setBaseParam('code',response.data[0]['code']);
					this.personfield.store.load({
						callback: this.afterload.createDelegate(this)
					})
				}
				this.searchfield.focus()
			},
			afterload: function(response) {
				if(this.personfield.store.data.length) {
					this.personfield.setValue(parseInt(this.oid) || this.personfield.store.getAt(0).id);
					this.abonent = parseInt(this.oid) || this.personfield.store.getAt(0).id;
					this.oid=0;
					this.personfield.fireEvent('change',this.personfield,this.abonent)
				} else {
					Ext.ux.msg('Сбой загрузки формы',"абонент не найден или отключен", Ext.Msg.ERROR);
				}
			},
			submitaction: function() {
							if(this.register<1) {
								Ext.ux.msg('Ошибка ввода',"выберите реестр оплат",Ext.Msg.ERROR);
								return false
							}
							if(this.abonent<1) {
								Ext.ux.msg('Ошибка ввода',"выберите абонента",Ext.Msg.ERROR);
								return false
							}
							if (!this.bankdate.getValue()) {
								Ext.ux.msg('Ошибка ввода',"введите правильную дату",Ext.Msg.ERROR);
								return false
							}
							if (parseFloat(this.sum.getValue() || 0) <= 0) {
								Ext.ux.msg('Ошибка ввода',"введите правильную сумму",Ext.Msg.ERROR);
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
					Ext.getCmp(this.my_owner_ct_id).refresh();
					(function(){
						this.hide();
						this.ownerCt.remove(this.id);	
					}).defer(300,this);
				}			
			},
			register: 0,
			abonent: 0
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.PaymentForm.superclass.initComponent.apply(this, arguments);
    }    
});

