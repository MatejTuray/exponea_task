from controllers.communicationsController import CommunicationController
from fastapi import Depends, Request
from fastapi_restful import set_responses
from interfaces.taskInterface import add_runner
from logger import log, log_request
from parsers.output.time_parser import TimeOutSingle
from stopit import ThreadingTimeout, TimeoutException
from utils.convert_from_ms import convert_from_ms
from utils.enums import SourceTypes, TaskTypes, URLList
from utils.response_models import TimeoutErrorModel, timeout_error

from resources.base import BaseResource


class SmartResponseResource(BaseResource):
    @log_request()
    @add_runner(SourceTypes.EXPONEA, TaskTypes.SMART)
    @set_responses(
        TimeOutSingle,
        200,
        {504: {"description": "Timeout Error", "model": TimeoutErrorModel}},
        summary="Repeats after failure",
        description="Endpoint fires single request to Exponea testing server, returns response on success, does subsequent requests on failure",
    )
    def get(self, request: Request, timeout: float = Depends(convert_from_ms)):
        with ThreadingTimeout(timeout) as ctx_timeout:
            exponea_test_cntrl_first = CommunicationController(
                url=URLList.EXPONEA_TEST_SERVER.value, timeout=0.3
            )
            exponea_test_cntrl_subsequent = CommunicationController(
                url=URLList.EXPONEA_TEST_SERVER.value, timeout=timeout
            )
            smart_runner = self.runners[0]
            smart_runner.push_task(exponea_test_cntrl_first.get, [None], 1)

            try:
                res = smart_runner.schedule_tasks(1, 0.3)
            except TimeoutException as e:
                log.info(e)
                smart_runner.push_task(
                    exponea_test_cntrl_subsequent.get, [None], 2
                )
                print(len(smart_runner.tasks))
                res = smart_runner.schedule_tasks(2, timeout)
        if ctx_timeout.state == ctx_timeout.TIMED_OUT:
            return timeout_error
        elif ctx_timeout.state == ctx_timeout.EXECUTED:
            if not res:
                return timeout_error
            return res

