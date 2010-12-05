# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url ( r'xml/$', 'statistics.views.statistics_xml_read', name = 'statistics_xml_read' ), 
    url ( r'', 'statistics.views.statistics_read', name = 'statistics_read' ),
)
