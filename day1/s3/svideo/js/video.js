angular.module('starter')

.controller('VideoCtrl', function($scope, $ionicModal,$stateParams, $timeout, localStorageService, $sce, Chats) {
        vid = $stateParams.id;
        $scope.data = {};

    $scope.trustSrc = function(src) {
      return $sce.trustAsResourceUrl(src);
    }

        Chats.get_video().get({"id":vid},function(data)
        {
            $scope.data.video = data.results;
        });

    //$scope.data.video = localStorageService.get('viewVideo');
    //$scope.data.video.listEp = _.range($scope.data.video.ep);
    //console.log($scope.data, _.range($scope.data.video.ep));




  });
