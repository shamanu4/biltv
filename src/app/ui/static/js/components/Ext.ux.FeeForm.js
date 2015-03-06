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
										var record_new = combo.store.getAt(combo.store.findExact('id',newval));
										var record_old = combo.store.getAt(combo.store.findExact('id',oldval));
										if(record_new.data.disabled) {
											alert("Внимание! Абонент отключен");
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
        							limit:100
    							}
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
										this.sum.setValue(record.data.sum);
										this.feetype = record.data.id
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
							fieldLabel: 'Дата снятия',
							format: 'Y-m-d'
						}),
						this.sum = new Ext.form.NumberField({
							fieldLabel: 'Сумма',
							baseChars: '1234567890.'
						}),
						this.descr = new Ext.form.TextField({
							fieldLabel: 'Описание'
						}),
						this.allowzero = new Ext.form.Checkbox({
							fieldLabel: 'Разрешить 0'
						}),		
						this.autopay = new Ext.form.Checkbox({
							fieldLabel: 'Автопополнение'
						}),							
						this.autoactivate = new Ext.form.Checkbox({
							fieldLabel: 'Включить абонента'
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
            submitaction: function() {
            				if(this.feetype<1) {
								Ext.ux.msg('Ошибка ввода',"выберите тип снятия",Ext.Msg.ERROR);
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
							if ((parseFloat(this.sum.getValue() || 0) <= 0)&&(!this.allowzero.getValue())) {
								Ext.ux.msg('Ошибка ввода',"введите правильную сумму",Ext.Msg.ERROR);
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
					this.searchfield.setValue(response.data[0]['code']);
					//this.personfield.setText(response.data[0]['person'])
					this.allowzero.setValue(false);
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
				this.abonent = parseInt(this.oid) || this.personfield.store.getAt(0).id;
				this.oid=0
			},
			fee_callback: function(response) {
                var $this = this;
				$this.searchfield.setRawValue('');
				$this.personfield.setRawValue('');
				$this.abonent = 0;
				$this.allowzero.setValue(false);
				if($this.my_owner_ct_id) {
					Ext.getCmp($this.my_owner_ct_id).refresh();
					(function(){
						this.hide();
						this.ownerCt.remove($this.id);
					}).defer(300, $this);
				}
			},
			register: 0,
			abonent: 0
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.FeeForm.superclass.initComponent.apply(this, arguments);
    }    
});

