import json
import logging

from async_asgi_testclient import TestClient
from controllers.remoteApiController import RemoteApiController
from main import app
from managers.resource_managers.all_responses_resource_manager import (
    AllResponsesResourceManager,
)
from pytest import mark
from requests.exceptions import HTTPError, ReadTimeout
from task_runners.runner import AllRunner
from tests.test_base import BaseTest
from utils.enums import URLList

from resources.all_responses_resource import AllResponsesResource


@mark.describe("All responses resource tests")
class TestAllResponsesResource(BaseTest):
    @mark.asyncio()
    @mark.it("Should return response")
    async def test_should_return_response(self):
        async with TestClient(app) as client:
            resp = await client.get("/api/all?timeout=5000")
            assert resp.status_code
            assert resp.json()

    @mark.it("Should return status code 200 and a json response")
    def test_success_mock(self, mocker):
        resource = mocker.patch.object(AllResponsesResource, "get")
        resource.get.return_value = self.create_response(200, [{"time": 123}])
        resp = resource.get(timeout=1000)
        assert resp.status_code == 200
        assert resp.json() == [{"time": 123}]
        assert resource.get.called_once_with(timeout=1000)

    @mark.it("Should return status code 504 and a json response")
    def test_timeout_mock(self, mocker):
        resource = mocker.patch.object(AllResponsesResource, "get")
        resource.get.return_value = self.create_response(
            504,
            {
                "error_message": "Request did not complete in specified time",
                "error_code": "timeout_exceeded",
            },
        )
        resp = resource.get(timeout=1000)
        assert resp.status_code == 504
        assert resp.json() == {
            "error_message": "Request did not complete in specified time",
            "error_code": "timeout_exceeded",
        }
        assert resource.get.called_once_with(timeout=1000)


@mark.describe("All responses resource manager tests")
class TestAllResponsesResourceManager(BaseTest):
    url = URLList.EXPONEA_TEST_SERVER.value
    cntrl = RemoteApiController(url=url, timeout=5)

    @mark.it("Should return valid response")
    def test_success(self, requests_mock, caplog):
        runner = AllRunner()
        requests_mock.register_uri("GET", self.url, json={"time": 123}, status_code=200)
        response = AllResponsesResourceManager().handle_get(
            timeout=2, runners=[runner], controllers=[self.cntrl]
        )
        assert response == [{"time": 123}, {"time": 123}, {"time": 123}]

    @mark.it("Should return timeout error")
    def test_timeout(self, requests_mock, caplog):
        runner = AllRunner()
        requests_mock.register_uri("GET", self.url, exc=HTTPError)
        response = AllResponsesResourceManager().handle_get(
            timeout=2, runners=[runner], controllers=[self.cntrl]
        )
        assert json.loads(response.body) == {
            "error_message": "Request did not complete in specified time",
            "error_code": "timeout_exceeded",
        }
