"""Provides a safe and descriptive wrapper around requests to aid in error handling and the patchy connection to the barge."""


import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api.logger import time_function
from api.models import Location

class SafeSession(object):
    """Wrapper class around a requests session that integrates error handling and effective retries.

        Arguments:
            uid {str} -- Username for SSL Login
            pwd {str} -- Password for SSL Login
            verify {bool, or str} --  
                'False': Unsecured connection 
                'path to certification files': safe connection.
        
        Keyword Arguments:
            max_retries {int} -- Number of retries on failed connection type defined by status_forcelist (default: {3})
            backoff_factor {float} -- {backoff factor} * (2 ^ ({number of total retries} - 1)) (default: {.5})
            status_forcelist {[type]} -- List of status codes to retry connection on (default: [500,503,504])"""

    def __init__(self, uid, pwd, verify, max_retries=3, backoff_factor=.5, status_forcelist=None):
        self.auth = (uid,pwd)
        self.verify = verify
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.status_forcelist =  status_forcelist or [500,503,504]

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

    def current_location(self, url, to_database=True):
        """Uses safe session to store the current location of the barge to a database.
        
        Arguments:
            url {str} -- URL of the PastPortGPS router interface.

        Returns:
            Location -- Instance of Location object representing current barge location.
        """
        _to_db = to_database
        _t0 = time.time()
        _s = requests.Session()
        _s.auth = self.auth
        logging.debug('Establishing Connection')
        try:
            req = self.requests_retry_session(session=_s).get(url, verify=self.verify)
            req.raise_for_status()
        except Exception as _x:
            logging.exception('Connection failed, %s', (_x))
        else:
            logging.debug('Connection Successful, %s', (req.status_code))
            return Location.from_request(req, _to_db)
        finally:
            _t1 = time.time()
            logging.debug('Took %d seconds', (_t1-_t0))

    @time_function
    def get_from(self, url):
        """Runs a get request to a safe session
        
        Arguments:
            url {str} -- URL to be sent get request

        Returns:
            response {Response} -- Requests response object
        """
        _s = requests.Session()
        _s.auth = self.auth
        logging.debug('Establishing Connection')
        try:
            _req = self.requests_retry_session(session=_s).get(url, verify=self.verify)
            _req.raise_for_status()
        except Exception as _x:
            logging.exception('Connection failed: %s', (_x))
        else:
            logging.debug('Connection Successful: %s', (_req.status_code))
            return _req
