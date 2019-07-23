angular.module('starter')

.controller('FeatureCtrl', function($scope, $ionicModal, $timeout, $http, localStorageService, $state,Chats) {

    $scope.data = {};

    $scope.doRefresh = function() {
      $timeout(function () {
        _getData();
        $scope.$broadcast('scroll.refreshComplete');
      }, 2000);
    };
    
    var _getData = function () {

        Chats.get_videos_by_category().get({c:"搞笑"},function(data)
        {
            $scope.data.videos = data.results;
        });
        Chats.get_videos_by_category().get({c:"搞笑"},function(data)
        {
            $scope.data.videos = data.results;
        });

        /*
      $http({method: 'GET', url: './js/data/videos.json'}).then(function successCallback(response) {
        $scope.data.videos = response.data;
      }, function errorCallback(response) {
        console.log(response)
      });
      */
    };

    var _init = function () {
      $scope.data.videos = [];
      _getData();
    };

    _init();

});
