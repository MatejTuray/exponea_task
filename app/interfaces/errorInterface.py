from logger import log
import requests
from functools import wraps


def error_interface(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except requests.exceptions.RequestException as e:
            log.error(
                "Handled request error while processing request: {0}".format(e)
            )
            raise e

        except Exception as e:
            log.error(
                "Handled unspecified error while processing request: {0}".format(
                    e
                )
            )
            raise e

    return decorated
