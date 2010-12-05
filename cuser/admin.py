#! -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.template import RequestContext
from models import GroupProfile, Invite
from forms import InviteForm

class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ('group', 'income')
    # list_display_links = ('shortcut', 'url')
    # search_fields = ('shortcut', 'url')
    # list_filter = ('date_created', 'date_updated')
    # date_hierarchy = 'date_created'

class InviteAdmin ( admin.ModelAdmin ):
    list_display = ( 'code', 'used', )
    list_filter = ( 'used', )
    
    make_100_template = "admin/cuser/make_100.html"

    def make_100 ( self, request ):
        if "POST" == request.method:
            form = InviteForm ( request.POST )
            if form.is_valid ():
                form.save ()
                messages.success ( request, u"成功生成%s个邀请码。" % form.cleaned_data['number'] )
                return HttpResponseRedirect ( ".." )
        else:
            form = InviteForm ()
        return render_to_response ( self.make_100_template,
            {
                "form" : form,
                "opts" : self.model._meta,
            },
            context_instance = RequestContext ( request )
        )
        queryset.make_100 ()
        self.message_user ( request, u"邀请码生成完成。" )
    make_100.short_description = u"生成100个邀请码"

    actions = [ ]

    def get_urls ( self ):
        from django.conf.urls.defaults import patterns, url
        return patterns ( '',
            url ( r'^make_100/$', self.admin_site.admin_view ( self.make_100 ), name = "make_100" ),
        ) + super ( InviteAdmin, self ).get_urls ()


UserAdmin.list_filter = ('is_staff', 'is_superuser' )

admin.site.unregister ( User )
admin.site.register ( User, UserAdmin )
admin.site.register(GroupProfile, GroupProfileAdmin)
admin.site.register ( Invite, InviteAdmin )
