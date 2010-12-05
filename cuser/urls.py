from django.conf.urls.defaults import *
from cuser.views import *

urlpatterns = patterns ( 'cuser.views',
    url ( r'upgrad/create/$', 'upgrade_create', name = 'upgrade_create' ),
    url ( r'auth/create/$', 'auth_create', name = 'auth_create' ),
    url ( r'auth/delete/$', 'auth_delete', name = 'auth_delete' ),
    url ( r'create/$', user_create, name = 'user_create' ),
    url ( r'update/$', 'user_update', name = 'user_update' ),
)
