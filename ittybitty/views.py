from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q
from models import IttyBittyURL, IPStatistics, VisitStatistics
from utils import completion_protocol
import simplejson
from datetime import datetime

# TODO Shortening service
def shortening_create ( request ):
    result = {}
    bitty_url = None
    if "POST" == request.method:
        raw_url = request.POST.get ( 'raw_url', '' )
        raw_url = completion_protocol ( raw_url )
        try:
            bitty_url = IttyBittyURL.objects.get ( url = raw_url )
        except IttyBittyURL.DoesNotExist:
            bitty_url = IttyBittyURL ( url = raw_url )
            
            if ( request.user.is_authenticated () ):
                bitty_url.user = request.user
            bitty_url.save ()
        
        result['result'] = not bitty_url == None and bitty_url.shortcut
    return HttpResponse ( simplejson.dumps ( result ) )

# FIXME Refactoring models move business to domain business
def shortening_read ( request, shortening ):
    bitty_url = get_object_or_404 ( IttyBittyURL, shortcut = shortening )
    try:
        ip = IPStatistics.objects.get ( url = bitty_url )
    except IPStatistics.DoesNotExist:
        IPStatistics ( url = bitty_url, ip = request.META['REMOTE_ADDR'] ).save ()
        
    return render_to_response (
        'ittybitty/read.html',
        { 'url' : bitty_url },
    )