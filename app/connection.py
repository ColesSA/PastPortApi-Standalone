"""Interface to PastPortGPS, the web-based location services for the barge

Returns:
    tuple -- coordinates of the glass barge
"""


import logging
import time
from logging.handlers import SMTPHandler

import requests
from bs4 import BeautifulSoup
from flask.logging import default_handler
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.config import Config

WEB=Config.WEB
CONN=Config.CONNECTION
ERR=Config.ERR

Retry.BACKOFF_MAX = CONN['BACKOFF_MAX']

smtp_handler = SMTPHandler(
    mailhost=ERR['MAIL_HOST'],
    fromaddr=ERR['FROM_ADDR'],
    toaddrs=ERR['TO_ADDRS'],
    subject=ERR['SUBJECT_DEFAULT'])
smtp_handler.setLevel(logging.ERROR)

LOGGER = logging.getLogger('smtp')
LOGGER.addHandler(smtp_handler)

DEBUGGER = logging.getLogger('debug')

def requests_retry_session(session=None):
    session = session or requests.Session()
    __max = CONN['MAX_RETRIES']
    retry = Retry(
        total=__max,
        read=__max,
        connect=__max,
        backoff_factor=CONN['BACKOFF_FACTOR'],
        status_forcelist=CONN['STATUS_FORCELIST'],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_secure_coords():
    t0 = time.time()
    try:
        DEBUGGER.debug(' * Getting Coordinates')
        s = requests.Session()
        s.auth = (WEB['UID'],WEB['PWD'])
        req = requests_retry_session(session=s).get(WEB['URL'], verify=False)
        req.raise_for_status()
    except Exception as x:
        LOGGER.exception('Connection failed, {}'.format(x))
        return None
    else:
        soup = BeautifulSoup(req.content, 'html.parser').find('div', {'id': 'latlong'})
        coords = (soup['data-latitude'],soup['data-longitude'])
        DEBUGGER.debug('Connection Successful, {}'.format(req.status_code))
        return coords
    finally:
        t1 = time.time()
        DEBUGGER.debug('Took {} seconds'.format(t1-t0))
