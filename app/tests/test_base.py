from async_asgi_testclient import TestClient
from main import app
from pytest import mark
import json
from requests import Response


class BaseTest:
    def create_response(self, status, resp_data):
        resp = Response()
        resp.status_code = status
        resp._content = json.dumps(resp_data).encode()
        return resp


@mark.asyncio()
@mark.describe("Base app tests")
class TestBaseApp:
    @mark.asyncio()
    @mark.it("Should start without errors")
    async def test_should_start(self):
        async with TestClient(app) as client:
            resp = await client.get("/")
            assert resp.status_code == 200
            assert resp.json() == {"message": "Pong!"}
