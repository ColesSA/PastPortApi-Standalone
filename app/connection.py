"""Provides a safe and descriptive wrapper around requests to aid in error handling and the patchy connection to the barge."""


import logging
import time

import requests
from bs4 import BeautifulSoup
from flask.logging import default_handler
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import app

Debugger = logging.getLogger('debug')

class SafeSession(object):
    """Wrapper class around a requests session that integrates error handling and effective retries."""

    def __init__(self, max_retries=3, backoff_factor=.5, status_forcelist=[500,503,504]):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist

    def requests_retry_session(self, session=None):
        """Wrapper around session that handles retries.
        
        Keyword Arguments:
            session {Requests session} -- (default: {None})
        
        Returns:
            Requests session 
        """
        session = session or requests.Session()
        
        retry = Retry(
            total=self.max_retries,
            read=self.max_retries,
            connect=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def set_security_info(self, uid, pwd, verify):
        """Sets the connection information for the requests sessions.
        
        Arguments:
            uid {str} -- Username for SSL Login
            pwd {str} -- Password for SSL Login
            verify {bool, or str} --  
                'False': Unsecured connection 
                'path to certification files': safe connection.
        """     
        self.auth = (uid,pwd)
        self.verify = verify

    def get(self, url):
        """Wrapper around requests 'get' function.
        
        Arguments:
            url {str} -- URL to send GET request to.
        
        Returns:
            requests Response object -- The 'GET' response.
        """
        t0 = time.time()
        s = requests.Session()
        s.auth = self.auth
        Debugger.debug('Establishing Connection')
        try:
            req = self.requests_retry_session(session=s).get(url, verify=self.verify)
            req.raise_for_status()
        except Exception as x:
            app.logger.exception('Connection failed, {}'.format(x))
        else:
            Debugger.debug('Connection Successful, {}'.format(req.status_code))
            return req
        finally:
            t1 = time.time()
            Debugger.debug('Took {} seconds'.format(t1-t0))


def get_coords(url):
    """Get the coordinates of the barge's current location
    
    Arguments:
        url {str} -- URL of the PastPortGPS router interface.
    
    Returns:
        tuple -- (float:latitude,float:longitude)
    """

    request = app.sess.get(url)
    soup = BeautifulSoup(request.content, 'html.parser').find('div', {'id': 'latlong'})
    coords = (soup['data-latitude'],soup['data-longitude'])
    return coords
