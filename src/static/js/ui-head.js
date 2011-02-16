function isInt(x) {
   var y=parseInt(x);
   if (isNaN(y)) return false;
   return x==y && x.toString()==y.toString();
}

Engine = {
    vp: null,
    components: {
        
    },
    getComponent: function(component,string) {
        if(string in Engine.components) {
            return Engine.components[string]
        } else {
            Engine.components[string] = new component()
            return Engine.components[string]
        }
    },
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
                    //Ext.ux.msg('Приветствие', response.msg, Ext.Msg.INFO);
                    Ext.getCmp('menu-exit-button').setDisabled(false)
                    this.loadMenu()
                } else {
                    this.doAuth()
                }
            }, this)
        },
        loadMenu: function() {
            MainApi.menu(function(response){
                for (i in response.menuitems) {
                if(isInt(i)) {
                        Ext.getCmp('menu-bar').toolbars[0].add(Ext.ux.menu[response.menuitems[i]]);
                    }
                }
                Ext.getCmp('menu-bar').toolbars[0].doLayout()
            }, this)
        }
    },
    user: {
        permissions: [

        ],
        hasPerm: function() {
            
        }
    },
    menu: {
        address: {
            city: {
                openGrid: function() {
                    grid = Engine.getComponent(Ext.ux.CityGrid,'Ext.ux.CityGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout()
                }
            },
            street: {
                openGrid: function() {
                    grid = Engine.getComponent(Ext.ux.StreetGrid,'Ext.ux.StreetGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout()
                }
            },
            house: {
                openGrid: function() {
                    grid = Engine.getComponent(Ext.ux.HouseNumGrid,'Ext.ux.HouseNumGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout()
                }
            },
            building: {
                openGrid: function() {
                    grid = Engine.getComponent(Ext.ux.BuildingGrid,'Ext.ux.BuildingGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout()
                }
            }
        },
        cashier: {
            abonent: {
                openGrid: function() {
                    grid = Engine.getComponent(Ext.ux.BuildingGrid,'Ext.ux.AbonentGrid')
                    if (grid.store && grid.rendered) {
                        grid.store.load()
                    }
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].add(grid);
                    Ext.getCmp('tab-panel').toolbars[0].doLayout()
                }
            }
        }
    }
}
