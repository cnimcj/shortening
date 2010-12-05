from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q
from models import IttyBittyURL
from statistics.models import Visit, IP
from utils import completion_protocol
from datetime import datetime

import time
import simplejson

# FIXME if create shortening is not contain white list
def shortening_create ( request ):
    result = {
        'shortening' : '',
        'url' : '',
        'date' : '',
    }
    bitty_url = None
    if "POST" == request.method:
#import dtest; dtest.set_trace ()
        raw_url = request.POST.get ( 'raw_url', '' )
        raw_url = completion_protocol ( raw_url )
        try:
            bitty_url = IttyBittyURL.objects.get ( url = raw_url )
        except IttyBittyURL.DoesNotExist:
            bitty_url = IttyBittyURL ( url = raw_url )
            
            if ( request.user.is_authenticated () ):
                bitty_url.user = request.user
            bitty_url.save ()
        result['shortening'] = bitty_url.shortcut
        result['url'] = bitty_url.url
        result['date'] = str ( int ( time.mktime ( bitty_url.date_created.timetuple () ) ) )
        result['title'] = bitty_url.title
#        result['referer'] = 
# result['result'] = not bitty_url == None and bitty_url.shortcut
    return HttpResponse ( simplejson.dumps ( result ) )

# FIXME Refactoring models move business to domain business
def shortening_read ( request, shortening ):
    bitty_url = get_object_or_404 ( IttyBittyURL, shortcut = shortening )
    try:
        ip = IP.objects.get ( Q ( url = bitty_url ), Q ( ip = request.META['REMOTE_ADDR'] ) )
    except IP.DoesNotExist:
        IP ( user = request.user, url = bitty_url, ip = request.META['REMOTE_ADDR'] ).save ()
        
    return render_to_response (
        'ittybitty/read.html',
        { 'url' : bitty_url },
    )
