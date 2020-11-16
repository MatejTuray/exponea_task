from logger import log
import requests
from functools import wraps


def error_interface(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except requests.exceptions.RequestException as e:
            log.error(f"Handled request error while processing request: {e}")
            return e

        except Exception as e:
            log.error(f"Handled unspecified error while processing request: {e}")
            return e

    return decorated
