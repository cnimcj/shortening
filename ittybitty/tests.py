#! -*- encoding: utf-8 -*-

__test__ = { 'doctest' : """
Completion url

>>> from util import completion_protocol
>>> completion_protocol ( 'qq.com' )
'http://qq.com'

Test views
 * create
 * read

* create
>>> from django.test.client import Client
>>> from django.contrib.auth.models import User
>>> import simplejson
>>> user = User ( username = "admin" )
>>> user.set_password ( '111' )
>>> user.save ()
>>> c = Client ()
>>> c.login ( username = 'admin', password = '111' )
True
>>> first_shortening = second_shortening = thirdly_shortening = {}
>>> r = c.post ( '/shortening/create/', { 'raw_url' : 'http://www.baidu.com' } )
>>> j = simplejson.loads ( r.content )
>>> first_shortening = j
>>> first_shortening['shortening']
'0Av'
>>> r = c.post ( '/shortening/create/', { 'raw_url' : 'http://www.qq.com' } )
>>> j = simplejson.loads ( r.content )
>>> second_shortening = j
>>> second_shortening['shortening']
'0Aw'
>>> len ( second_shortening['date'] )
10

* read
>>> r = c.get ( '/0Av' )
>>> url = r.context ['url']
>>> r.template.name
'ittybitty/read.html'
>>> url.url
u'http://www.baidu.com'
>>> from statistics.models import Day, IP
>>> from datetime import datetime
>>> ips = IP.objects.get ( url = url )
>>> ips.ip
u'127.0.0.1'
>>> day = Day.objects.get ( pk = 1 )
>>> day.hits
1
"""}
