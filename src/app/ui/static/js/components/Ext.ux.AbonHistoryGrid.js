Ext.ux.AbonHistoryGrid = Ext.extend(Ext.ux.CustomGridNE ,{
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
                        'timestamp',
                        'date',
                        'text',
                        'descr',
                        'cnt'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.abon_history_get,
                    create: AbonApi.foo,
                    update: AbonApi.foo,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:12,
                    foo:'bar',
                    uid:this.oid || 0
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
        Ext.ux.AbonHistoryGrid.superclass.initComponent.apply(this, [config]);
    },    
    columns: [
        {header: "Id", dataIndex: 'id', width:45},
        {header: "Timestamp", dataIndex: 'timestamp', width:180, sortable: true},
        {header: "Дата", dataIndex: 'date', width:150, sortable: true},
        {header: "Text", dataIndex: 'text', width:180},
        {header: "Descr", dataIndex: 'descr', width:300},
        {header: " ", dataIndex: 'cnt', width:26,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {            	
            	if((value>1)&&(!(value % 2))) {
                	return '<div class="inline_delete_button card_history_deldete" id="del_ch_'+record.data.id+'" val="'+record.data.id+'"></div>'
            	} 
            }
        }
    ]
});

Ext.reg('ext:ux:abon-history-grid', Ext.ux.AbonHistoryGrid);

