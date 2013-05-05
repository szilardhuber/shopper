var serverUrl = '';
var currentListId = 0;

var myModule = angular.module('shopper', ['ngCookies']);

/* 
 * Config routes
 */
myModule.config(['$routeProvider', function($routeProvider) {
  $routeProvider
      .when('/', {templateUrl:serverUrl+'/partial/ang-shoppinglist.html', controller:ListOfListsController})
      .when('/:listId', {templateUrl:serverUrl+'/partial/ang-list.html', controller:ListController})
      .otherwise({redirectTo: '/'});
}]);

/*
 * Set http interceptor
 */
myModule.config(function($httpProvider) {
  $httpProvider.responseInterceptors.push(interceptor);
});

/*
 * Set up swipe handling directive
 */
 myModule.directive('swipeable', function() {
    return {
      restrict: 'A',
      compile: function compile(element, attrs, transclude) {
        return function postLink(scope, element, attrs) {
          Hammer(element[0].parentNode, {
            swipe_velocity : 0.2
          }).on("swiperight", swipeRight);
        };
      }
    };
 });


myModule.run(['$rootScope', '$http', '$cookieStore', '$cookies', function($scope, $http, $cookieStore, $cookies) {
  $scope.requests401 = [];

  /**
  * On 'event:loginRequest' send credentials to the server.
  */
  $scope.$on('event:loginRequest', function(event, username, password) {
    window.location = '/User/Login';
    return;
  });
}]);
