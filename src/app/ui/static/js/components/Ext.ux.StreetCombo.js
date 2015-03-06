Ext.ux.StreetCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.streets_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'name',
            mode: 'local'
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.StreetCombo.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:street-combo', Ext.ux.StreetCombo);

