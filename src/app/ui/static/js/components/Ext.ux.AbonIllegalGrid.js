Ext.ux.AbonIllegalGrid = Ext.extend(Ext.ux.CustomGrid ,{
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
                        'date',
                        'comment',
                        'deleted'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.abon_illegal_get,
                    create: AbonApi.abon_illegal_add,
                    update: AbonApi.abon_illegal_update,
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
                {header: "Дата", dataIndex: 'date', xtype: 'datecolumn', editor: new Ext.form.DateField({format:'Y-m-d'}), format:'Y-m-d'},
                {header: "Погашено", dataIndex: 'deleted', xtype: 'checkcolumn', editable:true},
                {header: "Комментарий", dataIndex: 'comment', editor: new Ext.form.TextField(), width:300}
            ],
            viewConfig: {
                forceFit: true,
                getRowClass: function(record, index, rowParams, store) {
                    var c = record.get('deleted');
                    if (c) {
                        return '';
                    } else {
                        return 'maked_false_class';
                    }
                }
            },
            pageSize: 12,
            height: 380
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonIllegalGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Нелегалы',
    ds_model: Ext.data.Record.create([
			'id',
            'date',
            'comment',
            'deleted'
    ])
});

Ext.reg('ext:ux:abon-illegal-grid', Ext.ux.AbonIllegalGrid);


