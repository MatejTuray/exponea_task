from fastapi import FastAPI

from fastapi_restful import Api


def create_app():
    app = FastAPI()
    api = Api(app)
  
    # api.add_resource(myapi, "/uri")

    return app


main = create_app()