Ext.ux.msg = function(){
    var msgCt;
    function createBox(title, text, type){
        return ['<div class="msg">',
                '<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
                '<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc">',
                '<div class="ext-mb-icon ', type ,'">',
                '<h3>', title, '</h3>', text,
                '</div></div></div></div>',
                '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
                '</div>'].join('');
    }

    return function(title, text, type, callback){
        if(!msgCt){
            msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
        }
        msgCt.alignTo(document, 't-t');
        var m = Ext.DomHelper.append(msgCt, {html:createBox(title, text, type)}, true);
        if(Ext.isFunction(callback)) {
            m.slideIn('t').pause(2).ghost("t", {remove:true,callback:callback});
        } else {
            m.slideIn('t').pause(2).ghost("t", {remove:true});
        }
    }
}();


Ext.ux.LoginForm = Ext.extend(Ext.form.FormPanel,{
    frame:true,
    // configs for FormPanel
    width: 300,
    height: 160,
    padding: 10,
    initComponent: function(){
        var config = {
            buttons:[{
                text: 'ОК',
                handler: function(){
                    this.getForm().submit({
                        failure: function(form, action){
                            if(this.getForm().isValid()) {
                                Ext.ux.msg('Ошибка авторизации', action.result.msg, Ext.Msg.ERROR);
                            } else {
                                Ext.ux.msg('Ошибка ввода', 'обязательные поля не заполнены', Ext.Msg.ERROR);
                            }
                            this.ownerCt.loginFailed()
                            this.getForm().reset()                            
                        },
                        success: function(form, action){
                            Ext.ux.msg('Авторизация успешная', action.result.msg, Ext.Msg.INFO);
                            this.ownerCt.loginSuccess()
                            this.ownerCt.close()                            
                        },
                        scope: this
                    });                    
                },
                scope: this
            }],

            submitaction: function() {
                alert(1);
            },

            keys: [
                {
                    key: [Ext.EventObject.ENTER], handler: function() {
                        Ext.Msg.alert("Alert","Enter Key Event !");
                        this.submitaction()
                    }
                }
            ],

            defaults: {anchor: '100%'},
            defaultType: 'textfield',
            items: [{
                fieldLabel: 'Логин',
                allowBlank: false,
                name: 'username'
            },{
                fieldLabel: 'Пароль',
                allowBlank: false,
                name: 'password',
                inputType: 'password'
            }],

            // configs for BasicForm
            api: {
                submit: MainApi.login
            },
            clientValidation: true,
            paramsAsHash: true
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.LoginForm.superclass.initComponent.apply(this, arguments);
    }//initComponent    
});


Ext.ux.LoginWindow = Ext.extend(Ext.Window,{
    initComponent: function(){
        var config = {
            title: '"ТРК "TIM" вход в защищённую зону',
            layout: 'fit',
            height: 140,
            width: 260,
            closable: false,
            resizable: false,
            draggable: false,
            items: [new Ext.ux.LoginForm()]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.LoginWindow.superclass.initComponent.apply(this, arguments);
    },
    loginSuccess: function() {},
    loginFailed: function() {}
});


Ext.ux.TabPanel = Ext.extend(Ext.TabPanel,{
    initComponent: function(){
        var config = {
            frame:true
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.TabPanel.superclass.initComponent.apply(this, arguments);
    }
});


Ext.ux.MenuBar = Ext.extend(Ext.Toolbar,{
    initComponent: function(){
        var config = {
            items: [
                {
                    id: 'menu-exit-button',
                    xtype: 'tbbutton',
                    disabled: true,
                    text: 'Выход',
                    handler: Engine.auth.doLogout
                }
            ]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.MenuBar.superclass.initComponent.apply(this, arguments);
    }
});

/*
Ext.ux.ChannelGrid = new Ext.grid.GridPanel({
    initComponent: function(){
        var config = {
            frame:true,
            title: 'Movie Database',
            height:200,
            width:500,
            store: channels-store,
            columns: [
                {header: "Id", dataIndex: 'id'},
                {header: "Name", dataIndex: 'name'},
                {header: "Comment", dataIndex: 'comment'},
            ]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.ChannelGrid.superclass.initComponent.apply(this, arguments);
    }
});
*/