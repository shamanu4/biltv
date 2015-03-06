Ext.ux.CardTpCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.card_tp_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'name',
            mode: 'local'
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.CardTpCombo.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:free-cards-combo', Ext.ux.FreeCardCombo);


