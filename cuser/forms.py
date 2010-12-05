#!/usr/bin/env python
#! -*- encoding:utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import *
from django import forms
from models import Invite

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    invite = forms.CharField ( label = u"邀请码", max_length = 32, help_text = "请输入邀请码，暂时封闭测试" )
    recommender = forms.RegexField(label=u"推荐人", max_length=30, required = False, regex=r'^[\w.@+-]+$',
        help_text = u"Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages = {'invalid': u"This value may contain only letters, numbers and @/./+/-/_ characters."})
    username = forms.RegexField(label=u"用户名", max_length=30, regex=r'^[\w.@+-]+$',
        help_text = u"Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages = {'invalid': u"This value may contain only letters, numbers and @/./+/-/_ characters."})
    password1 = forms.CharField(label=u"密码", widget=forms.PasswordInput)
    password2 = forms.CharField(label=u"重复密码", widget=forms.PasswordInput,
        help_text = u"请保证两次输入密码一致。")

    class Meta:
        model = User
        fields = ("username",)
    
    def clean_invite ( self ):
        invite = self.cleaned_data['invite']
        try:
            obj = Invite.objects.get ( code = invite )
            if obj.used:
                raise forms.ValidationError ( u"邀请码已经使用过了。" )
            else:
                return invite
        except Invite.DoesNotExist:
            raise forms.ValidationError ( u"不存在的邀请码。" )

    def clean_recommender ( self ):
        recommender = self.cleaned_data['recommender']
        try:
            if recommender == "":
                return recommender
            User.objects.get ( username = recommender )
            return recommender
        except User.DoesNotExist:
            raise forms.ValidationError ( u"推荐人不存在。" )

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u"用户名已经被注册了，请重新输入。")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(u"两次密码输入不一致，请检查。")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        invite = self.cleaned_data['invite']
        Invite.objects.filter ( code = invite ).update ( used = True )
        return user
UserCreationForm.base_fields.keyOrder = [ 'invite', 'recommender', 'username', 'password1', 'password2' ]

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(label="用户名", max_length=30)
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u"错误的用户名或者密码。请重新输入。")
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u"没有激活的账号。")

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(u"你的浏览器不支持COOKIE。")

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    new_password1 = forms.CharField(label=u"新密码", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=u"重复新密码", widget=forms.PasswordInput)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u"两次密码输入不一致")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    old_password = forms.CharField(label=u"旧密码", widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(u"旧密码验证错误，请重新输入。")
        return old_password
PasswordChangeForm.base_fields.keyOrder = ['old_password', 'new_password1', 'new_password2']

class ProfileChangeForm ( forms.ModelForm ):
    
    class Meta:
        model = User
        fields = ( "email", )

class InviteForm ( forms.Form ):
    number = forms.IntegerField ( label = u"生成数量" )

    def save ( self ):
        Invite.objects.make_100 ( self.cleaned_data['number'] )
