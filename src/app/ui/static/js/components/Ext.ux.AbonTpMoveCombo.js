Ext.ux.AbonTpMoveCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
        	//cs_id:0,
        	fieldLabel:'Перенести на',
            store: new Ext.data.DirectStore({
    		    api: {
    		        read: AbonApi.card_get_for_move,
    		        create: AbonApi.foo,
    		        update: AbonApi.foo,
    		        destroy: AbonApi.foo
    		    },
    		    restful: true,
    		    autoLoad: true,
    		    reader: new Ext.data.JsonReader({
    		        root: 'data',
    		        totalProperty: 'total',
    		        //idProperty: 'id',
    		        fields: [
    		            'id',
    		            'num'
    		        ]
    		    }),
    		    baseParams : {        
    		        service_id:0
    		    },
    		    listeners: {
                    load: {
                        fn: function(store,records,options){                            
                            for(var i in records) {
                            	if(records[i].data.num < 0) {
                            		records[i].data.num = 'CaTV'
                            	}
                            }
                        },
                        scope: this
                    }
                }
    		}),
            editable: false,            
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'num',
            mode: 'local'
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.SourceCombo.superclass.initComponent.apply(this, arguments);
        this.store.setBaseParam('service_id',this.cs_id)
    }
});

