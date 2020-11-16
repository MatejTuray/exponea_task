from fastapi_restful import Resource
from logger import log


class BaseResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.runners = []

    def log_request(self, request):
        try:
            log.info(
                "Request",
                extra={
                    "request_handler": self.__class__.__name__,
                    "request_content_type": request.headers["accept"],
                    "request_user_agent": request.headers["user-agent"],
                    "request_method": request.method,
                    "request_url": request.url._url,
                    "request_client": f"{request.client[0]}:{request.client[1]}",
                },
            )
        except RuntimeError:
            pass
