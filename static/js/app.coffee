myApp = angular.module 'shopzenion', ['pascalprecht.translate']

myApp.config([
	'$translateProvider',
	($translateProvider) ->
		availableLanguages = ['en', 'hu']
		$translateProvider.translations 'en', Translations.en
		$translateProvider.translations 'hu', Translations.hu
		language = window.navigator.userLanguage or window.navigator.language;
		$translateProvider.preferredLanguage language
		$translateProvider.fallbackLanguage 'en'
		true
	])

myApp.config([
	'$routeProvider',
	($routeProvider) ->
#		$routeProvider.when '/login', 
#			templateUrl: '/login.html'
#			controller: LoginController
		$routeProvider.when '/',
			templateUrl: 'partials/main.html'
			controller: TestController
		.otherwise 
			redirectTo: '/'
		true
	])

myApp.config([
	'$locationProvider'
	($locationProvider) ->
		$locationProvider.html5Mode(true)
		true
	])

myApp.run ($rootScope, $translate) ->
	$rootScope.Constants = window.Constants
	true
