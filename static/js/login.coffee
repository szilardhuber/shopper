bootstap_alert = Object

bootstap_alert.warning = ->
	$('#alert_placeholder').html('<div class="alert alert-error block-message"><span>'+message+'</span></div>');

bootstap_alert.hide = ->
	$('#alert_placeholder').html('')

$ ->
	# Validate
	$('#login-form').validate 
		rules:
			email:
				required: true
				email: true
			password:
				minlength: 8
				required: true
		highlight: (label) ->
			group = $(label).closest('.control-group')
			group.removeClass 'success'
			group.addClass 'error'
		success: (label) ->
			group = $(label).closest('.control-group')
			group.removeClass 'error'
			group.addClass 'success'
	true
