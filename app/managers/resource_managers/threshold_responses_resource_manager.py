from stopit import ThreadingTimeout
from managers.resource_managers.all_responses_resource_manager import ResponseHelper


class ThresholdResponsesResourceManager(ResponseHelper):
    
    
    def handle_get(self,timeout, runners, controllers):
        ctx_timeout, res = self.base_schedule(timeout, runners, controllers)                     
        if ctx_timeout.state == ctx_timeout.EXECUTED:
            if not res:
                return []
            return [item for item in res if type(item) == dict]
        return []