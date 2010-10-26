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
>>> import simplejson
>>> c = Client ()
>>> c.login ( username = 'admin', password = '111' )
True
>>> r = c.post ( '/shortening/create/', { 'raw_url' : 'http://www.qq.com' } )
>>> j = simplejson.loads ( r.content )
>>> j['result']
'0Av'

* read
>>> r = c.get ( '/0Av' )
>>> url = r.context ['url']
>>> r.template.name
'ittybitty/read.html'
>>> url.url
u'http://www.qq.com'
>>> from ittybitty.models import VisitStatistics, IPStatistics
>>> from datetime import datetime
>>> ips = IPStatistics.objects.get ( url = url )
>>> ips.ip
u'127.0.0.1'
>>> vs = VisitStatistics.objects.get ( user__id = 1 )
>>> vs.count
1
"""}