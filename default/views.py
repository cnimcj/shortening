from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User, AnonymousUser
from ittybitty.models import IttyBittyURL

def read ( request ):
    if not isinstance ( request.user, AnonymousUser):
        urls = IttyBittyURL.objects.filter ( user = request.user ).order_by ( "-date_created" )
    else:
        urls = None

    id = request.GET.get ( "id", None )
    if id:
        shortening = IttyBittyURL.objects.get ( shortcut = id )
    else:
        shortening = None
    return render_to_response (
        "default/read.html",
        {
            "urls" : urls,
            "shortening" : shortening,
        },
        context_instance = RequestContext ( request ),
    )
