Ext.ux.AbonWarningGrid = Ext.extend(Ext.ux.CustomGrid ,{
    initComponent: function(){
        var config = {
            store: new Ext.data.DirectStore({
                restful: true,
                autoLoad: false,
                autoSave: false,
                reader: new Ext.data.JsonReader({
                    root: 'data',
                    totalProperty: 'total',
                    fields: [
                        'id',
                        'code',
                        'date',
                        'level'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.abon_warning_get,
                    create: AbonApi.abon_warning_add,
                    update: AbonApi.foo,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:10,
                    uid:this.oid
                }
            }),
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Код", dataIndex: 'code', editable:false},
                {header: "Дата", dataIndex: 'date', xtype: 'datecolumn', editable:false},
                {header: "Тип", dataIndex: 'level', editable:false}
            ],
            pageSize: 12,
            height: 380
            };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonWarningGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Предупреждения',
    ds_model: Ext.data.Record.create([
			'id',
			'code',
            'date',
            'level'
    ])
});

Ext.reg('ext:ux:abon-warning-grid', Ext.ux.AbonWarningGrid);


