from managers.resource_managers.threshold_responses_resource_manager import (
    ThresholdResponsesResourceManager,
)
from typing import List, Optional

from controllers.remoteApiController import RemoteApiController
from fastapi import Depends, Request
from fastapi_restful import set_responses
from interfaces.taskInterface import add_runner
from logger import log_request
from parsers.output.time_parser import TimeOutSingle
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
        exponea_cntrl = RemoteApiController(
            url=URLList.EXPONEA_TEST_SERVER.value, timeout=timeout
        )
        return ThresholdResponsesResourceManager().handle_get(
            timeout, self.runners, [exponea_cntrl]
        )
