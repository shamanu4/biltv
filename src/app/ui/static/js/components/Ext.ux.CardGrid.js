Ext.ux.CardGrid = Ext.extend(Ext.ux.CustomGrid, {
    store: 'card-store',
    title: 'Карточки',
    ds_model: card_ds_model,
    columns: [
        {header: "Id", dataIndex: "id", width: 100},
        {header: "Num", dataIndex: 'num', width: 100, editor: new Ext.form.TextField()},
        {header: "Owner", dataIndex: 'owner', width: 300},
        {header: "Active", dataIndex: 'active', width: 100, xtype: 'booleancolumn', default: true},
        {header: "Activated", dataIndex: 'activated', width: 150}
    ]
});

