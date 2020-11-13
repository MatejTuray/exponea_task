import abc
import requests
from app.interfaces.errorInterface import error_interface

class AbstractRequestController(abc.ABCMeta):
    @abc.abstractstaticmethod
    def query(method, url, timeout, data):
        raise NotImplementedError


class CommunicationController:
    def __init__(self, url, timeout):
        super().__init__()
        self.timeout = timeout
        self.url = url

    @error_interface
    def get(self):
        resp = requests.get(url=url, timeout=self.timeout)
        resp.raise_for_status()
        if resp.status_code == 200:
            data = resp.json()
            return data
