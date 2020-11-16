from async_asgi_testclient import TestClient
from resources.threshold_responses_resource import ThresholdResponsesResource
from logger import log
from main import app
from pytest import mark
from tests.test_base import BaseTest


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
        resource.get.return_value = self.create_response(
            200, []
        )
        resp = resource.get(timeout=1000)
        assert resp.status_code == 200
        assert resp.json() == []
        assert resource.get.called_once_with(timeout=1000)