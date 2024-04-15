from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime

from app.models import (DbText, DbSex, DbWindow,DbOCR)

from sqlalchemy.orm import Session
from sqlalchemy import func, distinct


def get_text_abnormal(db: Session, start_time:datetime, end_time:datetime):
    return paginate(db.query(DbText)\
    .filter(DbText.sensitive == 1)\
    .filter(DbText.create_time >= start_time)\
    .filter(DbText.create_time < end_time)\
    .filter(DbText.image_path != "pure_text").order_by(DbText.create_time.desc()))
    
    
def get_puretext_abnormal(db: Session, start_time:datetime, end_time:datetime):
    return paginate(
        db.query(DbText)\
        .filter(DbText.sensitive == 1)\
        .filter(DbText.create_time >= start_time)\
        .filter(DbText.create_time < end_time)\
        .filter(DbText.image_path == "pure_text").order_by(DbText.create_time.desc())
    )

def get_window_abnormal(db: Session, start_time:datetime, end_time:datetime):
    return paginate(
        db.query(DbWindow)\
        .filter(DbWindow.is_abnormal == 1)\
        .filter(DbWindow.create_time >= start_time)\
        .filter(DbWindow.create_time < end_time).order_by(DbWindow.create_time.desc()))

def get_sex_abnormal(db: Session, start_time:datetime, end_time:datetime):
    return paginate(
        db.query(DbSex)\
        .filter(DbSex.is_abnormal == 1)\
        .filter(DbSex.create_time >= start_time)\
        .filter(DbSex.create_time < end_time).order_by(DbSex.create_time.desc())
        )

def get_ocr_count(db:Session):
    return db.query(func.count(distinct(DbOCR.content_id))).scalar()

def get_sex_count(db:Session):
    return db.query(func.count(distinct(DbSex.content_id))).scalar()

def get_window_count(db:Session):
    return db.query(func.count(distinct(DbWindow.content_id))).scalar()

def get_text_count(db:Session):
    return db.query(func.count(DbText.content_id)).scalar()


