from stopit import ThreadingTimeout
from utils.response_models import timeout_error
from logger import log


class ResponseHelper:
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
        try:
            ctx_timeout, res = self.base_schedule(timeout, runners, controllers)
        except Exception as e:
            log.error(e)
            return timeout_error
        else:
            if ctx_timeout.state == ctx_timeout.TIMED_OUT:
                return timeout_error
            elif ctx_timeout.state == ctx_timeout.EXECUTED:
                valid = [item for item in res if type(item) == dict]
                if not valid:
                    return timeout_error
                return valid
