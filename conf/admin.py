#! -*- encoding: utf-8 -*-
from django.contrib import admin
from conf.models import Config

class ConfigAdmin ( admin.ModelAdmin ):
    list_display = ( 'key', 'value', 'help_text', )

admin.site.register ( Config, ConfigAdmin )
