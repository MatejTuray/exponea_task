from managers.resource_managers.first_response_resource_manager import FirstResponseResourceManager
from controllers.remoteApiController import RemoteApiController
from fastapi import Depends, Request
from fastapi_restful import set_responses
from interfaces.taskInterface import add_runner
from logger import log_request
from parsers.output.time_parser import TimeOutSingle
from utils.convert_from_ms import convert_from_ms
from utils.enums import SourceTypes, TaskTypes, URLList
from utils.response_models import TimeoutErrorModel

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
        exponea_cntrl = RemoteApiController(
            url=URLList.EXPONEA_TEST_SERVER.value, timeout=timeout
        )
        return FirstResponseResourceManager().handle_get(
            timeout, self.runners, [exponea_cntrl]
        )

