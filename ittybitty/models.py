from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.db import models
from ittybitty.utils import gen_shortcut
from shorturls.baseconv import base62
from datetime import datetime
try:
    SITE = Site.objects.get_current()
except:
    SITE = None

class IttyBittyURL(models.Model):
    """
    The Itty Bitty URL model that is responsible for matching shortcuts up with
    a real URL.
    """
    user = models.ForeignKey ( User, blank = True, null = True )
    shortcut = models.CharField(max_length=10, blank=True, unique=True)
    url = models.URLField(unique=True)
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

def set_shortcut(sender, instance, created, *args, **kwargs):
    """
    Generates the shortcut for an Itty Bitty URL object if it hasn't already
    been generated.
    """
    if not instance.shortcut:
        # instance.shortcut = gen_shortcut(instance.id)
        instance.shortcut = base62.from_decimal ( 100000 + instance.id )
        instance.save()
    return instance
    
models.signals.post_save.connect(set_shortcut, sender=IttyBittyURL)

class VisitStatistics ( models.Model ):
    user = models.ForeignKey ( User, blank = True, null = True )
    count = models.IntegerField ( default = 0 )
    create_at = models.DateTimeField(auto_now_add=True)
    
    # def save ( self, *args, **kwargs ):
    #     self.count += 1
    #     super ( IPStatistics, self).save ( *args, **kwargs )

class IPStatistics ( models.Model ):
    ip = models.IPAddressField ()
    url = models.ForeignKey ( IttyBittyURL )
    
    def save ( self, *args, **kwargs ):
        super ( IPStatistics, self).save ( *args, **kwargs )
        bitty_url = self.url
        if bitty_url.user:
            try:
                visit =  VisitStatistics.objects.get (
                    create_at = datetime.now ().date (),
                    user = bitty_url.user )
            except VisitStatistics.DoesNotExist:
                visit =  VisitStatistics (
                    create_at = datetime.now ().date (),
                    user = bitty_url.user )

            visit.count += 1
            visit.save ()
        bitty_url.hits += 1
        bitty_url.save ()