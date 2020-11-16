from typing import Any, Dict, Optional, Tuple

from fastapi import APIRouter, FastAPI

from fastapi_restful.cbv import (
    INCLUDE_INIT_PARAMS_KEY,
    RETURN_TYPES_FUNC_KEY,
    _cbv,
)

## fastapi_restful custom extension for API object


class Resource:
    # raise NotImplementedError
    pass


class Api:
    def __init__(self, app: FastAPI, prefix: str):
        self.prefix = prefix
        self.app = app

    def add_resource(
        self, resource: Resource, *urls: str, **kwargs: Any
    ) -> None:
        router = APIRouter()
        _cbv(router, type(resource), *urls, instance=resource)
        self.app.include_router(
            router, prefix=self.prefix, tags=kwargs.get("tags")
        )


def take_init_parameters(cls: Any) -> Any:
    setattr(cls, INCLUDE_INIT_PARAMS_KEY, True)
    return cls


def set_responses(
    response: Any,
    status_code: int = 200,
    responses: Dict[str, Any] = None,
    summary: str = "Default summary",
    **kwargs: Any
) -> Any:
    def decorator(func: Any) -> Any:
        def get_responses() -> Tuple[
            Any, int, Optional[Dict[str, Any]], str, Optional[Any]
        ]:
            return response, status_code, responses, summary, kwargs

        print(func)
        setattr(func, RETURN_TYPES_FUNC_KEY, get_responses)
        return func

    return decorator
