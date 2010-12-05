from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.db import models
from ittybitty.utils import gen_shortcut
from shorturls.baseconv import base62
from datetime import datetime
from urllib import urlopen
import re
from chardet import detect
try:
    SITE = Site.objects.get_current()
except:
    SITE = None


def get_url_title ( url ):
    try:
        handler = urlopen ( url )
        c = handler.read ()
        handler.close ()
        titles = re.findall ( r"<title>(.+?)</title>", c )

        if len ( titles ) == 0:
            title = ""
        else:
            title = titles [0]
    except:
        title = ""

    return title

class IttyBittyURL(models.Model):
    """
    The Itty Bitty URL model that is responsible for matching shortcuts up with
    a real URL.
    """
    user = models.ForeignKey ( User, blank = True, null = True )
    shortcut = models.CharField(max_length=10, blank=True, unique=True)
    url = models.URLField(unique=True)
    title = models.CharField ( max_length = 255, default = "" )
    hits = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url

    def get_shortcut(self):
        return 'http://%s/%s' % (SITE.domain, self.shortcut)

    class Meta:
        ordering = ('-date_created', 'shortcut')
        verbose_name = 'Itty Bitty URL'
        verbose_name_plural = 'Itty Bitty URLs'

class URLWhiteList ( models.Model ):
    url = models.URLField ( unique = True )

    def __unicode__ ( self ):
        return self.url

def set_shortcut(sender, instance, created, *args, **kwargs):
    """
    Generates the shortcut for an Itty Bitty URL object if it hasn't already
    been generated.
    """
    m = False
    if not instance.shortcut:
        # instance.shortcut = gen_shortcut(instance.id)
        instance.shortcut = base62.from_decimal ( 100000 + instance.id )
        instance.save ()
        m = True

    if not instance.title:
        title = get_url_title ( instance.url )
        code = detect ( title )
        title = title.decode ( code['encoding'] )
        instance.title = title# get_url_title ( instance.url )
        m = True

    if m:
        instance.save ()

    return instance
    
models.signals.post_save.connect(set_shortcut, sender=IttyBittyURL)
