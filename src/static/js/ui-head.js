

Engine = {
    vp: null,
    auth: {
        doAuth: function() {
            lw = new Ext.ux.LoginWindow()
            lw.show()
            lw.caller = this
            lw.loginSuccess = (function(){
                lw.caller.checkAuth()
            })
        },
        doLogout: function() {
            MainApi.logout(function(response){
                if(response.success) {
                    Ext.ux.msg('Завершение работы', response.msg, Ext.Msg.INFO, function(){
                        location.reload()
                    });
                } else {
                    Ext.ux.msg('Завершение работы', 'ошибка при завершении работы', Ext.Msg.ERROR);
                }
            }, this)
        },
        checkAuth: function() {
            MainApi.is_authenticated(function(response){
                if(response.authenticated) {
                    Ext.ux.msg('Приветствие', response.msg, Ext.Msg.INFO);
                    Ext.getCmp('menu-exit-button').setDisabled(false)
                    this.loadMenu()
                } else {
                    this.doAuth()
                }
            }, this)
        },
        loadMenu: function() {
            MainApi.menu(function(response){
                //debugger;
                Ext.getCmp('menu-bar').toolbars[0].add(response.menuitems);
                Ext.getCmp('menu-bar').toolbars[0].doLayout()
            }, this)
        }
    },
    user: {
        permissions: [

        ],
        hasPerm: function() {
            
        }
    }
}

/*
                {
                    xtype: 'tbseparator'
                },{
                    id: 'menu-scrambler-button',
                    xtype: 'tbbutton',
                    text: 'Скрамблер',
                    disabled: true,
                    menu: [
                        {
                            text: 'Каналы'
                        },{
                            text: 'Стволы'
                        },
                    ]
                },{
                    xtype: 'tbseparator'
                },{
                    id: 'menu-cashier-button',
                    xtype: 'tbbutton',
                    text: 'Касса',
                    disabled: true,
                    menu: [
                        {
                            text: 'Item One'
                        },{
                            text: 'Item Two'
                        },{
                            text: 'Item Three'
                        }
                    ]
                }
*/