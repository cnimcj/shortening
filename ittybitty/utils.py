import re

VALID = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-0123456789'

def gen_shortcut(num):
    """
    Generates a short URL for any URL on your Django site.  It is intended to
    make long URLs short, a la TinyURL.com.

    Thanks to Jonathan Geddes for the help with this one.
    """
    short = ''
    while num != 0:
        num, remainder = divmod(num - 1, len(VALID))
        short += VALID[remainder]
    return short
    
def completion_protocol ( raw_url ):
    pattern = r'http://'
    search_result = re.compile ( pattern, re.I ).search ( raw_url )
    if not search_result:
        return 'http://' + raw_url
    return raw_url