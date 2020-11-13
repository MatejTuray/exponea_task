from fastapi_restful import Resource


class FirstResponse(Resource):
    def get(self):
        return "done"