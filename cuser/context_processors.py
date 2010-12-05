#!/usr/bin/env python
import pdb
from django.contrib.auth.models import AnonymousUser

def auth ( request ):
    def get_user ( request ):
        if not isinstance ( request.user, AnonymousUser ):
            return request.user
        else:
            return None

    return {
        "user" : get_user ( request )
    }
