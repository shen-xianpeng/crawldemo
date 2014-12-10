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
                return ('data' in data) ? data.data.results[0] : data;
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
            .baseApiUrl('http://10.192.64.83:5000/'); // main API endpoint

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
                    .label('Actions')
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
             .addField(new Field('business').label('商家').map(truncate))
            .addField(new Field('title').label('标题').map(truncate)) // the default list field type is "string", and displays as a string
            .addField(new Field('attend_time').label('参与时间'))
            .addField(new Field('address').label('地址'))
            .addField(new Field('status').label('状态'))
            .addField(new ReferenceMany('tags') // a Reference is a particular type of field that references another entity
                .targetEntity(tag) // the tag entity is defined later in this file
                .targetField(new Field('name')) // the field to be displayed in this list
        )
        post_list_view.addTab({0:['show','edit','delete']});
        post_list_view.addQuickFilter('父母帮', function () { // a quick filter displays a button to filter the list based on a set of query parameters passed to the API
                var now = new Date(),
                    year = now.getFullYear(),
                    month = now.getMonth() + 1,
                    day = now.getDate();
                month = month < 10 ? '0' + month : month;
                day = day < 10 ? '0' + day : day;
                return {
                    source_cat: 'fumubang'
                };
            });
            //.listActions(['show', 'edit', 'delete']);

        post.showView() // a showView displays one entry in full page - allows to display more data than in a a list
             .title('"{{ entry.values.title }}"')
            .addField(new Field('id'))
            .addField(new Field('title'))
            .addField(new Field('attend_time'))
            .addField(new Field('content').type('wysiwyg'))
            .addField(new ReferenceMany('tags')
                .targetEntity(tag)
                .targetField(new Field('name'))
        );

        post.creationView()
            .title('创建活动')
            .addField(new Field('title').label("标题")) // the default edit field type is "string", and displays as a text input
            .addField(new Field('content').type('wysiwyg').label('内容')) // overriding the type allows rich text editing for the body

        post.editionView()
            .title('编辑 "{{ entry.values.title }}"') // title() accepts a template string, which has access to the entry
            .actions(['list', 'show', 'delete']) // choose which buttons appear in the action bar
            .addField(new Field('title').label("标题"))
            .addField(new Field('content').type('wysiwyg').label('内容'))
            .addField(new ReferenceMany('tags')
                .targetEntity(tag)
                .targetField(new Field('name')));

 
        // tag.menuView()
        //     .order(3);

        tag.dashboardView()
            .title('Recent tags')
            .order(3)
            .limit(10)
            .totalItems(totalItems)
            .interceptor(interceptor)
            .pagination(pagination)
            .addField(new Field('id').label('ID'))
            .addField(new Field('name'))
            .addField(new Field('published').label('Is published ?').type('boolean'));

        tag.listView()
            .totalItems(totalItems)
            .interceptor(interceptor)
            .title('所有类别')
            .infinitePagination(false) // by default, the list view uses infinite pagination. Set to false to use regulat pagination
            .pagination(pagination)
            .addField(new Field('id').label('ID'))
            .addField(new Field('name'))
            .addField(new Field('published').type('boolean'))
            .addField(new Field('custom')
                .type('template')
                .label('分类名字')
                .template(function () {
                    return '{{ entry.values.name.toUpperCase() }}';
                })
        )
            .listActions(['show']);

        tag.showView()
            .addField(new Field('name'))
            .addField(new Field('是否显示').type('boolean'));

        NgAdminConfigurationProvider.configure(app);
    });
}());
