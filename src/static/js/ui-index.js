Ext.onReady(function(){
    var vp = new Ext.ux.MainViewport();
    Engine.vp = vp;
    Engine.auth.checkAuth();
});


