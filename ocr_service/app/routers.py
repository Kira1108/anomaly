from fastapi import APIRouter
from app.reader import ImageReader
from app.model import OcrResponse
from app.model import Ocr
from fastapi import Body
from pydantic import BaseModel


router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)

ocr = Ocr()



class Base64Input(BaseModel):
    content:str

@router.get("/ocr_local", response_model=OcrResponse)
async def parse_ocr(path:str):
    img = ImageReader(path).read()
    return ocr.get_box(img)


@router.post("/ocr", response_model=OcrResponse)
async def parse_ocr(content:Base64Input):
    img = ImageReader(content=content.content).read()
    return ocr.get_box(img)