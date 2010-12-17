/* 

 new Ext.data.DirectStore({
    api: {
        read: GameApi.cards_on_hand
    },
    storeId: 'cards-on-hand-store',
    paramsAsHash: false,
    reader: new Ext.data.JsonReader({
        root: 'data',
        fields: [
            'id',
            'name',
            'card_id',
            'image',
            'turned',
            'type'
        ]
    })
});

 */

new Ext.data.DirectStore({
    api: {
        read: TvApi.channels
    },
    storeId: 'channels-store',
    paramsAsHash: false,
    reader: new Ext.data.JsonReader({
        root: 'data',
        fields: [
            'id',
            'name',
            'bound',
            'comment',
        ]
    })
});

Ext.ux.cities_store = new Ext.data.DirectStore({
    api: {
        read: CityGrid.read,
        create: CityGrid.create,
        update: CityGrid.update,
        destroy: CityGrid.destroy
    },
    autoSave: false,
    storeId: 'cities-store',    
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        fields: [
            'id',
            'name',
            'label',
            'comment',
        ]
    }),
    writer: new Ext.data.JsonWriter({        
        encode: false,
        writeAllFields: true,
        listful: true
    }),
    baseParams : {
        start:0,
        limit:10
    },
    listeners:{
        write: function (store,action,result,res,rs){
            console.log('store write action')
            console.log(res.result)
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
});

var cities_ds_model = Ext.data.Record.create([
    'id',
    'name',
    'label',
    'comment',
]);
