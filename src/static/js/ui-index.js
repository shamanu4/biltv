Ext.onReady(function(){
	var vp = new Ext.ux.MainViewport();
    Ext.ux.msg('Грузимся ....', 'пожалуйста подождите', "ext-mb-invisible");
    Engine.vp = vp;
    Engine.auth.checkAuth();
});


