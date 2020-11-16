import datetime
import logging
import sys
import json_log_formatter
from functools import wraps


def logRoundtrip(response, *args, **kwargs):
    log.info(
        "LogRoundTrip",
        extra={
            "req": {
                "request_method": response.request.method,
                "request_url": response.request.url,
                "request_user_agent": response.request.headers["User-Agent"],
            },
            "elapsed": response.elapsed.total_seconds() * 1000,
        },
    )


def log_request():
    def log_decorator(f, *args, **kwargs):
        @wraps(f, *args, **kwargs)
        def decorated(self, request, *args, **kwargs):
            self.log_request(request)
            return f(self, request, *args, **kwargs)

        return decorated

    return log_decorator


class CustomJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra["message"] = message
        if "time" not in extra:
            extra["time"] = datetime.datetime.utcnow()
        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)
        extra["log_level"] = record.levelname
        return extra


formatter = CustomJSONFormatter()
json_handler = logging.StreamHandler(sys.stdout)
json_handler.setFormatter(formatter)
logging.getLogger().addHandler(json_handler)
logging.getLogger().setLevel(logging.INFO)
log = logging
