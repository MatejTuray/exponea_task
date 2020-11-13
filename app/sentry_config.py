import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app import main

sentry_sdk.init(dsn="https://examplePublicKey@o0.ingest.sentry.io/0")

asgi_app = SentryAsgiMiddleware(main)