Ext.ux.cities_store = new Ext.data.DirectStore({
    api: {
        read: CityGrid.read,
        create: CityGrid.create,
        update: CityGrid.update,
        destroy: CityGrid.destroy
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'cities-store',    
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
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
        limit:16,
        filter_fields:['name'],
        filter_value:''
    },
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
});

Ext.ux.cities_combo_store = new Ext.data.DirectStore({
    api: {
        read: CityGrid.read,
        create: CityGrid.create,
        update: CityGrid.update,
        destroy: CityGrid.destroy
    },
    restful: true,
    autoLoad: true,
    storeId: 'cities-combo-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'name',
            'label',
            'comment',
        ]
    }),
    baseParams : {
        filter_fields:['name'],
        filter_value:'',
        filter:''
    }
});

Ext.ux.sources_combo_store = new Ext.data.DirectStore({
    api: {
        read: SourceGrid.read,
        create: SourceGrid.foo,
        update: SourceGrid.foo,
        destroy: SourceGrid.foo
    },
    restful: true,
    autoLoad: true,
    storeId: 'sources-combo-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'name',
        ]
    }),
    baseParams : {
        filter_fields:['name'],
        filter_value:'',
        filter:''
    }
});

var cities_ds_model = Ext.data.Record.create([
    'id',
    'name',
    'label',
    'comment',
]);

Ext.ux.streets_store = new Ext.data.DirectStore({
    api: {
        read: StreetGrid.read,
        create: StreetGrid.create,
        update: StreetGrid.update,
        destroy: StreetGrid.destroy
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'streets-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'city',
            'name',
            'code',
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
        limit:16,
        filter_fields:['name','code'],
        filter_value:''
    },
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
});

Ext.ux.streets_combo_store = new Ext.data.DirectStore({
    api: {
        read: StreetGrid.read,
        create: StreetGrid.create,
        update: StreetGrid.update,
        destroy: StreetGrid.destroy
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'streets-combo-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'city',
            'name',
            'code',
            'comment',
        ]
    }),
    baseParams : {
        filter_fields:['name','code'],
        filter_value:''
    }    
});

var streets_ds_model = Ext.data.Record.create([
    'id',
    'city',
    'name',
    'code',
    'comment',
]);

Ext.ux.house_num_store = new Ext.data.DirectStore({
    api: {
        read: HouseNumGrid.read,
        create: HouseNumGrid.create,
        update: HouseNumGrid.update,
        destroy: HouseNumGrid.destroy
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'house-num-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'num',
            'code',
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
        limit:16,
        filter_fields:['num'],
        filter_value:''
    },
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
});

Ext.ux.houses_combo_store = new Ext.data.DirectStore({
    api: {
        read: HouseNumGrid.read,
        create: HouseNumGrid.create,
        update: HouseNumGrid.update,
        destroy: HouseNumGrid.destroy
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'houses-combo-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'num',
            'code',
            'comment',
        ]
    }),
    baseParams : {
        filter_fields:['num'],
        filter_value:'',
        filter:''
    }    
});

var house_num_ds_model = Ext.data.Record.create([
    'id',
    'num',
    'code',
    'comment',
]);

Ext.ux.building_store = new Ext.data.DirectStore({
    api: {
        read: BuildingGrid.read,
        create: BuildingGrid.create,
        update: BuildingGrid.update,
        destroy: BuildingGrid.destroy
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'building-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'street',
            'house',
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
        limit:16,
        filter_fields:['street__name','house__num'],
        filter_value:''
    },
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
});

var building_ds_model = Ext.data.Record.create([
    'id',
    'street',
    'house',
    'comment',
]);

Ext.ux.abonent_store = new Ext.data.DirectStore({
    api: {
        read: AbonentGrid.read,
        create: AbonentGrid.create,
        update: AbonentGrid.update,
        destroy: AbonentGrid.destroy
    },
    remoteSort: true,
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'abonent-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'code',
            'person',
            'person__passport',
            'address',
            'bill__balance',
            'comment',
            'confirmed',
			'disabled',
			'deactivated',
        ]
    }),
    writer: new Ext.data.JsonWriter({
        encode: false,
        writeAllFields: true,
        listful: true
    }),
    baseParams : {
        start:0,
        limit:16,
        filter_fields:['person__firstname','person__lastname','person__passport','person__sorting',
        	'code','address__building__street__name','address__building__sorting','address__sorting'],
        filter_value:''
    },
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
});

Ext.ux.card_store = new Ext.data.DirectStore({
    api: {
        read: CardGrid.read,
        create: CardGrid.create,
        update: CardGrid.update,
        destroy: CardGrid.destroy
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'card-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'num',
            'owner',
            'active',
            'activated',            
        ]
    }),
    writer: new Ext.data.JsonWriter({
        encode: false,
        writeAllFields: true,
        listful: true
    }),
    baseParams : {
        start:0,
        limit:16,
        filter_fields:['num'],
        filter_value:''
    },
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
});

var card_ds_model = Ext.data.Record.create([
    'id',
    'num',
    'owner',
    'active',
    'activated'
]);

Ext.ux.free_card_combo_store = new Ext.data.DirectStore({
                restful: true,
                autoLoad: true,
                autoSave: false,
                storeId: 'free_card_combo_store',
                reader: new Ext.data.JsonReader({
                    root: 'data',
                    totalProperty: 'total',
                    fields: [
                        'id',
                        'num',
                        'active',
                        'activated',
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.free_cards_get,
                    create: CardGrid.create,
                    update: CardGrid.update,
                    destroy: CardGrid.destroy
                },
                baseParams : {
                    uid:this.oid,
                    filter_fields:['num'],
                    filter_value:''
                }
            })

Ext.ux.card_tp_combo_store = new Ext.data.DirectStore({
                restful: true,
                autoLoad: true,
                autoSave: false,
                storeId: 'card_tp_combo_store',
                reader: new Ext.data.JsonReader({
                    root: 'data',
                    totalProperty: 'total',
                    fields: [
                        'id',
                        'name',
                    ]
                }),
                writer: new Ext.data.JsonWriter({
                    encode: false,
                    writeAllFields: true,
                    listful: true
                }),
                api: {
                    read: AbonApi.cards_tp_list_get,
                    create: CardGrid.create,
                    update: CardGrid.update,
                    destroy: CardGrid.destroy
                },
                baseParams : {
                    uid:this.oid,
                    filter_fields:['name'],
                    filter_value:''
                }
            })
			

Ext.ux.register_store = new Ext.data.DirectStore({
    api: {
        read: RegisterGrid.read,
        create: RegisterGrid.create,
        update: RegisterGrid.update,
        destroy: RegisterGrid.destroy
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'register-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
			'source',
            'total',
            'current',
            'closed',
            'start',
			'end',
			'bank',
			'payments_total',
			'payments_maked'
        ]
    }),
    writer: new Ext.data.JsonWriter({
        encode: false,
        writeAllFields: true,
        listful: true
    }),
    baseParams : {
        start:0,
        limit:16,
        filter_fields:['num'],
        filter_value:''
    },
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
});

var register_ds_model = Ext.data.Record.create([
			'id',
			'source',
            'total',
            'current',
            'closed',
            'start',
			'end',
			'bank'
]);