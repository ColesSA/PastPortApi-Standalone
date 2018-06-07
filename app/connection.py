import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.config import Config
import logging
import requests
from bs4 import BeautifulSoup

"""Retry.BACKOFF_MAX = Config.BACKOFF_MAX

def requests_retry_session(
    retries=3,
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

t0 = time.time()
try:
    response = requests_retry_session().get(
        'http://localhost:9999',
    )
except Exception as x:
    print('It failed :(', x.__class__.__name__)
else:
    print('It eventually worked', response.status_code)
finally:
    t1 = time.time()
    print('Took', t1 - t0, 'seconds')

"""

def get_coords():
    logging.debug(' * Getting Coordinates')
    with requests.get(Config.URL,verify=False, auth=(Config.WEB_UID, Config.WEB_PWD)) as req:
        soup = BeautifulSoup(req.content, 'html.parser').find('div', {'id': 'latlong'})
        return {'latitude':soup['data-latitude'],'longitude':soup['data-longitude']}

#requests.put('127.0.0.1:5000/api/now', data=get_coords()).json()