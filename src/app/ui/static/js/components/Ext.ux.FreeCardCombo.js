Ext.ux.FreeCardCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.free_card_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'num',
            mode: 'local'
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.FreeCardCombo.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:free-cards-combo', Ext.ux.FreeCardCombo);

