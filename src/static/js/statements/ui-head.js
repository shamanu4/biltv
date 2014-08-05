function isInt(x) {
   var y=parseInt(x);
   if (isNaN(y)) return false;
   return x==y && x.toString()==y.toString();
}


alert = jAlert; 
//confirm = jConfirm;
//prompt= jPrompt;
alertsMask = new Ext.LoadMask(Ext.getBody(),{msg:null});		

Engine = {
    vp: null,
    components: {
        
    },
    getComponent: function(component,string,params) {
        if(string in Engine.components) {
            Ext.apply(Engine.components[string], params);            
			return Engine.components[string]
        } else {
            Engine.components[string] = new component(params)
			return Engine.components[string]
        }
    },
    getComponentFromPool: function(component,string,params,instances) {
        if(!instances) {
            instances=10;
        }
        if(!(string in Engine.components)) {
            Engine.components[string] = {
                index : 0,
                data : []
            }
        }
        Engine.components[string].index++;
        var index = Engine.components[string].index;
        Engine.components[string].data[index]=new component(params);
        if(Engine.components[string].index-instances>0) {
            Engine.components[string].data[index-instances].destroy();
            Engine.components[string].data[index-instances]=null;
        }
        return Engine.components[string].data[index];
    },
    auth: {
        doAuth: function() {
			Ext.get('loading').hide();
			Ext.get('loading-mask-half').hide();
            location.href="/"
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
                    Ext.get('loading').hide();
                    Ext.get('loading-mask-half').hide();
                } else {
                    this.doAuth()
                }
            }, this)
        }
//        loadMenu: function() {
//			MainApi.menu(function(response){
//                for (i in response.menuitems) {
//                if(isInt(i)) {
//                        Ext.getCmp('menu-bar').toolbars[0].add(Ext.ux.menu[response.menuitems[i]]);
//                    }
//                }
//                Ext.getCmp('menu-bar').toolbars[0].doLayout()
//				Ext.get('loading').hide();
//				Ext.get('loading-mask-half').hide();
//            }, this)
//        }
    },
    user: {
		id: null,
        permissions: [

        ],
        hasPerm: function() {
            
        }
    }
}
