Ext.ux.IllegalGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'illegal-store',
            ds_model: illegal_ds_model,
            title: 'Нелегалы',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Код", dataIndex: 'code', editor: new Ext.form.TextField()},
                {header: "Дата", dataIndex: 'date', xtype: 'datecolumn', editor: new Ext.form.DateField({format:'Y-m-d'}), format:'Y-m-d'},
                {header: "Погашено", dataIndex: 'deleted', xtype: 'checkcolumn', editable:true},
                {header: "Комментарий", dataIndex: 'comment', editor: new Ext.form.TextField(), width:300}
            ]
});

