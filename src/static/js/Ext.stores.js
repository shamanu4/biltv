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
