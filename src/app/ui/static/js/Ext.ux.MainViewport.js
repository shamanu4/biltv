Ext.ux.MainViewport = Ext.extend(Ext.Viewport, {
    renderTo: Ext.getBody(),

    initComponent: function(){
        var config = {
            layout: 'border',
            defaults: {
                frame: true
            },
            items: [
                {
                    id: 'tab-panel',
                    region: 'center',
                    tbar: new Ext.ux.TabPanel()
                },{
                    id: 'menu-bar',
                    region: 'north',
                    tbar: new Ext.ux.MenuBar()
                }
            ]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.MainViewport.superclass.initComponent.apply(this, arguments);
    },//initComponent
    sayHello: function(){
        Ext.Msg.prompt('Name', 'Please enter your name:', function(btn, text){
            if (btn == 'ok') {
                MainApi.hi(text, function(response){
                    Ext.ux.msg('Success', response.msg, Ext.Msg.INFO);
                })
            }
        })
    }
});