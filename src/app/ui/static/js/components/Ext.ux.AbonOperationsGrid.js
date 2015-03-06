Ext.ux.AbonOperationsGrid = Ext.extend(Ext.ux.CustomGridNE ,{
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
                        'abssum',
                        'prev',
                        'maked',
                        'descr',
                        'inner_descr',
                        'rolled_by'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.operations_get,
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
                        //obj.parent_form.children_forms.cards.obj=obj
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
        {header: "Timestamp", dataIndex: 'timestamp', width:180, sortable: true},
        {header: "Sum", dataIndex: 'abssum', width:50, sortable: true},
        {header: "Prev", dataIndex: 'prev', width:50},
        {header: "Descr", dataIndex: 'inner_descr', width:200},
        {header: "", dataIndex: 'id', width:26,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                return '<div class="inline_rollback_button abonent_rollback_fee" id="roll_fee_"'+value+'" val="'+value+'"></div>'
            }
        }
    ],
	viewConfig: {
        forceFit: true,
		getRowClass: function(record, index, rowParams, store) {
            var c = record.get('rolled_by');
            if (c>0) {
                return ''
            }
            var c = record.get('abssum');
            if (c>0) {
				return 'maked_true_class';
			} else {
				return 'maked_false_class';
			}
        }
    },
    pageSize: 12,
    height: 380
});

Ext.reg('ext:ux:abon-operations-grid', Ext.ux.AbonOperationsGrid);


