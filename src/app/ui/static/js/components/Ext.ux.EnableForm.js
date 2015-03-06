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
					xtype: 'form',
					width:  500,
					items: [
						this.date = new Ext.form.DateField({
							fieldLabel: 'Дата включения',
							format: 'Y-m-d'
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
                            if(this.abonent<1) {
								Ext.ux.msg('Ошибка ввода',"выберите абонента",Ext.Msg.ERROR);
								return false
							}
							if (!this.date.getValue()) {
								Ext.ux.msg('Ошибка ввода',"введите правильную дату",Ext.Msg.ERROR);
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
				this.personfield.setValue(parseInt(this.oid) || this.personfield.store.getAt(0).id);
				this.abonent = parseInt(this.oid) || this.personfield.store.getAt(0).id;
				this.oid=0
			},
			abon_enable_callback: function(response) {
				this.searchfield.setRawValue('');
				this.personfield.setRawValue('');
				this.abonent = 0;
				(function(){
					this.hide();
					this.ownerCt.remove(this.id);	
				}).defer(300,this);
				Ext.getCmp(this.my_owner_ct_id).refresh();		
			},
			register: 0,
			abonent: 0
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.EnableForm.superclass.initComponent.apply(this, arguments);
    }    
});

