bootstrap_alert = function() {}
bootstrap_alert.warning = function(message) {
            $('#alert_placeholder').html('<div class="alert alert-error block-message"><span>'+message+'</span></div>')
}
bootstrap_alert.success = function(message) {
            $('#alert_placeholder').html('<div class="alert alert-success block-message"><span>'+message+'</span></div>')
}
bootstrap_alert.hide = function() {
			$('#alert_placeholder').html('')
}
        
$(document).ready(function(){

		
		// Call validate on submit and prevent navigation
		$('#submit').click(function(e) {
				e.preventDefault;
				$('#register-form').valid();
		});


		// Validate
		$('#register-form').validate({
			rules: {
			  email: {
				required: true,
				email: true
			  },
			  password: {
				required: true,
				minlength: 8
			  },
			  password2: {
			    required: true,
			    equalTo: "#password"
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
			submitHandler: function(label) {
				bootstrap_alert.hide();
				$.ajax({
					url: '/User/Register',
					type: 'POST',
					data: {'email' : $('#email').val(), 'password' : $('#password').val() },
					complete: function(e, xhr, settings){
						if (e.status === 200) {
							bootstrap_alert.success("Successfull registration. An email was sent to your address to confirm you identity.");
						}
						else if (e.status === 400) {
								bootstrap_alert.warning("Registration error. Please try again.");
								$('#password').focus();	
						}
					}
				});
			}
	    });
	  
}); // end document.ready
