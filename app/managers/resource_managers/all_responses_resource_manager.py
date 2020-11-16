from stopit import ThreadingTimeout
from utils.response_models import timeout_error


class ResponseHelper:
    
    def __init__(self, runners=[], controllers=[]):
        self.runners = runners
        self.controllers = controllers
    
    @staticmethod
    def base_schedule(timeout, runners, controllers):
        with ThreadingTimeout(timeout) as ctx_timeout:
            cntrl = controllers[0]
            runner = runners[0]
            runner.push_task(cntrl.get, [None], 3)
            res = runner.schedule_tasks(3, timeout)
            return ctx_timeout, res     


class AllResponsesResourceManager(ResponseHelper):    
    
    def handle_get(self, timeout, runners, controllers):
        ctx_timeout, res = self.base_schedule(timeout, runners, controllers)                     
        if ctx_timeout.state == ctx_timeout.TIMED_OUT:
            return timeout_error
        elif ctx_timeout.state == ctx_timeout.EXECUTED:
            if not res:
                return timeout_error
            return [item for item in res if type(item) == dict]
      
