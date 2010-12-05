from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from cuser.forms import UserCreationForm, AuthenticationForm, ProfileChangeForm, PasswordChangeForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

setattr ( settings, "LOGIN_URL", "/user/auth/create/" )

def user_create ( request ):
    if "POST" == request.method:
        form = UserCreationForm ( request.POST )
        if form.is_valid ():
            form.save ()
            return HttpResponseRedirect ( "/" )
    else:
#        recommender = request.GET.get ( "recommender", None )
#        invite = request.GET.get ( "
        form = UserCreationForm ( request.GET )

    context = {\
        "form" : form
    }
    return render_to_response (
        "create.html",
        context
    )

@login_required
def user_update ( request ):
    if "POST" == request.method:
        profile_form = ProfileChangeForm ( request.POST, instance = request.user )
        password_form = PasswordChangeForm ( request.user, request.POST )
        
        email_has_changed = False
        if profile_form.is_valid ()\
            and "email" in profile_form.changed_data:
            profile_form.save ()
            email_has_changed = True
        
        if password_form.is_valid ():
            password_form.save ()

        if email_has_changed\
            or password_form.is_valid ():
            return HttpResponseRedirect ( "/" )
    else:
        profile_form  = ProfileChangeForm  ( instance = request.user )
        password_form = PasswordChangeForm ( request.user )
    
    context = {\
        "profile_form" : profile_form,
        "password_form" : password_form,
    }
    return render_to_response (
        "update.html",
        context
    )

def auth_create ( request ):
    if "POST" == request.method:
        form = AuthenticationForm ( request, data = request.POST )
        if form.is_valid ():
            login ( request, form.get_user () )
            return HttpResponseRedirect ( "/" )
    else:
        form = AuthenticationForm ()
    request.session.set_test_cookie ()
    context = {\
        "form" : form
    }
    return render_to_response (
        "auth/create.html",
        context
    )

def auth_delete ( request ):
    logout ( request )
    return HttpResponseRedirect ( "/" )

def upgrade_create ( request ):
    pass
