from async_asgi_testclient import TestClient
from resources.all_responses_resource import AllResponsesResource
from managers.resource_managers.all_responses_resource_manager import AllResponsesResourceManager
from controllers.remoteApiController import RemoteApiController
from utils.enums import URLList
import logging
from main import app
from pytest import mark
from tests.test_base import BaseTest
from task_runners import AllRunner

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
    
    @mark.it("Should instantiate new cntrl with timeout, list of runners and a list of controllers")
    def test_init(self):
        mngr = AllResponsesResourceManager(timeout=5, runners=[], controllers=[])
        assert mngr.__class__.__name__ == "AllResponsesResourceManager"
        assert mngr.url == self.url
        assert mngr.timeout == 5


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


