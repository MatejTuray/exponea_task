from controllers.communicationsController import CommunicationController
from fastapi import Depends, Request
from fastapi_restful import set_responses
from interfaces.taskInterface import add_runner
from logger import log_request
from parsers.output.time_parser import TimeOutSingle
from stopit import ThreadingTimeout
from utils.convert_from_ms import convert_from_ms
from utils.enums import SourceTypes, TaskTypes, URLList
from utils.response_models import TimeoutErrorModel, timeout_error

from resources.base import BaseResource


class FirstResponseResource(BaseResource):
    @log_request()
    @add_runner(SourceTypes.EXPONEA, TaskTypes.FIRST_SUCCESSFUL)
    @set_responses(
        TimeOutSingle,
        200,
        {504: {"description": "Timeout Error", "model": TimeoutErrorModel}},
        summary="First successful",
        description="Endpoint returns the first successful response that returns from Exponea testing "
        "HTTP server. If timeout is reached before any successful response was received, the "
        "endpoint should return an error.",
    )
    def get(self, request: Request, timeout: float = Depends(convert_from_ms)):       
        with ThreadingTimeout(timeout) as ctx_timeout:
            exponea_cntrl = CommunicationController(
                url=URLList.EXPONEA_TEST_SERVER.value, timeout=timeout
            )
            runner = self.runners[0]
            runner.push_task(exponea_cntrl.get, [None], 3)
            res = runner.schedule_tasks(3, timeout)
        if ctx_timeout.state == ctx_timeout.TIMED_OUT:
            return timeout_error
        elif ctx_timeout.state == ctx_timeout.EXECUTED:
            if not res:
                return timeout_error
            return res
