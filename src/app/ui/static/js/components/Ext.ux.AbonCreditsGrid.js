Ext.ux.AbonCreditsGrid = Ext.extend(Ext.ux.CustomGrid ,{
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
                        'bill',
                        'sum',
                        'valid_from',
                        'valid_until',
                        'valid',
                        'manager'
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.abon_credit_get,
                    create: AbonApi.abon_credit_add,
                    update: AbonApi.abon_credit_update,
                    destroy: AbonApi.foo
                },
                baseParams : {
                    start:0,
                    limit:10,
                    uid:this.oid
                }
            }),
            columns: [
                {header: "Id", dataIndex: 'id', width:40},
                {header: "Bill", dataIndex: 'bill', width:65},
                {header: "Sum", dataIndex: 'sum', width:65, editor: new Ext.form.TextField()},
                {header: "Valid from", dataIndex: 'valid_from', width:120
                    //editor: new Ext.form.DateField({format:"Y-m-d"})
                },
                {header: "Valid until", dataIndex: 'valid_until', width:120,
                    editor: new Ext.form.DateField({format:"Y-m-d"})
                },
                {header: "manager", dataIndex: 'manager', width:80}
            ],
            viewConfig: {
                forceFit: true,
                getRowClass: function(record, index, rowParams, store) {
                    var c = record.get('valid');
                    if (c) {
                        return 'maked_true_class';
                    } else {
                        return '';
                    }
                }
            },
            pageSize: 12,
            height: 380
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCreditsGrid.superclass.initComponent.apply(this, [config]);
    },
    title: 'Кредиты',
    ds_model: credit_ds_model
});

Ext.reg('ext:ux:abon-credits-grid', Ext.ux.AbonCreditsGrid);


