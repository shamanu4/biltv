Ext.ux.WarningGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'warning-store',
            ds_model: warning_ds_model,
            title: 'Предупреждения',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Код", dataIndex: 'code', editable:false},
                {header: "Дата", dataIndex: 'date', xtype: 'datecolumn', editable:false},
                {header: "Тип", dataIndex: 'level', editable:false}
            ]
});


