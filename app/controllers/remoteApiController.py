import requests
from interfaces.errorInterface import error_interface
from logger import logRoundtrip


class RemoteApiController:
    def __init__(self, url, timeout):
        super().__init__()
        self.timeout = timeout
        self.url = url

    @error_interface
    def get(self):
        with requests.Session() as session:
            session.hooks["response"].append(logRoundtrip)
            resp = session.get(url=self.url, timeout=self.timeout)
            resp.raise_for_status()
            if resp.status_code == 200:
                data = resp.json()
                return data
