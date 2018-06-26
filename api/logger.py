import logging
import time

def time_function(func):
    """Logs the time a function takes to execute"""
    def wrapper(*args, **kwargs):
        _t0 = time.time()
        _out = func(*args, **kwargs)
        _t1 = time.time()
        logging.debug('Took %d seconds', (_t1-_t0))
        return _out
    return wrapper
