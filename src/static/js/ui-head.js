function isInt(x) {
   var y=parseInt(x);
   if (isNaN(y)) return false;
   return x==y && x.toString()==y.toString();
}


alert = jAlert; 
//confirm = jConfirm;
//prompt= jPrompt;
alertsMask = new Ext.LoadMask(Ext.getBody(),{msg:null});		

Engine = {
    vp: null,
    components: {
        
    },
    getComponent: function(component,string,params) {
        if(string in Engine.components) {
            Ext.apply(Engine.components[string], params);            
			return Engine.components[string]
        } else {
            Engine.components[string] = new component(params)
			return Engine.components[string]
        }
    },
    getComponentFromPool: function(component,string,params,instances) {
        if(!instances) {
            instances=10;
        }
        if(!(string in Engine.components)) {
            Engine.components[string] = {
                index : 0,
                data : []
            }
        }
        Engine.components[string].index++;
        var index = Engine.components[string].index;
        Engine.components[string].data[index]=new component(params);
        if(Engine.components[string].index-instances>0) {
            Engine.components[string].data[index-instances].destroy();
            Engine.components[string].data[index-instances]=null;
        }
        return Engine.components[string].data[index];
    },
    auth: {
        doAuth: function() {
			Ext.get('loading').hide();
			Ext.get('loading-mask-half').hide();
            var lw = new Ext.ux.LoginWindow()
            lw.show()
            lw.caller = this
            lw.loginSuccess = (function(){
                lw.caller.checkAuth()
            })
        },
        doLogout: function() {
            MainApi.logout(function(response){
                if(response.success) {
                    Ext.ux.msg('Завершение работы', response.msg, Ext.Msg.INFO, function(){
                        location.reload()
                    });
                } else {
                    Ext.ux.msg('Завершение работы', 'ошибка при завершении работы', Ext.Msg.ERROR);
                }
            }, this)
        },
        checkAuth: function() {
            MainApi.is_authenticated(function(response){
                if(response.authenticated) {
                    //Ext.ux.msg('Приветствие', response.msg, Ext.Msg.INFO);
                    Ext.getCmp('menu-exit-button').setDisabled(false)
                    this.loadMenu()
                } else {
                    this.doAuth()
                }
            }, this)
        },
        loadMenu: function() {
			MainApi.menu(function(response){
                for (i in response.menuitems) {
                if(isInt(i)) {
                        Ext.getCmp('menu-bar').toolbars[0].add(Ext.ux.menu[response.menuitems[i]]);
                    }
                }
                Ext.getCmp('menu-bar').toolbars[0].doLayout()
				Ext.get('loading').hide();
				Ext.get('loading-mask-half').hide();
            }, this)
        }
    },
    user: {
		id: null,
        permissions: [

        ],
        hasPerm: function() {
            
        }
    },
    menu: {
        address: {
            city: {
                openGrid: function() {
                    var grid = Engine.getComponent(Ext.ux.CityGrid,'Ext.ux.CityGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                }
            },
            street: {
                openGrid: function() {
                    var grid = Engine.getComponent(Ext.ux.StreetGrid,'Ext.ux.StreetGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                }
            },
            house: {
                openGrid: function() {
                    var grid = Engine.getComponent(Ext.ux.HouseNumGrid,'Ext.ux.HouseNumGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                }
            },
            building: {
                openGrid: function() {
                    var grid = Engine.getComponent(Ext.ux.BuildingGrid,'Ext.ux.BuildingGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                }
            }
        },
        cashier: {
            abonent: {
                openGrid: function() {
                    var grid = Engine.getComponent(Ext.ux.AbonentGrid,'Ext.ux.AbonentGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                },
                openForm: function(id,code,confirmed,dis) {
                	var form = Engine.getComponentFromPool(Ext.ux.AbonentForm,'Ext.ux.AbonentForm',{'oid':id,'code':code,'confirmed':confirmed,'dis':dis})
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                }
            },
			register: {
				openGrid: function() {
                    var grid = Engine.getComponent(Ext.ux.RegisterGrid,'Ext.ux.RegisterGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                },
				openForm: function(id) {
                    var form = Engine.getComponentFromPool(Ext.ux.RegisterForm,'Ext.ux.RegisterForm',{'oid':id,})
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                },
				deletePayment: function(id,obj) {
					this.obj=obj					
					if(confirm('Удалить платёж?')) {
						AbonApi.reg_payments_delete({
                            payment_id: (id || 0)
                        },this.deletePaymentCallback.createDelegate(this));
					}
				},
				deletePaymentCallback: function(response) {
					if (response.success) {
						$(this.obj).parent().parent().parent().hide('slow')						
					}
				},
				transferPayment: function(id,obj) {
					this.obj=obj
					alert('not implemented yet...')
					return false					
					if(confirm('Перенести платёж?')) {
						
					}
				},
				transferPaymentCallback: function(response) {
					if (response.success) {
						$(this.obj).parent().parent().parent().hide('slow')						
					}
				},
				partiallyConfirm: function(id,source) {
					if(confirm('Засчитать платежи реестра '+source+'?')) {
						AbonApi.reg_payments_partially_confirm({
                            register_id: (id || 0)
                        },this.partiallyConfirmCallback.createDelegate(this));
						Ext.get('loading').show();
            			Ext.get('loading-mask-half').show();						
					}
				},
				partiallyConfirmCallback: function(response){
					Ext.get('loading').hide();
            		Ext.get('loading-mask-half').fadeOut('fast');
				}				
			},
			payment: {
				openForm: function(oid,my_owner_ct_id) {
					if (typeof my_owner_ct_id == 'object') {
						my_owner_ct_id = 0
					}
					if ((typeof oid == 'object') && ('oid' in oid)) {
						oid = oid['oid']
					}
					var form = Engine.getComponent(Ext.ux.PaymentForm,'Ext.ux.PaymentForm',{'oid':oid,'my_owner_ct_id':my_owner_ct_id})
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
				},
				rollback: function(id,obj) {
					this.obj=obj	
					if(confirm('Откатить платёж?')) {
						AbonApi.payment_rollback({
                            payment_id: (id || 0)
                        },this.rollbackPaymentCallback.createDelegate(this));	
					}
				},
				rollbackPaymentCallback: function(response) {
					if (response.success) {
						$(this.obj).parent().parent().parent().hide('slow')						
					}
				},
			},
			fee: {
				openForm: function(oid,my_owner_ct_id) {
					if (typeof my_owner_ct_id == 'object') {
						my_owner_ct_id = 0
					}
					if ((typeof oid == 'object') && ('oid' in oid)) {
						oid = oid['oid']
					}
					var form = Engine.getComponent(Ext.ux.FeeForm,'Ext.ux.FeeForm',{'oid':oid,'my_owner_ct_id':my_owner_ct_id})
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
				},
				rollback: function(id,obj) {					
					this.obj=obj
					if(confirm('Откатить снятие?')) {
						AbonApi.fee_rollback({
                            fee_id: (id || 0)
                        },this.rollbackFeeCallback.createDelegate(this));	
					}
				},
				rollbackFeeCallback: function(response) {
					if (response.success) {
						$(this.obj).parent().parent().parent().hide('slow')						
					}
				},			
			},
			transfer: {
				openForm: function(oid,my_owner_ct_id) {
					if (typeof my_owner_ct_id == 'object') {
						my_owner_ct_id = 0
					}
					if ((typeof oid == 'object') && ('oid' in oid)) {
						oid = oid['oid']
					}
					var form = Engine.getComponent(Ext.ux.TransferForm,'Ext.ux.TransferForm',{'oid':oid,'my_owner_ct_id':my_owner_ct_id})
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
				}
			},
			history_delete: function(id,obj) {
				this.obj=obj
				if(confirm('Удалить историю?')) {
					AbonApi.history_delete({
                 	   history_id: (id || 0)
                    },this.history_delete_callback.createDelegate(this));	
				}
			},
			history_delete_callback: function(response) {
				if (response.success) {
					$(this.obj).parent().parent().parent().hide('slow')						
				}
			},			
			abon_disable: { 
				openForm: function(oid,my_owner_ct_id) {
					if (typeof my_owner_ct_id == 'object') {
						my_owner_ct_id = 0
					}
					if ((typeof oid == 'object') && ('oid' in oid)) {
						oid = oid['oid']
					}
					var form = Engine.getComponent(Ext.ux.DisableForm,'Ext.ux.DisableForm',{'oid':oid,'my_owner_ct_id':my_owner_ct_id})
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
				}
			},
			abon_enable: { 
				openForm: function(oid,my_owner_ct_id) {
					if (typeof my_owner_ct_id == 'object') {
						my_owner_ct_id = 0
					}
					if ((typeof oid == 'object') && ('oid' in oid)) {
						oid = oid['oid']
					}
					var form = Engine.getComponent(Ext.ux.EnableForm,'Ext.ux.EnableForm',{'oid':oid,'my_owner_ct_id':my_owner_ct_id})
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].add(form);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
				}
			},
			abon_card_func: {
				store: null,
				card_activate: function(card_id) {
					if(confirm("активировать карточку?")) {
						AbonApi.card_activate({
							card_id:card_id
						})									
					}
				},
				card_deactivate: function(card_id) {
					if(confirm("отключить карточку?")) {
						AbonApi.card_deactivate({
							card_id:card_id
						})															
					}
				},
				card_unbind: function(card_id) {
					if(confirm("удалить карточку?")) {
						AbonApi.card_unbind({
							card_id:card_id
						})				
					}
				},
				tp_activate: function(card_service_id) {
					if(confirm("активировать тариф?")) {
						AbonApi.cards_tp_activate({
							cs_id:card_service_id
						})					
					}
				},
				tp_deactivate: function(card_service_id) {
					if(confirm("отключить тариф?")) {
						AbonApi.cards_tp_deactivate({
							cs_id:card_service_id
						})					
					}
				},
				tp_move_form: function(card_service_id) {
					//alert(card_service_id)
					w = new Ext.ux.AbonTpMoveForm({
						cs_id:card_service_id,
					})
					w.show();
				},
				
				tp_move: function(card_service_id,card_id) {
					AbonApi.cards_tp_move({
						//18779
						service_id:card_service_id,
						card_id:card_id,
					})
				},

				tp_unbind: function(card_service_id) {
					if(confirm("удалить тариф?")) {
						AbonApi.cards_tp_delete({
							cs_id:card_service_id
						})
					}
				},
			},
            sched: {
                sched_delete: function(sched_id) {
                    if(confirm("удалить планировщик?")) {
                        AbonApi.abon_sched_delete({
                            sched_id:sched_id
                        })
                    }
                }
            },
			report: {
				launch: function() {
					window.open('/report','_newtab');
				}
			}
        },
        scrambler: {
            card: {
                openGrid: function() {
                    var grid = Engine.getComponent(Ext.ux.CardGrid,'Ext.ux.CardGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout();
                },
                send_all: function() {
                    if(confirm("Переслать все карточки?")) {
                        AbonApi.card_send_all({
                            action:'confirm',
                        });
                    }
                }
            }
        }
    }
}
