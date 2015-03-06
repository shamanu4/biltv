Ext.ux.AbonInfoPanel = Ext.extend(Ext.Panel ,{
    initComponent: function() {
        var config = {
            closable: true,
            title: 'Информация',
            border : true,
            defaults: {
                frame: true,
                split: true    
            },
            tbar: new Ext.ux.TabPanel({
                width: 1000,
                height: 480,
                items: [{
                    title: 'Тарифы',
                    xtype: 'panel',
                    layout: 'column',
                    items: [
                        {
                            title: 'Карточки',
                            xtype: 'ext:ux:abon-cards-grid',
                            columnWidth: .5,
                            height: 280,
                            oid: this.oid,
                            parent_form: function(scope){return scope;}(this)
                        },{                            
                            title: 'Тарифы',
                            xtype: 'ext:ux:abon-cards-tp-grid',
                            columnWidth: .5,
                            height: 280,
                            oid: this.oid,
                            parent_form: function(scope){return scope;}(this)
                        }]
                    },{
                        title: 'Оплаты',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype:'ext:ux:abon-payments-grid',
                            oid: this.oid
                        }]
                    },{
                        title: 'Снятия',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype:'ext:ux:abon-fees-grid',
                            oid: this.oid
                        }]
                    },{
                        title: 'Операции',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype:'ext:ux:abon-operations-grid',
                            oid: this.oid
                        }]
                    },{
                        title: 'Дополнительно',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype:'ext:ux:abon-comments-panel',
                            oid: this.oid
                        }]
                    },{                            
                        title: 'История',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                        	xtype: 'ext:ux:abon-history-grid',
                        	oid: this.oid
                        }]
                    },{
                        title: 'Кредиты',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype: 'ext:ux:abon-credits-grid',
                            oid: this.oid
                        }]
                    },{
                        title: 'Нелегалы',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype: 'ext:ux:abon-illegal-grid',
                            oid: this.oid
                        }]
                    },{
                        title: 'Предупреждения',
                        xtype: 'panel',
                        parent_form: this,
                        items: [{
                            xtype: 'ext:ux:abon-warning-grid',
                            oid: this.oid
                        }]
                    }]
            }),
            children_forms:{
                cards : {
                    obj: null
                },
                tariffs: {
                    obj: null
                }
            }
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.AbonentForm.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:abon-info-panel', Ext.ux.AbonInfoPanel);

