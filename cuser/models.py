#! -*- encoding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save


class UserProfile ( models.Model ):
    user = models.ForeignKey ( User, null = True, blank = True, related_name = 'opuser' )
    referrer = models.ForeignKey ( User, null = True, blank = True, related_name = 'rpuser' )
    hits = models.PositiveIntegerField(default=0)

class Reward ( models.Model ):
    REWARD_TYPE = (
        ( u"N", u"新手红包" ),
        ( u"R", u"推荐人奖励" ),
    )

    user = models.ForeignKey ( User, null = True, blank = True, related_name = 'ouser' )
    referrer = models.ForeignKey ( User, null = True, blank = True, related_name = 'ruser' )
    created  = models.DateField ( auto_now_add = True )
# reward_type = models.CharField ( max_length = 2, choices = REWARD_TYPE )

class InviteManager ( models.Manager ):
    def make_code ( self ):
        import md5
        import random
        code = md5.new ( str ( random.random () * 100000 ) ).hexdigest ()[:8]
        return code

    def make_100 ( self, count ):
        for i in range ( count ):
            try:
                invite = self.model ( code = self.make_code (), used= False )
                invite.save ()
            except:
                pass

class Invite ( models.Model ):
    code = models.CharField ( u"注册码", max_length = "6" )
    used = models.BooleanField ( u"使用" )
    objects = InviteManager ()

    class Meta:
        verbose_name = u"邀请码"
        verbose_name_plural = u"邀请码"

    def __unicode__ ( self ):
        return self.code

class GroupProfile ( models.Model ):
    group  = models.ForeignKey ( Group )
    income = models.DecimalField ( u'收益', max_digits = 10, decimal_places = 2 )
    

def user_post_save ( sender, instance, created = None, **kwargs ):
    if created:
        profile = UserProfile ( user = instance )
        profile.save ()

def group_post_save ( sender, instance, created = None, **kwargs ):
    """
    新增分组时初始化收益的数据项
    """
    if created:
        gp = GroupProfile ( income = 0, group = instance )
        gp.save ()

post_save.connect ( user_post_save, sender = User )
post_save.connect ( group_post_save, sender = Group )
