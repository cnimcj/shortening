# -*- encoding:utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q, Sum
from django.core import serializers
from statistics.models import Day
from cuser.models import Reward
import datetime
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string

# FIXME 具体什么时候结算
# FIXME 计算通过下线获得的收入
@login_required
def statistics_read ( request ):
    month = request.GET.get ( "month", None )
    if not month:
        month = datetime.date.today ().month 
    
    NEWBIE_REWARD = getattr ( settings, "NEWBIE_REWARD", 0 )
    RECOMMENDER_REWARD = getattr ( settings, "RECOMMENDER_REWARD", 0 )
    try:
        newbie_reward = Reward.objects.get ( Q ( user = request.user ), Q ( referrer = None ) )
    except Reward.DoesNotExist:
        newbie_reward = None
    recommender_reward = Reward.objects.filter ( referrer = request.user )
    recommender_rewards = len ( recommender_reward )
    objects = Day.objects.filter ( user = request.user )
    total = objects.filter ( create_at__month = month ).aggregate ( Sum ( 'hits' ) )['hits__sum'] or 0
    context_dict = {
        "archives" : objects.dates ( 'create_at', 'month' ),
        "total" : total,
        "recommender_reward" : RECOMMENDER_REWARD * recommender_rewards,
        "newbie_reward" : newbie_reward and NEWBIE_REWARD or 0,
    }
    return render_to_response (
            "read.html",
            context_dict,
            context_instance = RequestContext ( request ),
    )

def statistics_xml_read ( request ):
    request.user = authenticate ( username = "cj", password = "111"  )
    objects = Day.objects.filter ( user = request.user )
    data = serializers.serialize ( "xml", objects )
    return HttpResponse ( data, mimetype="text/xml" )
