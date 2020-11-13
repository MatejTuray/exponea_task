from fastapi_restful import Resource
from app.interfaces.taskInterface import add_runner
from app.utils.enums import SourceTypes, TaskTypes, URLList
from app.controllers.communicationsController import CommunicationController


@add_runner(SourceTypes.EXPONEA, TaskTypes.ALL_SUCCESSFUL)
class AllResponses(Resource):
    def get(self):
        exponea_test_cntrl = CommunicationController(
            url=URLList.EXPONEA_TEST_SERVER.value, timeout=2
        )
        # exponea_runner = self.kwargs[EXPONEA_ALL_SUCCESSFUL]
        # exponea_runner.add_task(exponea_test_cntrl.get)
        # res = exponea_runner.schedule_tasks()
