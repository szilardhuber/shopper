TestController = ($rootScope, $scope, $window) ->
	$scope.Constants = $window.Constants
#	$.ajax
#		url: "#{window.Constants.product_list_url}"
#		data: 'q=tes'
#		dataType: 'json'
#		type: 'GET'
#		error: (jqXHR, textStatus, errorThrown) ->
#			$('body').append "AJAX Error: #{textStatus} #{jqXHR}"
#		success: (data, textStatus, jqXHR) ->
#			$scope.$apply ->
#				$scope.products = data
	true


LoginController = ($scope, $window, $http) ->
	$scope.loginSent = false

	reset = () ->
		$scope.$apply () ->
			$scope.loginSent = false
			true

	$scope.sendEmail = (form) ->
		email = form.email.$modelValue
		$scope.loginSent = true
		$window.setInterval reset, Constants.login_timeout
		$http(
			url: "/api/v2/sessions/new"
			method: "GET"
			params:
				email: email
		).success((response) ->
				alert(response)
		).error((data, status, headers, config) ->
			alert(status)
		)
		true

	$scope.emailChange = (loginEmail) ->	
		if loginEmail.$valid
			$('#emailGroup').removeClass('has-error')
			$('#emailGroup').addClass('has-success')
		else
			$('#emailGroup').removeClass('has-success')
			$('#emailGroup').addClass('has-error')
		true

	$scope.submit = () ->
		alert('Hehe')
		true

	true
