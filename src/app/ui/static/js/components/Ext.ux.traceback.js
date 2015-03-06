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
        '</form>'
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
	        }]
	    }).show();
	}
	
}(); 

