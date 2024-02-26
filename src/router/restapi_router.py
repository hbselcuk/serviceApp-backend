from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict
from modules.auth.utils import VerifyToken


from modules.auth.db_conn import *

from s3_conn import listObjects, generatePresignedDownloadUrl, generatePresignedUploadUrl

import json

auth = VerifyToken()
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
    orderId: str
    filename: str


# ids = json.dumps({"0":"getstuff","1":"10","2":"0"})

@router.post("/getStuff/")
async def getData(data: getStuffData, req: Request):
    print (data.param_0, str(data.param_1), str(data.param_2))
    pgData = getPGData(data.param_0, str(data.param_1), str(data.param_2))
    return json.dumps(pgData)
    

@router.post("/doStuff/")
async def doStuff(data: doStuffData):
    print (data.param_0, str(data.param_1), str(data.param_2), data.brian, str(data.param_2))
    pgData = doStuffWithData(data.param_0, str(data.param_1), "'"+(data.brian)+"'",  str(data.param_2))
    #return pgData
    return JSONResponse(content=json.dumps(pgData), media_type="application/json")


@router.post("/getDownloadLink")
async def getDownloadLink(data: getS3Data):
    pre_signed_url = generatePresignedDownloadUrl('mov-dev-bucket', f'{data.orderId}/{data.filename}')

    if pre_signed_url:
        print("Pre-signed URL:", pre_signed_url)
        return pre_signed_url
    else:
        print("Failed to generate pre-signed URL.")


@router.post("/getUploadLink")
async def getUploadLink(data: getS3Data, req: Request):
    sub = req.userInfo['sub']
    pre_signed_url = generatePresignedUploadUrl('mov-dev-bucket', f'{sub}/{data.orderId}/{data.filename}')

    if pre_signed_url:
        print("Pre-signed URL:", pre_signed_url)
        return pre_signed_url
    else:
        print("Failed to generate pre-signed URL.")