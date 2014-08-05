Ext.onReady(function(){
	var vp = new Ext.ux.MainViewport();
	Ext.ux.msg('Грузимся ....', 'пожалуйста подождите', "ext-mb-invisible");
    Engine = window.Engine || {};
    Engine.vp = vp;
    Engine.auth.checkAuth();
    
	$.alerts._overlay = function(status) {
			switch( status ) {
				case 'show':
					alertsMask.show();			
				break;
				case 'hide':
					alertsMask.hide();
				break;
			}
		}

});


