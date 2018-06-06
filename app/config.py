"""Opens private config values as class"""

import json
import logging
import sys

import urllib3

if sys.version_info[0] < 3:
    from urllib import quote_plus
else:
    from urllib.parse import quote_plus

urllib3.disable_warnings()

class Config(object):
    with open("./config.json", 'r') as stream:
        __vars = json.load(stream)

    ENV=None
    DEBUG=True
    TESTING=False
    LOGGING=True
    URL=__vars['URL']
    DRIVER=__vars['DRIVER']
    SERVER=__vars['SERVER']
    DATABASE=__vars['DB']
    DB_UID=__vars['DB_UID']
    DB_PWD=__vars['DB_PWD']
    WEB_UID=__vars['WEB_UID']
    WEB_PWD=__vars['WEB_PWD']
    RESTFUL_JSON = {'separators': (', ', ': '),
                    'indent': 2}

    __quote = quote_plus('DRIVER='+DRIVER+
            ';SERVER='+SERVER+';DATABASE='+DATABASE+
            ';UID='+DB_UID+';PWD='+DB_PWD)
    DB_URI = 'mssql+pyodbc:///?odbc_connect=%s' % __quote

    if(LOGGING):
        logging.basicConfig(level=logging.DEBUG,
            format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                )
        

        
