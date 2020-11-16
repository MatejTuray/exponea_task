import os
import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_restful.api_settings import get_api_settings
from fastapi_restful.openapi import simplify_operation_ids
from fastapi_restful.timing import add_timing_middleware
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from openapi_meta import tags_metadata
from resources.all_responses_resource import AllResponsesResource
from resources.first_response_resource import FirstResponseResource
from resources.threshold_responses_resource import ThresholdResponsesResource
from resources.smart_response_resource import SmartResponseResource
from utils.api import Api
from logger import log

load_dotenv(verbose=True)


def create_app():
    get_api_settings.cache_clear()
    settings = get_api_settings()
    settings.docs_url = "/api/docs"
    settings.redoc_url = "/api/redoc"
    settings.title = "Exponea Task Api"
    app = FastAPI(openapi_tags=tags_metadata, **settings.fastapi_kwargs)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    api = Api(app, prefix="/api")
    api.add_resource(AllResponsesResource(), "/all", tags=["Exponea Test Server"])
    api.add_resource(FirstResponseResource(), "/first", tags=["Exponea Test Server"])
    api.add_resource(
        ThresholdResponsesResource(),
        "/within-timeout",
        tags=["Exponea Test Server"],
    )
    api.add_resource(SmartResponseResource(), "/smart", tags=["Exponea Test Server"])
    simplify_operation_ids(app)
    add_timing_middleware(app, record=log.info, prefix="/api")
    Instrumentator().instrument(app).expose(app)
    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Pong!"}


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0, attach_stacktrace=True
)

app = SentryAsgiMiddleware(app)
