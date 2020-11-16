from stopit import ThreadingTimeout
from utils.response_models import timeout_error
from managers.resource_managers.all_responses_resource_manager import ResponseHelper
from logger import log


class FirstResponseResourceManager(ResponseHelper):
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
                if not res:
                    return timeout_error
                return res
