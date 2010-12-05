#! -*- encoding:utf-8 -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
>>> from django.test.client import Client
>>> from django.contrib.auth.models import User
>>> from models import Invite
>>> Invite.objects.make_100 ( 10 )
>>> Invite.objects.all ().count ()
10
>>> invite = Invite.objects.get ( pk = 1 )
>>> client = Client ()
>>> USER_CREATE = "/user/create/"
>>> USER_UPDATE = "/user/update/"
>>> AUTH_CREATE = "/user/auth/create/"
>>> AUTH_DELETE = "/user/auth/delete/"

开始测试

>>> user_data = {\
        "username" : "user1",\
        "password1" : "pass",\
        "password2" : "pass",\
        "invite" : invite.code,\
        "recommender" : "", }
>>> response = client.post ( USER_CREATE, user_data )
>>> response.status_code
302
>>> user = User.objects.get ( username = "user1" )
>>> user
<User: user1>
>>> user_data['recommender'] = 'user100'
>>> user_data['username'] = 'user3'
>>> response = client.post ( USER_CREATE, user_data )
>>> response.context['form'].errors.has_key ( 'recommender' )
True
>>> client.logout ()

登陆

>>> response = client.post ( AUTH_CREATE, { \
        "username" : "user1",\
        "password" : "pass",\
    } )
>>> response.status_code
200

用户资料修改
>>> client.login ( username = 'user1', password = 'pass' )
True
>>> response = client.post ( USER_UPDATE, {\
        "new_password1" : "newpass",\
        "new_password2" : "newpass",\
        "old_password" : "pass",\
        "email" : "cn.imcj@gmail.com" }, follow = True )
>>> response.status_code
200
>>> response.redirect_chain
[('http://testserver/', 302)]
>>> user = User.objects.get ( username = "user1" )
>>> user.email
u"cn.imcj@gmail.com"
>>> client.login ( username = "user1", password = "pass" )
False



"""}

