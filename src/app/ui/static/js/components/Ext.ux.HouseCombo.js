Ext.ux.HouseCombo = Ext.extend(Ext.form.ComboBox, {
    initComponent: function() {
        var config = {
            store: Ext.ux.houses_combo_store,
            editable: true,
            forceSelection: true,
            lazyRender: false,
            triggerAction: 'all',
            valueField: 'id',
            displayField: 'num',
            mode: 'local'
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.HouseCombo.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:house-combo', Ext.ux.HouseCombo);

Ext.apply(Ext.form.VTypes, {
    decimal:  function(v) {
        return /^\d{1,5}$/.test(v);
    },
    decimalText: 'Должно быть числом 0-99999',
    decimalMask: /[\d]/i
});

