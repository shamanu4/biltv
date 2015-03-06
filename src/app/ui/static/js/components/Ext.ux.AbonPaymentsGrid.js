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
                    filter_fields:['sum'],
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
            }
        };
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

