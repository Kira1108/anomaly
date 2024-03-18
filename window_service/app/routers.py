from fastapi import APIRouter
from app.reader import ImageReader
from app.model import AbnWindowInfo,AbnormaWindowDetect
from pydantic import BaseModel

class Base64Input(BaseModel):
    content:str

window_model = AbnormaWindowDetect()

router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)

@router.get("/window_local", response_model=AbnWindowInfo)
async def parse_sex(path:str):
    img = ImageReader(path).read()
    r = window_model.predict(img)
    return r


@router.post("/window", response_model=AbnWindowInfo)
async def parse_sex(content:Base64Input):
    img = ImageReader(content = content.content).read()
    r = window_model.predict(img)
    return r


