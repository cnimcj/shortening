# -*- encoding:utf-8 -*-
from django.db import models

class ConfigManager ( models.Manager ):
    def keyWithInt ( self, key ):
        return int ( self.key ( key ) )

    def key ( self, key ):
        return super ( ConfigManager, self ).get_query_set ().get ( key = key ).value

class Config ( models.Model ):
    """
    >>> config = Config ( key = u"设置", help_text = u"设置", value = "内容" )
    >>> config.save ()
    >>> Config.objects.key ( u"设置" )
    u'\u5185\u5bb9'
    >>> Config.objects.keyWithInt ( u"设置" )
    """
    key = models.CharField ( u"键", max_length = 100, unique = True )
    help_text = models.CharField ( u"键说明", max_length = 100, null = True, blank = True )
    value = models.CharField ( u"值", max_length = 100 )

    objects = ConfigManager ()

    def __unicode__ ( self ):
        return self.help_text or self.key

