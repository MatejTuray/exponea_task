from managers.resource_managers.smart_response_resource_manager import (
    SmartResponseResourceManager,
)
from controllers.remoteApiController import RemoteApiController
from fastapi import Depends, Request
from fastapi_restful import set_responses
from interfaces.taskInterface import add_runner
from logger import log, log_request
from parsers.output.time_parser import TimeOutSingle
from utils.convert_from_ms import convert_from_ms
from utils.enums import SourceTypes, TaskTypes, URLList
from utils.response_models import TimeoutErrorModel

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
        exponea_test_cntrl_first = RemoteApiController(
            url=URLList.EXPONEA_TEST_SERVER.value, timeout=0.3
        )
        exponea_test_cntrl_subsequent = RemoteApiController(
            url=URLList.EXPONEA_TEST_SERVER.value, timeout=timeout
        )
        return SmartResponseResourceManager.handle_get(
            timeout,
            self.runners,
            [exponea_test_cntrl_first, exponea_test_cntrl_subsequent],
        )
