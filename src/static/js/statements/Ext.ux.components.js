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
        if(type=="ext-mb-error") {
            var delay = 10;
        } else if (type=="ext-mb-invisible") {
            var delay = 1
        } else {
            var delay = 3
        }
        if(!msgCt){
            msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true)
        }
        msgCt.alignTo(document, 't-t');
        var m = Ext.DomHelper.append(msgCt, {html:createBox(title, text, type)}, true);
        if(Ext.isFunction(callback)) {
            m.slideIn('t').pause(delay).ghost("t", {remove:true,callback:callback});
        } else {
            m.slideIn('t').pause(delay).ghost("t", {remove:true});
        }
    }
}();

Ext.ux.traceback = function() {
	
	function createBox(text,token) {
		
		return [
    	'<form action="/traceback/" id="traceback-form" method="POST">',
    		'<input type="hidden" name="csrfmiddlewaretoken" value="'+token+'" />',
    		'<label for="traceback-content">трейсбек:</label>',
    		'<br />',
        	'<textarea id="traceback-content" cols="75" rows="8" name=traceback disabled>',
        		text,         
        	'</textarea>',
        	'<br />',
        	'<label for="traceback-description">',
        		'опишите Ваши действия перед сбоем <br />',
        		'это поможет решить проблему быстрее <br />',
        	'</label>',
        	'<textarea id="traceback-descripton" cols="75" rows="10" name=traceback-descr>',        		         
        	'</textarea>',
    		'<br />',
        '</form>',
    	].join('')
	}
	
	return function(title,text,token) {
		
		new Ext.Window({			
			title: title,
	        plain: true,
	        html:createBox(text,token), 
	        modal: true,
	        width: 600,
	        buttons: [{
	            text: 'отослать отчёт',
	            handler: function() {
	            	$("#traceback-content").removeAttr("disabled");
	            	Ext.get("traceback-form").dom.submit();	          	    	           
	            }
	        }],
	    }).show();
	}
	
}(); 
