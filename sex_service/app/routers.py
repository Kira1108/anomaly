from fastapi import APIRouter
from app.reader import ImageReader
from app.model import SexInfo
from app.model import SexDetector
from pydantic import BaseModel

sex_model = SexDetector()

router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)

class Base64Input(BaseModel):
    content:str

ocr = SexDetector()

@router.get("/sex_local", response_model=SexInfo)
async def parse_sex(path:str):
    img = ImageReader(path).read()
    r = sex_model.predict(img)
    return r


@router.post("/sex", response_model=SexInfo)
async def parse_sex(content:Base64Input):
    img = ImageReader(content = content.content).read()
    r = sex_model.predict(img)
    return r