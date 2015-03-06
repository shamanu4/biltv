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
                                    this.children_forms.confirmed.obj=obj;
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
                                    this.children_forms.disabled.obj=obj;
                                    if((this.dis=="false")||(this.dis==false)) {
                                        obj.setText("Подключен");
										obj.addClass("bold_green")										
                                    } else {
                                    	obj.setText("Отключен");
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
                                        obj.setText("Отключить");
										obj.setIcon("/static/extjs/custom/delete_16.png")                                        
                                    } else {
										obj.setText("Подключить");
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
				this.children_forms_ready();
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
                    confirmed: this.children_forms.confirmed.obj.checked
					//disabled: this.children_forms.disabled.obj.checked,
					//activated: this.children_forms.address.obj.activated_field.value,
					//deactivated: this.children_forms.address.obj.deactivated_field.value                       
                },this.submitcallback.createDelegate(this));
            },
            submitcallback: function(result,e) {                
                if(result.success) {                    
                    //Ext.ux.abonent_store.load()
					this.setTitle("абон: "+(result.data[0]['code'] || '<новый>'));
					if (!this.oid) {
						this.hide();
						this.ownerCt.remove(this.id);
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
                    this.setTitle("абон: "+(result.data[0]['code'] || '<новый>'));
					this.hide();
					this.ownerCt.remove(this.id);
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
                	this.hide();
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
                        	this.children_forms.person.obj.onShow();
                        	this.children_forms.address.obj.onShow()
                    	} else {
                      		(function(){
                      			if(this.children_forms.person.obj && this.children_forms.address.obj) {
									this.children_forms.person.obj.onShow();
                        			this.children_forms.address.obj.onShow()
                        		}                    		
							}).defer(1000,this);
                    	}
                    },
                    scope: this
                }
            }
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonentForm.superclass.initComponent.apply(this, arguments);
    }    
});

