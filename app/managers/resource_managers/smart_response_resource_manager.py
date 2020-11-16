from stopit import ThreadingTimeout, TimeoutException
from logger import log
from utils.response_models import timeout_error


class SmartResponseResourceManager:
    @staticmethod
    def handle_get(timeout, runners, controllers):
        with ThreadingTimeout(timeout) as ctx_timeout:
            cntrl_first = controllers[0]
            cntrl_subsequent = controllers[1]
            runner = runners[0]
            runner.push_task(cntrl_first.get, [None], 1)
            try:
                res = runner.schedule_tasks(1, 0.3)
            except TimeoutException as e:
                log.info(e)
                runner.push_task(cntrl_subsequent.get, [None], 2)
                res = runner.schedule_tasks(2, timeout)
        if ctx_timeout.state == ctx_timeout.TIMED_OUT:
            return timeout_error
        elif ctx_timeout.state == ctx_timeout.EXECUTED:
            if not res:
                return timeout_error
            return res
