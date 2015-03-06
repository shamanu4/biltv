Ext.ux.RegisterGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'register-store',
            title: 'Реестры',
            ds_model: register_ds_model,
            columns: [
                {header: "Id", dataIndex: 'id', width:70, editable:false},
                {header: "Source", dataIndex: 'source', width:165, editable:false, editor: new Ext.ux.SourceCombo(),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						this.editable = true;
						return value;
					}
                },
                {header: "Total", dataIndex: 'total', width:100, editable:false, editor: new Ext.form.TextField(),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						this.editable = true;
						return value;
					} 
				},
                {header: "Start", dataIndex: 'start', width:100, editable:false, editor: new Ext.form.DateField({format:'Y-m-d'}),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						this.editable = true;
						return value;
					},
                	listeners: {
                    	change : {
                        	fn: function(obj) {
                            	var tfoo=1;
								debugger;
                        	},
                        	scope: this
                    	}
                	}
				},
				{header: "End", dataIndex: 'end', width:100, editable:false, editor: new Ext.form.DateField({format:'Y-m-d'}),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						this.editable = true;
						return value;
					}
				},
				{header: "Bank", dataIndex: 'bank', width:100, editable:false, editor: new Ext.form.DateField({format:'Y-m-d'}),
					renderer: function(value, metaData, record, rowIndex, colIndex, store){
						this.editable = true;
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
                }
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



