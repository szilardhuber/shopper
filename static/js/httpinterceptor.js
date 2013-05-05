var interceptor = ['$rootScope','$q', function($scope, $q) {

  function success(response, headers) {
    if (headers) {
      $scope.sessionCookie = headers['Set-Cookie'];
    }
    return response;
  }

  function error(response) {
    var status = response.status;

    if (status == 401) {
      var deferred = $q.defer();
      var req = {
        config: response.config,
        deferred: deferred
      };
      $scope.requests401.push(req);
      $scope.$broadcast('event:loginRequest');
      return deferred.promise;
    }
    return $q.reject(response);
  }

  return function(promise) {
    return promise.then(success, error);
  };
}];
