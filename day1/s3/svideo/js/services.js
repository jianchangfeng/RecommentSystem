if (typeof(base_url) == "undefined")
{
  //var base_url = "http://rest.appbk.com/video/"; //修改为服务器的地址
  var base_url = "http://112.124.115.52:8080/" 
  var uid = "maris@appbk.com" //用户id
}

angular.module('starter.services', [])

.factory('Chats', function ($resource) {
  return {
    get_videos_by_category:function(){ //获得视频推荐列表
      return $resource(base_url + "get_videos_by_category?c=:c&uid=" + uid);
    },
      get_video:function(){ //获得一个视频的信息
      return $resource(base_url + "get_video?id=:id&uid=" + uid);
    },
      add_action:function(){ //添加用户行为
      return $resource(base_url + "add_action?uid="+uid+"&id=:id&action=:action");
    },
      get_videos_by_search:function(){ //搜索
      return $resource(base_url + "get_videos_by_search?n=:n");
    },
      get_relate_videos:function(){ //获得相关视频
      return $resource(base_url + "get_relate_videos?id=:id&uid="+uid);
    },
  };
});
/*
.factory('app_resource', function ($resource) {
  return {
    get_game_categories:function(){
      return $resource(base_url + 'app/get_game_categories');
    }
  };
});
*/
