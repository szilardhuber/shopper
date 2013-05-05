function ListOfListsController($scope, $routeParams, $http, $cookieStore, $cookies) {
    var headers = {};
    headers['Cookie'] = $scope.sessionCookie;
    $http({method: 'GET', url: serverUrl + '/api/v1/Lists', headers: headers}).success(function(data, status, headers, config) {
        if (data.length === 0) {
            params = {name: 'Shopping List'};
            $http({method: 'POST', url: serverUrl + '/api/v1/Lists', headers: headers, params: params}).success(function(data, status, headers, config) {
                if (status == 200) {
                    window.location.reload();
                }
            });
        }
        else {
            $scope.lists = data;
        }
    });
}
