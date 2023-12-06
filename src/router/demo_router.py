from fastapi import APIRouter
from pydantic import BaseModel

from db_conn import *

import json

class DemoData(BaseModel):
    test_string: str
    test_int: int

router = APIRouter(
    prefix="/restAPI",
    tags=["restAPI"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def demo_post(data: DemoData):
    test = {"what":"it's a test"}
    return test

class getStuffData(BaseModel):
    param_0: int
    param_1: int
    param_2: int

# ids = json.dumps({"0":"getstuff","1":"10","2":"0"})

@router.post("/doStuff/")
async def getData(data: getStuffData):
    pgData = getPGData([data.param_0], [str(data.param_1)], [str(data.param_2)])
    #pgData = getPGData((str(data.param_1), [str(data.param_2)]))
    #pgData = getPGData("getstuff", 10, 0)
    return json.dumps(pgData)

