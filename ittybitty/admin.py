from django.contrib import admin
from models import IttyBittyURL, URLWhiteList

class IttyBittyURLAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'url', 'date_created', 'hits')
    list_display_links = ('shortcut', 'url')
    search_fields = ('shortcut', 'url')
    list_filter = ('date_created', 'date_updated')
    date_hierarchy = 'date_created'

class URLWhiteListAdmin ( admin.ModelAdmin ):
    list_display = ( 'url', )

admin.site.register(IttyBittyURL, IttyBittyURLAdmin)
admin.site.register ( URLWhiteList, URLWhiteListAdmin )
