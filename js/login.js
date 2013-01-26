bootstrap_alert = function() {}
bootstrap_alert.warning = function(message) {
            $('#alert_placeholder').html('<div class="alert alert-error block-message"><span>'+message+'</span></div>')
}
bootstrap_alert.hide = function() {
			$('#alert_placeholder').html('')
}
        
$(document).ready(function(){

		
		// Call validate on submit and prevent navigation
		$('#submit').click(function(e) {
				e.preventDefault;
				$('#Login-form').valid();
		});


		// Validate
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
				bootstrap_alert.hide();
			},
			submitHandler: function(label) {
				$.ajax({
					url: '/User/Login',
					type: 'POST',
					data: {'email' : $('#email').val(), 'password' : $('#password').val() },
					complete: function(e, xhr, settings){
						if (e.status === 200) {
							window.location.href = "/";
						}
						else if (e.status === 401) {
								bootstrap_alert.warning("Login error. Please try again.");
								$('#password').focus();	
						}
					}
				});
			}
	    });
	  
}); // end document.ready
