import logging

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.config import Config
import app

import time

Retry.BACKOFF_MAX = Config.BACKOFF_MAX

TIME_DIFF = 0

def requests_retry_session(
    retries=2,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_secure_coords():
    t0 = time.time()
    try:
        logging.debug(' * Getting Coordinates')
        s = requests.Session()
        s.auth = (Config.WEB_UID,Config.WEB_PWD)
        req = requests_retry_session(session=s).get(Config.URL, verify=False)
    except Exception as x:
        logging.error('Connection failed, {}'.format(x.__class__.__name__))
        return None
    else:
        try:
            soup = BeautifulSoup(req.content, 'html.parser').find('div', {'id': 'latlong'})
            coords = (soup['data-latitude'],soup['data-longitude'])
        except Exception as e:
            logging.error('Connection Failed, {}'.format(req.status_code))
            return None
        else:
            logging.debug('Connection Successful, {}'.format(req.status_code))
            return coords
    finally:
        t1 = time.time()
        TIME_DIFF = t1-t0
        logging.debug('Took {} seconds'.format(TIME_DIFF))
    


