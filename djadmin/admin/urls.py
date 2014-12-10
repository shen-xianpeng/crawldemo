from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns('',
    url(r'posts/?$', PostApi.as_view(),
        name='post_list'),
    url(r'posts/(?P<post_id>\w+)/?$', PostApi.as_view(),
        name='post_api'),
    url(r'tags/?$', tag_list,
        name='tag_list'),
    url(r'tags/(?P<tag_id>\w+)/?$', tag_detail,
        name='tag_detail'),
)
