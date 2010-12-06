# -*- encoding:utf-8 -*-
from django.db import models

class ConfigManager ( models.Manager ):
    def str ( self, key ):
        return unicode ( self.get ( key ) )

    def int ( self, key ):
        return int ( self.get ( key ) )

    def get ( self, key ):
        return super ( ConfigManager, self ).get_query_set ().get ( key = key ).value

class Config ( models.Model ):
    """
    >>> config = Config ( key = u"设置", help_text = u"设置", value = "内容" )
    >>> config.save ()
    >>> Config.keys.get ( u"设置" )
    u'\u5185\u5bb9'
    >>> Config.keys.int ( u"设置" )
    Traceback (most recent call last):
    ...
    UnicodeEncodeError: 'decimal' codec can't encode character ... in position 0: invalid decimal Unicode string
    >>> isinstance ( Config.keys.str ( u"设置" ), unicode )
    True
    """
    key = models.CharField ( u"键", max_length = 100, unique = True )
    help_text = models.CharField ( u"键说明", max_length = 100, null = True, blank = True )
    value = models.CharField ( u"值", max_length = 100 )

    keys = ConfigManager ()

    def __unicode__ ( self ):
        return self.help_text or self.key

    class Meta:
        verbose_name = u"配置"
        verbose_name_plural = u"配置"
#db_table = u"conf_config"
#        app_label = u"系统"

