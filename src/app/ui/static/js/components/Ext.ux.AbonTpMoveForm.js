Ext.ux.AbonTpMoveForm = Ext.ux.AbonInfoPanel = Ext.extend(Ext.Window ,{
    initComponent: function() {
        var config = {
        	//cs_id: 0,
            closable: true,
            title: 'Перенос тарифа',
            layout: 'form',
            border: true,
            modal: true,
            width: 350,
            height: 80,
            items: [
            	this.card_combo = new Ext.ux.AbonTpMoveCombo({cs_id:this.cs_id})
            ],
            bbar: [
            	this.submit_button = new Ext.Button({
            		text: 'перенести',
            		handler: function() {
            			var card_id = parseInt(this.card_combo.getValue());
            			if(!card_id) {
            				alert('выберите карту')
            			} else {
            				Engine.menu.cashier.abon_card_func.tp_move(this.cs_id,card_id);
            				this.close()
            			}
            		},
            		scope: this
            	}),
            	new Ext.Toolbar.Separator(),
            	this.cancel_button = new Ext.Button({
            		text: 'отменить',
            		handler: function() {
            			this.close()
            		},
            		scope: this
            	})
            
            ]
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonTpMoveForm.superclass.initComponent.apply(this, arguments);        
    }
});


