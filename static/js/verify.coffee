bootstrap_alert = Object

bootstrap_alert.warning = (message) ->
	$('#alert_placeholder').html('<div class="alert alert-error block-message"><span>'+message+'</span></div>')

bootstrap_alert.hide = ->
	$('#alert_placeholder').html('')

$ ->
	# Validate
	$('#resend-form').validate
		rules:
			email:
				required: true
				email: true
		highlight: (label) ->
			group = $(label).closest('.control-group')
			group.removeClass 'success'
			group.addClass 'error'
		success: (label) ->
			group = $(label).closest('.control-group')
			group.removeClass 'error'
			group.addClass 'success'
	true
