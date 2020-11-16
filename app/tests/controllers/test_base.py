from async_asgi_testclient import TestClient
from main import app
from pytest import mark


class BaseTest:
    def __init__(self) -> None:
        self.client = TestClient(app)


@mark.asyncio()
@mark.describe("Base app tests")
def AppTest(BaseTest):
    @mark.asyncio()
    @mark.it("Should start without errors")
    async def should_start(self):
        async with self.client:
            resp = await self.client.get("/")
            assert resp.status_code == 200

