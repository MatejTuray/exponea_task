from pytest import mark
from utils.enums import URLList
from controllers.remoteApiController import RemoteApiController
import logging
from requests.exceptions import ReadTimeout, HTTPError


@mark.describe("Requests to remote api (exponea test server)")
class TestRemoteApiController:
    url = URLList.EXPONEA_TEST_SERVER.value
    cntrl = RemoteApiController(url=url, timeout=5)

    @mark.it("Should instantiate new cntrl with url and timeout")
    def test_init(self):
        cntrl = RemoteApiController(url=self.url, timeout=5)
        assert cntrl.__class__.__name__ == "RemoteApiController"
        assert cntrl.url == self.url
        assert cntrl.timeout == 5

    @mark.it("Should return status code 200 and a json response")
    def test_get_should_succeed(self, requests_mock, caplog):
        requests_mock.register_uri(
            "GET", self.url, json={"time": 123}, status_code=200
        )
        with caplog.at_level(logging.INFO):
            resp = self.cntrl.get()
        assert resp == {"time": 123}
        assert "LogRoundTrip" in caplog.text

    @mark.it("Should timeout and log the response")
    def test_get_should_timeout_and_log_reponse(self, requests_mock, caplog):
        requests_mock.register_uri("GET", self.url, exc=ReadTimeout)
        with caplog.at_level(logging.ERROR):
            self.cntrl.get()
        assert "Handled request error while processing request" in caplog.text

    @mark.it("Should raise general http error and log the response")
    def test_get_should_error_and_log_reponse(self, requests_mock, caplog):
        requests_mock.register_uri("GET", self.url, exc=HTTPError)
        with caplog.at_level(logging.ERROR):
            self.cntrl.get()
        assert "Handled request error while processing request" in caplog.text

    @mark.it("Should raise general error and log the response")
    def test_get_should_error_and_log_reponse(self, requests_mock, caplog):
        requests_mock.register_uri("GET", self.url, exc=Exception)
        with caplog.at_level(logging.ERROR):
            self.cntrl.get()
        assert (
            "Handled unspecified error while processing request" in caplog.text
        )

    @mark.it("Benchmark get")
    def test_benchmark_get(self, benchmark, requests_mock):
        requests_mock.register_uri(
            "GET", self.url, json={"time": 123}, status_code=200
        )
        resp = benchmark(self.cntrl.get)
        assert resp == {"time": 123}
        
