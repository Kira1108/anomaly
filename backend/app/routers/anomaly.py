from app.crud.queries import (
    get_text_abnormal, 
    get_window_abnormal,
    get_sex_abnormal,
    get_ocr_count,
    get_sex_count, 
    get_text_count, 
    get_window_count,
    get_puretext_abnormal)
from app.schemas import TextOut, WindowOut, SexOut, Base64Output, ImagePathInput
from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.reader import File2b64Reader
from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/anormaly",
    tags=["anormaly"],
    responses={404: {"description": "Not found"}},
)

def process_times(start_time, end_time):
    if start_time is None:
        start_time = datetime.now()
        start_time = datetime(2022,1,1)

    if end_time is None:
        now = datetime.now()
        end_time = datetime(now.year, now.month, now.day) + timedelta(days = 1)
    
    return start_time, end_time


@router.get("/text", response_model=Page[TextOut])
@router.get("/text/limit-offset", response_model=LimitOffsetPage[TextOut])
def text_anormaly(db: Session = Depends(get_db), start_time:Optional[datetime] = None, end_time:Optional[datetime] = None):
    start_time, end_time = process_times(start_time, end_time)
    return get_text_abnormal(db,start_time, end_time)

@router.get("/puretext", response_model=Page[TextOut])
@router.get("/puretext/limit-offset", response_model=LimitOffsetPage[TextOut])
def text_anormaly(db: Session = Depends(get_db), start_time:Optional[datetime] = None, end_time:Optional[datetime] = None):
    start_time, end_time = process_times(start_time, end_time)
    return get_puretext_abnormal(db,start_time, end_time)



@router.get("/window", response_model=Page[WindowOut])
@router.get("/window/limit-offset", response_model=LimitOffsetPage[WindowOut])
def window_anormaly(db: Session = Depends(get_db), start_time:Optional[datetime] = None, end_time:Optional[datetime] = None):
    start_time, end_time = process_times(start_time, end_time)
    return get_window_abnormal(db,start_time, end_time)


@router.get("/sex", response_model=Page[SexOut])
@router.get("/sex/limit-offset", response_model=LimitOffsetPage[SexOut])
def sex_anormaly(db: Session = Depends(get_db), start_time:Optional[datetime] = None, end_time:Optional[datetime] = None):
    start_time, end_time = process_times(start_time, end_time)
    return get_sex_abnormal(db,start_time, end_time)


@router.get("/ocr_count")
def ocr_counts(db: Session = Depends(get_db)):
    return {"data":get_ocr_count(db)}

@router.get("/sex_count")
def sex_counts(db: Session = Depends(get_db)):
    return {"data":get_sex_count(db)}

@router.get("/window_count")
def window_counts(db: Session = Depends(get_db)):
    return {"data":get_window_count(db)}

@router.get("/text_count")
def text_counts(db: Session = Depends(get_db)):
    return {"data":get_text_count(db)}

@router.get("/img/{full_path:path}")
def get_image(full_path:str):
    return {"data":File2b64Reader(full_path).read()}


@router.post("/img", response_model = Base64Output)
def fetch_image(img: ImagePathInput):
    try:
        return Base64Output(b64_image = File2b64Reader(img.full_path).read())
    
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"image located at {img.full_path} not found")
    
