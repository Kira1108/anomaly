from fastapi import APIRouter
from app.model import TextInfo,DFAParser
from typing import List
from pydantic import BaseModel

dfa_parser = DFAParser()


class TextInput(BaseModel):
    texts:List[str]
    
router = APIRouter(
    prefix="/text",
    tags=["text"],
    responses={404: {"description": "Not found"}},
)

@router.post("/dfa", response_model=TextInfo)
async def parse_text(texts:TextInput):
    r = dfa_parser.parse(texts.texts)
    return r