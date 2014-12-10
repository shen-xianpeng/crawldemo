Date.prototype.format = function(format){ 
    var o = { 
    "M+" : this.getMonth()+1, //month 
    "d+" : this.getDate(), //day 
    "h+" : this.getHours(), //hour 
    "m+" : this.getMinutes(), //minute 
    "s+" : this.getSeconds(), //second 
    "q+" : Math.floor((this.getMonth()+3)/3), //quarter 
    "S" : this.getMilliseconds() //millisecond 
    } ;
 
    if(/(y+)/.test(format)) { 
    format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
    } 
 
    for(var k in o) { 
        if(new RegExp("("+ k +")").test(format)) { 
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length)); 
        } 
    } 
    return format; 
};
//window.filter_func = [];
function filterarg(post_list_view, filter_config){
    var f = function (value){

            return function () {
                return {source_cat: value}
        }
    };
    for (var name in filter_config){
        var filter_key = filter_config[name];
        var f_func = f(filter_key);
        //window.func.push(f_func);
        post_list_view.addQuickFilter(name, f_func(name));
    };
};



/*global angular*/
(function () {
    "use strict";

    var app = angular.module('myApp', ['ng-admin']);

    app.controller('main', function ($scope, $rootScope, $location) {
        $rootScope.$on('$stateChangeSuccess', function () {
            $scope.displayBanner = $location.$$path === '/dashboard';
        });
    });

    app.directive('customPostLink', ['$location', function ($location) {
        return {
            restrict: 'E',
            template: '<a ng-click="displayPost(entry)">{{entry.values.title}}</a>',
            link: function ($scope) {
                $scope.displayPost = function (entry) {
                    var postId = entry.values.id;

                    $location.path('/show/posts/' + postId);
                };
            }
        };
    }]);

    app.config(function (NgAdminConfigurationProvider, Application, Entity, Field, Reference, ReferencedList, ReferenceMany) {


        function date_format(time_float) {
        //ng-admin map存在bug
        //console.log(typeof(time_float));
            if(typeof(time_float)!='number') return time_float;
            console.log(time_float);
            var date = new Date(time_float*1000);

            var date = new Date(time_float*1000);
            //console.log(date);
            //return time_float;
            //alert(date.format("yyyy"));
            return date.format("yyyy-MM-dd hh:mm");

        
        }

        function extraParams() {
            var now = Date.now();
            var hash = md5(now + privateKey + publicKey);

            return {
                apikey: publicKey,
                hash: hash,
                ts: now
            };
        }
        var totalCount;
        function interceptor(data, operation, what, url, response, deferred){
        console.log(operation);
            if (operation === 'getList') {
               totalCount = response.data.total;
                    response.total= totalCount
                return response.data.data;
            } else if (operation === 'get') {
                window.data=data;
                return ('data' in data) ? data.data: data;
            }else{
                return data;
            }
        }

        function totalItems(response){
            return response.total;
        }

        function pagination(page, maxPerPage) {
            return {
                offset: (page - 1) * maxPerPage,
                limit: 10
            }
        }


        function newline2br(value) {
            if (!value) {
                return '';
            }
            window.l = value.replace("\n", "<br>");
            return value.replace("\n", "<br>");
        }

        function truncate(value) {
            if (!value) {
                return '';
            }
            return value.length > 10 ? value.substr(0, 10) + '...' : value;
        }

//        function pagination(page, maxPerPage) {
//            return {
//                _start: (page - 1) * maxPerPage,
//                _end: page * maxPerPage
//            };
//        }

        var app = new Application('亲子活动') // application main title
            .baseApiUrl('http://xianpeng.org:5000/'); // main API endpoint

        // define all entities at the top to allow references between them
        var post = new Entity('posts').label('活动'); // the API endpoint for posts will be http://localhost:3000/posts/:id


        var tag = new Entity('tags').label('分类')
            .readOnly(); // a readOnly entity has disabled creation, edition, and deletion views

        // set the application entities
        app
            .addEntity(post)
            .addEntity(tag);
            //.addEntity(comment);

        // post.menuView()
        //     .order(1); // post should be the first item in the sidebar menu

        post.dashboardView()
            .title('最近的活动')
            .totalItems(totalItems)
            .interceptor(interceptor)
            .order(1)
            .limit(10)
            .pagination(pagination)
            .addField(new Field('title')//.isDetailLink(true).map(truncate)
                    .type('template')
                    .label('标题')
                    .template(function () {
                      return '<custom-post-link></custom-post-link>';
                     })
                );

        var post_list_view = post.listView()
            .totalItems(totalItems)
            .interceptor(interceptor)
            .title('所有的活动') // default title is "List of [entity_name]s"
            .perPage(10)
            .pagination(pagination)
            .addField(new Field('index').label('序号').isDetailLink(true))
            .addField(new Field('title').label('标题').map(truncate)) // the default list field type is "string", and displays as a string
            .addField(new Field('age_range').label('适合年龄'))
            .addField(new Field('can_join').label('能否报名').type('boolean'))
            .addField(new Field('apply_start').label('报名开始').map(date_format))
            .addField(new Field('apply_end').label('报名结束').map(date_format))
            .addField(new Field('address').label('地址').map(truncate))
            .addField(new Field('price').type('wysiwyg').label('价格'))
            .addField(new Field('status').label('状态'))
            .addField(new ReferenceMany('cat') // a Reference is a particular type of field that references another entity
                .targetEntity(tag) // the tag entity is defined later in this file
                .targetField(new Field('title')) // the field to be displayed in this list
                .label('类别')
        );      
        post_list_view.addTab({0:['show','edit','delete']});
        post_list_view.sortParams(function(field, dir) {
		    return {
		        params: { _sort: field, _sortDir: dir },
		        headers: {}
		    };
		});
        var filter_config = {
            '父母邦': 'fumubang',
            '哈哈儿童': 'haha',
            '爱早教': 'izaojiao',
            '玩童会': 'bbeden'
            };
        filterarg(post_list_view, filter_config);
//	                var now = new Date(),
//	                    year = now.getFullYear(),
//	                    month = now.getMonth() + 1,
//	                    day = now.getDate();
//	                month = month < 10 ? '0' + month : month;
//	                day = day < 10 ? '0' + day : day;

        post.showView() // a showView displays one entry in full page - allows to display more data than in a a list
             .title('"{{ entry.values.title }}"')
            .addField(new Field('id'))
            .addField(new Field('title').label('标题'))
            .addField(new Field('age_range').label('适合年龄'))
            .addField(new Field('price').label('价格'))
            .addField(new Field('act_time_desc').label('活动时间描述'))
            .addField(new Field('apply_start').label('报名开始').map(date_format))
            .addField(new Field('apply_end').label('报名结束').map(date_format))
            .addField(new Field('orig_apply_time_str').label('报名截止时间'))
            .addField(new Field('brief').label('简介'))
            .addField(new Field('content').type('text').label('内容'))
            .addField(new Field('body').type('wysiwyg').label('主体'))
            .addField(new Reference('cat')
                .targetEntity(tag)
                .targetField(new Field('title'))
                .label('分类')
            )
            .addField(new Field('link').label('原始链接').type('template').template(function () {
                            return "<a href='{{entry.values.link}}' target='_blank'>{{entry.values.link}}</a>";
                        })
             );

        post.creationView()
            .title('创建活动')
            .addField(new Field('title').label("标题")) // the default edit field type is "string", and displays as a text input
            .addField(new Field('content').type('wysiwyg').label('内容')) // overriding the type allows rich text editing for the body

        post.editionView()
            .title('编辑 "{{ entry.values.title }}"') // title() accepts a template string, which has access to the entry
            .actions(['list', 'show', 'delete']) // choose which buttons appear in the action bar
            .addField(new Field('title').label("标题"))
            .addField(new Field('price').label('价格'))
            .addField(new Field('age_range').label('适合年龄'))
            .addField(new Field('act_time_desc').label('活动时间描述'))
            .addField(new Field('brief').label('简介'))
            .addField(new Field('content').type('text').label('内容'))
            .addField(new Field('body').type('wysiwyg').label('主体'))
            .addField(new Reference('cat').label("分类")
                .targetEntity(tag)
                .targetField(new Field('title')));

 
        // tag.menuView()
        //     .order(3);

        tag.dashboardView()
            .title('分类列表')
            .order(3)
            .limit(10)
            .totalItems(totalItems)
            .interceptor(interceptor)
            .pagination(pagination)
            .addField(new Field('id').label('ID'))
            .addField(new Field('title').label('名字'));

        tag.listView()
            .totalItems(totalItems)
            .interceptor(interceptor)
            .title('所有类别')
            .infinitePagination(false) // by default, the list view uses infinite pagination. Set to false to use regulat pagination
            .pagination(pagination)
            .addField(new Field('id').label('ID'))
            .addField(new Field('title')
                .type('template')
                .label('分类名字')
                .template(function () {
                    return '{{ entry.values.title.toUpperCase() }}';
                })
        )
            .listActions(['show']);

        tag.showView()
            .addField(new Field('title').label('名称'))
            .addField(new Field('是否显示').type('boolean'));

        NgAdminConfigurationProvider.configure(app);
    });
}());
