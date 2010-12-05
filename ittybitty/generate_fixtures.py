#!/usr/bin/env python
import random
import simplejson
import calendar
from datetime import datetime

def generate_numeric ():
    numeric = int ( random.random () * 255 )
    return numeric

def generate_ip ():
    return "%s.%s.%s.%s" % ( generate_numeric (), generate_numeric (), generate_numeric (), generate_numeric () )

def generate_ip_models ():
    data = []

    d1 = datetime ( year = 2010, month = 1, day = 1 )
    d2 = datetime ( year = 2010, month = 2, day = 1 )
    
    i = 1
    for month in range ( 1, 2 ):
        m = calendar.monthrange ( 2010, month )

        for day in range ( 1, m[1] + 1 ):
            now_date = "2010-%s-%s 16:00:00" % ( month, day )
            for count in range ( 1, int ( random.random () * 999 ) ):
                ip_models = {
                    'pk' : i,
                    "model" : "statistics.ip",
                    "fields" : {
                        "user" : 1,
                        "url" : 1,
                        "ip" : generate_ip (),
                        "create_at" : now_date
                    }
                }

#                day_models = {
#                    "pk" : i,
#                    "model" : "statistics.day",
#                    "fields" : {
#                        "user" : 1,
#                        "hit" : 1,
#                        "ip" : i,
#                        "create_at" : now_date
#                    }
#                }
                i += 1
                data.append ( ip_models )
# data.append ( visit_models )

    return simplejson.dumps ( data )

data = generate_ip_models ()
print ( data )
# f = file ( "statistics/fixtures/initial_data.json", "w+" )
# f.write ( data )
# f.close ()
