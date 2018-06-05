"""Opens private config values as class:[], global vars:[X]"""

import json
import logging
import sys

import urllib3

urllib3.disable_warnings()

if sys.version_info[0] < 3:
    from urllib import quote_plus
else:
    from urllib.parse import quote_plus

def get_json():
    """Pulls json data from config.json\n
    Returns:
        Dict -- config values
    """
    with open("./configuration/config.json", 'r') as stream:
        return json.load(stream)

CONFIG = get_json()
SERVER = CONFIG['SERVER']
DB = CONFIG['DB']
URL = CONFIG['URL']
UID = CONFIG['UID']
PWD = CONFIG['PWD']
QUOTE = quote_plus(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='
    +SERVER+';PORT=1433;DATABASE='+DB+';UID='+UID+';PWD='+PWD)
DB_URI = 'mssql+pyodbc:///?odbc_connect=%s' % QUOTE
