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

__conn=Config.CONNECTION
__err=Config.ERR

smtp_handler = SMTPHandler(
    mailhost=__err['MAIL_HOST'],
    fromaddr=__err['FROM_ADDR'],
    toaddrs=__err['TO_ADDRS'],
    subject=__err['SUBJECT_DEFAULT'])
smtp_handler.setLevel(logging.ERROR)

Logger = logging.getLogger('smtp')
Logger.addHandler(smtp_handler)

Debugger = logging.getLogger('debug')

def requests_retry_session(session=None):
    session = session or requests.Session()
    __max = __conn['MAX_RETRIES']
    retry = Retry(
        total=__max,
        read=__max,
        connect=__max,
        backoff_factor=__conn['BACKOFF_FACTOR'],
        status_forcelist=__conn['STATUS_FORCELIST'],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def safe_session(url, uid, pwd):
    s = requests.Session()
    s.auth = (uid, pwd)
    req = requests_retry_session(session=s).get(url, verify=False)
    return req

def get_coords(url, uid, pwd):
    t0 = time.time()
    try:
        Debugger.debug('Fetching Coordinates')
        req = safe_session(url, uid, pwd)
        req.raise_for_status()
    except Exception as x:
        Logger.exception('Connection failed, {}'.format(x))
    else:
        Debugger.debug('Connection Successful, {}'.format(req.status_code))
        soup = BeautifulSoup(req.content, 'html.parser').find('div', {'id': 'latlong'})
        coords = (soup['data-latitude'],soup['data-longitude'])
        return coords
    finally:
        t1 = time.time()
        Debugger.debug('Took {} seconds'.format(t1-t0))
