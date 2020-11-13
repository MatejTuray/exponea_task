from fastapi_restful import Resource


class SmartResponse(Resource):
    def get(self):
        return "done"