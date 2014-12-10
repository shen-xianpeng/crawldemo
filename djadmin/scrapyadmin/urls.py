# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from admin import urls as adminurls
from admin.views import index_view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scrapyadmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', index_view),
    url(r'^', include('admin.urls')),
)
