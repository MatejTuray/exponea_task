from typing import List, Optional

from controllers.communicationsController import CommunicationController
from fastapi import Depends, Request
from fastapi_restful import set_responses
from interfaces.taskInterface import add_runner
from logger import log_request
from parsers.output.time_parser import TimeOutSingle
from stopit import ThreadingTimeout
from utils.convert_from_ms import convert_from_ms
from utils.enums import SourceTypes, TaskTypes, URLList

from resources.base import BaseResource


class ThresholdResponsesResource(BaseResource):
    @log_request()
    @add_runner(SourceTypes.EXPONEA, TaskTypes.WITHIN_TIMEOUT)
    @set_responses(
        Optional[List[TimeOutSingle]],
        200,
        summary="Successful responses within timeout",
        description="Endpoint collects all successful responses that return within a given "
        "timeout. If a timeout is reached before any of the 3 requests finish, the "
        "server should return an empty array instead of an error. ",
    )
    def get(self, request: Request, timeout: float = Depends(convert_from_ms)):
        with ThreadingTimeout(timeout) as ctx_timeout:
            exponea_test_cntrl = CommunicationController(
                url=URLList.EXPONEA_TEST_SERVER.value, timeout=timeout
            )
            runner = self.runners[0]
            runner.push_task(exponea_test_cntrl.get, [None], 3)
            res = runner.schedule_tasks(3, timeout)
        if ctx_timeout.state == ctx_timeout.TIMED_OUT:
            return []
        elif ctx_timeout.state == ctx_timeout.EXECUTED:
            return [item for item in res if type(item) == dict]
