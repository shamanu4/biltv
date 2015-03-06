Ext.ux.AbonCommentsPanel = Ext.extend(Ext.Panel ,{
	    initComponent: function() {
        var config = {
            closable: false,
			frame: true,
            defaults: {
                frame: true,
                split: true    
            },            
            items: [
			this.comment_field = new Ext.form.TextArea({
				xtype: 'textarea',
				width: 900
			}),
			{
            	xtype: 'tbbutton',
            	cls: 'x-btn-text-icon',
            	icon: '/static/extjs/custom/tick_16.png',
            	text: 'Сохранить',
				listeners: {
                	click : {
                    	fn: function(obj) {
							AbonApi.comment_set({
                            	uid: (this.oid || 0),
								comment: this.comment_field.getValue()
                        	});
                    	},
                    	scope: this
                	}
            	}
			}],
			listeners: {
                afterrender : {
                    fn: function(obj) {
						AbonApi.comment_get({
                            uid: (this.oid || 0)
                        },this.getCommentCallback.createDelegate(this));
                    },
                    scope: this
                }
            },
			getCommentCallback: function(response) {
				this.comment_field.setValue(response.data.comment)
			}
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonCommentsPanel.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:abon-comments-panel', Ext.ux.AbonCommentsPanel );

