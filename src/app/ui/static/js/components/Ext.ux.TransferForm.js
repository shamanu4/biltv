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
						})
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
            							'disabled'
									]
    							}),
    							baseParams : {
        							start:0,
        							limit:8
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
										this.abonent_to = newval;
										this.oid=0								
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
						this.date = new Ext.form.DateField({
							fieldLabel: 'Дата',
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
                    	obj.getEl().on('keypress', function(e) {
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
							this.abonent_from = this.oid;
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
								Ext.ux.msg('Ошибка',"закройте форму и попробуйте еще раз",Ext.Msg.ERROR);
								return false
							}
                            if(this.abonent_to<1) {
								Ext.ux.msg('Ошибка ввода',"выберите абонента",Ext.Msg.ERROR);
								return false
							}
							if (!this.date.getValue()) {
								Ext.ux.msg('Ошибка ввода',"введите правильную дату",Ext.Msg.ERROR);
								return false
							}
							if(this.abonent_to==this.abonent_from) {
								Ext.ux.msg('Ошибка ввода',"нельзя передать сумму на тот же счёт",Ext.Msg.ERROR);
								return false
							}
							if (parseFloat(this.sum.getValue() || 0) <= 0) {
								Ext.ux.msg('Ошибка ввода',"введите правильную сумму",Ext.Msg.ERROR);
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
					this.searchfield.setValue(response.data[0]['code']);
					this.personfield.setRawValue('');
					this.personfield.store.setBaseParam('code',response.data[0]['code']);
					this.personfield.store.load({
						callback: this.afterload.createDelegate(this)
                    })
				}
				this.searchfield.focus()
			},
			afterload: function(response) {
				this.personfield.setValue(parseInt(this.oid) || this.personfield.store.getAt(0).id);
				this.abonent_to = parseInt(this.oid) || this.personfield.store.getAt(0).id;
				this.oid=0
			},
			transfer_callback: function(response) {
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
			abonent_from: 0,
			abonent_to: 0
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.FeeForm.superclass.initComponent.apply(this, arguments);
    }    
});

