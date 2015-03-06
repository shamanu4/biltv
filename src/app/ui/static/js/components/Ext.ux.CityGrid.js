Ext.ux.CityGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'cities-store',
            ds_model: cities_ds_model,
            title: 'Города',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Name", dataIndex: 'name', editor: new Ext.form.TextField()},
                {header: "Label", dataIndex: 'label', editor: new Ext.form.TextField()},
                {header: "Comment", dataIndex: 'comment', editor: new Ext.form.TextField()}
            ]
});

Ext.reg('ext:ux:city-grid', Ext.ux.CityGrid);

