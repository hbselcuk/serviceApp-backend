from fastapi import APIRouter
from pydantic import BaseModel


class DemoData(BaseModel):
    test_string: str

router = APIRouter(
    prefix="/demo",
    tags=["demo"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def demo_post(data: DemoData):
    return {"test_string": data.test_string}
    

