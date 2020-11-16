from pydantic import BaseModel, Field
from typing import List


class TimeOutSingle(BaseModel):
    time: int


class TimeOut(BaseModel):
    responses: List[TimeOutSingle]
