from typing import List

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


class AllResponsesResource(BaseResource):
    @log_request()
    @add_runner(SourceTypes.EXPONEA, TaskTypes.ALL_SUCCESSFUL)
    @set_responses(
        List[TimeOutSingle],
        200,
        {504: {"description": "Timeout Error", "model": TimeoutErrorModel}},
        summary="All successful responses",
        description="Endpoint collects all successful responses from Exponea testing HTTP server and "
        "returns the result as an array. If timeout is reached before all requests finish, or none of "
        "the responses were successful, the endpoint should return an 504 Timeout error.",
    )
    def get(self, request: Request, timeout: float = Depends(convert_from_ms)):       
        with ThreadingTimeout(timeout) as ctx_timeout:
            exponea_cntrl = CommunicationController(
                url=URLList.EXPONEA_TEST_SERVER.value, timeout=timeout
            )
            runner = self.runners[0]
            runner.push_task(exponea_cntrl.get, [None], 3)
            res = runner.schedule_tasks(3, timeout)
            response = [item for item in res if type(item) == dict]
        if ctx_timeout.state == ctx_timeout.TIMED_OUT:
            return timeout_error
        elif ctx_timeout.state == ctx_timeout.EXECUTED:
            if not response:
                return timeout_error
            return response
