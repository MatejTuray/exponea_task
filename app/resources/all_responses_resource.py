from typing import List

from controllers.remoteApiController import RemoteApiController
from managers.resource_managers.all_responses_resource_manager import (
    AllResponsesResourceManager,
)
from fastapi import Depends, Request
from fastapi_restful import set_responses
from interfaces.taskInterface import add_runner
from logger import log_request
from parsers.output.time_parser import TimeOutSingle
from utils.convert_from_ms import convert_from_ms
from utils.enums import SourceTypes, TaskTypes, URLList
from utils.response_models import TimeoutErrorModel
from logger import log
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
        exponea_cntrl = RemoteApiController(
            url=URLList.EXPONEA_TEST_SERVER.value, timeout=timeout
        )
        return AllResponsesResourceManager().handle_get(
            timeout, self.runners, [exponea_cntrl]
        )
