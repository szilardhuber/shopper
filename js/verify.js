bootstrap_alert = function() {}
bootstrap_alert.warning = function(message) {
            $('#alert_placeholder').html('<div class="alert alert-error block-message"><span>'+message+'</span></div>')
}
bootstrap_alert.hide = function() {
			$('#alert_placeholder').html('')
}
        
$(document).ready(function(){
		// Validate
		$('#resend-form').validate({
			rules: {
			  email: {
				required: true,
				email: true
			  }
			},
			highlight: function(label) {
				$(label).closest('.control-group').removeClass('success');
				$(label).closest('.control-group').addClass('error');
			},
			success: function(label) {
				$(label).closest('.control-group').removeClass('error');
				$(label).closest('.control-group').addClass('success');
			},
	    });
	  
}); // end document.ready
