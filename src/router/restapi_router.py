from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict

from _db_conn import *

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

class doStuffData(BaseModel):
    param_0: int
    param_1: int
    param_2: int
    brian: str

class getS3Data(BaseModel):
    param_0: int


# ids = json.dumps({"0":"getstuff","1":"10","2":"0"})

@router.post("/getStuff/")
async def getData(data: getStuffData):
    print (data.param_0, str(data.param_1), str(data.param_2))
    pgData = getPGData(data.param_0, str(data.param_1), str(data.param_2))
    return json.dumps(pgData)
@router.post("/doStuff/")
async def doStuff(data: doStuffData):
    print (data.param_0, str(data.param_1), str(data.param_2), data.brian, str(data.param_2))
    pgData = doStuffWithData(data.param_0, str(data.param_1), "'"+(data.brian)+"'",  str(data.param_2))
    #return pgData
    return JSONResponse(content=json.dumps(pgData), media_type="application/json")

@router.post("/getS3/")
async def getS3(data: getS3Data):
    print (data.param_0)
    s3Data = "request received"
    return s3Data

