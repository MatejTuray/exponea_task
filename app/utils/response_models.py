from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class TimeoutErrorModel(BaseModel):
    error_message: str = Field(
        title="Error code",
        default="Request did not complete in specified time",
    )
    error_code: str = Field(title="Error message", default="timeout_exceeded")


timeout_error = JSONResponse(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    content={
        "error_message": "Request did not complete in specified time",
        "error_code": "timeout_exceeded",
    },
)

no_data = JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
