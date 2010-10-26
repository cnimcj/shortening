from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url ( 'create/$', 'ittybitty.views.shortening_create', name = 'shorting_create' ),
)