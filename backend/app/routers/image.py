from fastapi import APIRouter, Depends
from typing import List, Optional
from pydantic import BaseModel
import os
from app.reader import ImageReader
from app.utils import md5_id
from app.config import IMAGE_PATH
from app.crud import (
    save_ocr_result,
    save_sex_result, 
    save_text_result, 
    save_window_result)
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import OcrResponse, Base64Input,AbnWindowInfo,SexInfo,BboxInfo

from PIL import Image

from app.ai_client import AnomalyClient

client = AnomalyClient()



router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)

@router.post("/ocr", response_model=OcrResponse)
async def parse_ocr(image:Base64Input, db: Session = Depends(get_db)):
    r = client.predict_ocr(image.image)
    save_ocr_result(db, r.result, md5_id(), 0, "",ip_address=image.ip_address)
    return r


@router.post("/sex", response_model=SexInfo)
async def parse_sex(image:Base64Input, db: Session = Depends(get_db)):
    r = client.predict_sex(image.image)
    save_sex_result(db, r, md5_id(), 0, "",ip_address=image.ip_address)
    return r

@router.post("/window", response_model=AbnWindowInfo)
async def parse_window(image:Base64Input, db: Session = Depends(get_db)):
    r = client.predict_window(image.image)
    save_window_result(db, r, md5_id(), 0, "",ip_address=image.ip_address)
    return r

@router.post("/all")
async def parse_all(image:Base64Input, db: Session = Depends(get_db)):
    # 

    content_id = md5_id()

    # parse sex info
    r_sex = client.predict_sex(image.image)
    
    # parse ocr-text info
    r_ocr = client.predict_ocr(image.image)
    
    texts = [t.text for t in r_ocr.result]
    r_text = client.predict_dfa(texts)
    
    # parse_window info
    r_window = client.predict_window(image.image)
    
    # retrieve detection results
    text_sensitive = any(record['sensitive'] for record in r_text.result)
    sex_dic = r_sex.sex_model_result
    max_key = max(sex_dic, key = sex_dic.get)
    sex_sensitive = max_key in ['hentai','porn','sexy'] and sex_dic[max_key] > 50
    window_sensitive = r_window.is_abnormal
    is_sensitive = text_sensitive or sex_sensitive or window_sensitive
    
    if is_sensitive:
        img = ImageReader(content = image.image).read()
        image_path = os.path.join(IMAGE_PATH, f"{content_id}.jpg")
        Image.fromarray(img).save(image_path) 
    else:
        image_path = ""
    
    # save to database
    save_sex_result(db, r_sex, content_id, 0, image_path,ip_address=image.ip_address)
    save_ocr_result(db, r_ocr.result, content_id, 0, image_path,ip_address=image.ip_address)
    save_text_result(db, r_text, content_id, ip_address=image.ip_address, image_path = image_path)
    save_window_result(db, r_window, md5_id(), 0, image_path,ip_address=image.ip_address)  

    response = {
        "image_content_id":content_id,
        "is_sensitive":is_sensitive,
        "sex_result": r_sex.sex_model_result, 
        "text_result": r_text.result,
        "window_result":r_window.is_abnormal
        }
    
    return response




