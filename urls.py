# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()
# TODO 数据统计 用户或者站长查看统计数据

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^shortening/', include('shortening.ittybitty.urls')),
    url (r'^(?P<shortening>\w+)', 'shortening.ittybitty.views.shortening_read', name = 'shortening_read' ),
)
