from django.db import models
from django.db.models.signals import post_save
from datetime import datetime
from django.contrib.auth.models import User
from ittybitty.models import IttyBittyURL
from cuser.models import Reward
import datetime

class IP ( models.Model ):
    user  = models.ForeignKey ( User, blank = True, null = True )
    ip = models.IPAddressField ()
    url = models.ForeignKey ( IttyBittyURL )
    create_at = models.DateTimeField ( auto_now_add = True )

    class Meta:
        unique_together = ( ( 'ip', 'url' ), )

class Day ( models.Model ):
    user  = models.ForeignKey ( User, blank = True, null = True )
    create_at = models.DateTimeField ( )
    hits = models.IntegerField ( default = 0 )

    def save ( self, *args, **kwargs ):
        self.hits += 1
        super ( Day, self ).save ( *args, **kwargs )


def post_save_ip ( sender, instance, created = None, **kwargs ):
    if instance.user:
        profile = instance.user.get_profile () 
        profile.hits += 1
        profile.save ()

        if profile.referrer and profile.hits == 100:
            newbie_reward = Reward ( user = instance.user )
            newbie_reward.save ()
            recommender_reward = Reward ( user = instance.user, referrer = profile.referrer )
            recommender_reward.save ()
        try:
            day = Day.objects.get ( create_at = instance.create_at.date () )
        except Day.DoesNotExist:
            day = Day ( user = instance.user )
            day.create_at = instance.create_at.date ()
        day.save ()


post_save.connect ( post_save_ip, sender = IP )

class Visit ( models.Model ):
    user  = models.ForeignKey ( User, blank = True, null = True )
    url   = models.ForeignKey ( IttyBittyURL )
    ip    = models.ForeignKey ( IP )
    create_at = models.DateTimeField(auto_now_add=True)
    

