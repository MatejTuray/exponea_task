import json

from async_asgi_testclient import TestClient
from controllers.remoteApiController import RemoteApiController
from main import app
from managers.resource_managers.threshold_responses_resource_manager import (
    ThresholdResponsesResourceManager,
)
from pytest import mark
from requests.exceptions import HTTPError, ReadTimeout
from task_runners.runner import AllRunner
from tests.test_base import BaseTest
from utils.enums import URLList

from resources.threshold_responses_resource import ThresholdResponsesResource


@mark.describe("Within timeout resource tests")
class TestTresholdResponsesResource(BaseTest):
    @mark.asyncio()
    @mark.it("Should return response")
    async def test_should_return_response(self):
        async with TestClient(app) as client:
            resp = await client.get("/api/within-timeout?timeout=5000")
            assert resp.status_code

    @mark.it("Should return status code 200 and a json response")
    def test_success_mock(self, mocker):
        resource = mocker.patch.object(ThresholdResponsesResource, "get")
        resource.get.return_value = self.create_response(200, {"time": 123})
        resp = resource.get(timeout=1000)
        assert resp.status_code == 200
        assert resp.json() == {"time": 123}
        assert resource.get.called_once_with(timeout=1000)

    @mark.it("Should return status code 200 and a json response - empty array")
    def test_timeout_mock(self, mocker):
        resource = mocker.patch.object(ThresholdResponsesResource, "get")
        resource.get.return_value = self.create_response(200, [])
        resp = resource.get(timeout=1000)
        assert resp.status_code == 200
        assert resp.json() == []
        assert resource.get.called_once_with(timeout=1000)


@mark.describe("All responses resource manager tests")
class TestTresholdResponsesResourceManager(BaseTest):
    url = URLList.EXPONEA_TEST_SERVER.value
    cntrl = RemoteApiController(url=url, timeout=5)

    @mark.it("Should return valid response")
    def test_success(self, requests_mock, caplog):
        runner = AllRunner()
        requests_mock.register_uri("GET", self.url, json={"time": 123}, status_code=200)
        response = ThresholdResponsesResourceManager().handle_get(
            timeout=2, runners=[runner], controllers=[self.cntrl]
        )
        assert response == [{"time": 123}, {"time": 123}, {"time": 123}]

    @mark.it("Should return empty array")
    def test_timeout(self, requests_mock, caplog):
        runner = AllRunner()
        requests_mock.register_uri("GET", self.url, exc=HTTPError)
        response = ThresholdResponsesResourceManager().handle_get(
            timeout=2, runners=[runner], controllers=[self.cntrl]
        )
        assert response == []
