// 
//	jQuery Validate example script
//
//	Prepared by David Cochran
//	
//	Free for your use -- No warranties, no guarantees!
//

$(document).ready(function(){

	// Validate
	// http://bassistance.de/jquery-plugins/jquery-plugin-validation/
	// http://docs.jquery.com/Plugins/Validation/
	// http://docs.jquery.com/Plugins/Validation/validate#toptions
	
		$('#Login-form').validate({
	    rules: {
	      email: {
	        required: true,
	        email: true
	      },
	      password: {
	      	minlength: 8,
	        required: true
	      }
	    },
	    highlight: function(label) {
	    	$(label).closest('.control-group').removeClass('success');
	    	$(label).closest('.control-group').addClass('error');
	    },
	    success: function(label) {
	    	$(label).closest('.control-group').removeClass('error');
	    	$(label).closest('.control-group').addClass('success');
	    }
	  });
	  
}); // end document.ready