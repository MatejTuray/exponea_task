from fastapi_restful import Resource


class ThresholdedResponse(Resource):
    def get(self):
        return "done"