from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.ai_client import AnomalyClient 
from app.schemas import TextInfo
from app.utils import md5_id
from app.crud import save_text_result
from app.database import get_db
from app.schemas import TextInput
from sqlalchemy.orm import Session

client = AnomalyClient()

router = APIRouter(
    prefix="/text",
    tags=["text"],
    responses={404: {"description": "Not found"}},
)

@router.post("/dfa", response_model=TextInfo)
async def parse_text(texts:TextInput, db: Session = Depends(get_db)):
    r = client.predict_dfa(texts.text)
    save_text_result(db, r, md5_id())
    return r