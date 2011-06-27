Ext.onReady(function(){
	var vp = new Ext.ux.MainViewport();
    Ext.ux.msg('Грузимся ....', 'пожалуйста подождите', "ext-mb-invisible");
    Engine.vp = vp;
    Engine.auth.checkAuth();
	Ext.get(document).on('keypress', function(e,o) {
		if(e.ctrlKey) {
			e.preventDefault()
			if(e.button==119) {
				// Ctrl+X
					active_tab = Ext.getCmp("tab-panel").toolbars[0].getActiveTab()
					if (active_tab) {
							(function(){
								this.hide()
								Ext.getCmp("tab-panel").toolbars[0].remove(this.id);
								Ext.getCmp("tab-panel").toolbars[0].doLayout();
							}).defer(100, active_tab);						
					}				
				
			}								
		}            				               				
    });
});


