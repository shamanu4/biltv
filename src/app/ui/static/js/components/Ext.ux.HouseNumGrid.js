Ext.ux.HouseNumGrid = Ext.extend(Ext.ux.CustomGrid ,{
            store: 'house-num-store',
            ds_model: house_num_ds_model,
            title: 'Номера домов',
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Num", dataIndex: 'num', editor: new Ext.form.TextField()},
                {header: "Code", dataIndex: 'code', editor: new Ext.form.TextField()},
                {header: "Comment", dataIndex: 'comment', editor: new Ext.form.TextField()}
            ]
});

