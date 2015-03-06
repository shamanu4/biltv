Ext.ux.LoginWindow = Ext.extend(Ext.Window,{
    initComponent: function(){
        var config = {
            title: 'Панель оператора КТБ',
            layout: 'fit',
            height: 140,
            width: 260,
            closable: false,
            resizable: false,
            draggable: false,
            items: [new Ext.ux.LoginForm()]
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.LoginWindow.superclass.initComponent.apply(this, arguments);
    },
    loginSuccess: function() {},
    loginFailed: function() {}
});


