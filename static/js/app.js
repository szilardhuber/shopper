// Generated by CoffeeScript 1.6.3
var myApp;

myApp = angular.module('shopzenion', ['pascalprecht.translate']);

myApp.config([
  '$translateProvider', function($translateProvider) {
    var availableLanguages, language;
    availableLanguages = ['en', 'hu'];
    $translateProvider.translations('en', Translations.en);
    $translateProvider.translations('hu', Translations.hu);
    language = window.navigator.userLanguage || window.navigator.language;
    $translateProvider.preferredLanguage(language);
    $translateProvider.fallbackLanguage('en');
    return true;
  }
]);

myApp.config([
  '$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {
      templateUrl: 'partials/main.html',
      controller: TestController
    }).otherwise({
      redirectTo: '/'
    });
    return true;
  }
]);

myApp.config([
  '$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode(true);
    return true;
  }
]);

myApp.run(function($rootScope, $translate) {
  $rootScope.Constants = window.Constants;
  return true;
});
