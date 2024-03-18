from sqlalchemy.orm import Session
from sqlalchemy import update
from app.models import (
    DbOCR, 
    DbText, 
    DbSex, 
    DbWindow,
    DbVideo, 
    DbVideoFrames,
    DbUser)
from app.crud.hash import Hash

def save_ocr_result(db:Session, ocr_result, content_id, image_id, image_path, ip_address = None):
    """saved ocred results to database"""
    for box in ocr_result:
        box_result = DbOCR(
            text = box.text,
            confidence = box.confidence,
            topleft = str(box.topleft),
            topright = str(box.topright),
            bottomright = str(box.bottomright),
            bottomleft = str(box.bottomleft),
            content_id = content_id,
            image_id = image_id,
            image_path = image_path,
            ip_address = ip_address
        )
        db.add(box_result)
        db.commit()
        db.close()


def save_text_result(db:Session, text_result, content_id, ip_address = None, image_path = None):
    """save text analyze results to database"""
    for record in text_result.result:
        text_model = DbText(
            content_id = content_id,
            text = record['text'],
            sensitive = record['sensitive'],
            sensitive_words = str(record['sensitive_words']),
            ip_address = ip_address,
            image_path= image_path
        )
        db.add(text_model)
        db.commit()
        db.close()


def save_sex_result(db:Session, sex_result, content_id, image_id, image_path, ip_address = None):
    "save sexual detect results to database"

    sex_dic = sex_result.sex_model_result

    max_key = max(sex_dic, key = sex_dic.get)
    sex_sensitive = max_key in ['hentai','porn','sexy'] and sex_dic[max_key] > 50

    sex = DbSex(
        content_id = content_id,
        image_id = image_id,
        image_path = image_path,
        ip_address = ip_address,
        is_abnormal = sex_sensitive,
        **sex_result.sex_model_result
    )

    db.add(sex)
    db.commit()
    db.close()

def save_window_result(db:Session, window_result, content_id, image_id, image_path, ip_address = None):
    "save sexual detect results to database"
    window = DbWindow(
        content_id = content_id,
        image_id = image_id,
        image_path = image_path,
        ip_address = ip_address,
        confidence = window_result.confidence,
        is_abnormal = window_result.is_abnormal
    )
    db.add(window)
    db.commit()
    db.close()



def save_video_raw(db:Session, video_path:str, content_id, ip_address = None):
    "save ratio information to database"
    video = DbVideo(
        video_path = video_path, 
        content_id = content_id, 
        is_processed = False,
        ip_address = ip_address)
    db.add(video)
    db.commit()
    db.close()


def get_next_video(db: Session):
    """retrieve next unprocessed video"""
    result = db.query(DbVideo)\
        .filter(DbVideo.is_processed == 0)\
        .order_by(DbVideo.create_time.asc())\
        .first()
    db.close()
    return result


def update_video_status(db: Session, video):
    """query video status"""
    db.execute(update(DbVideo)\
        .where(DbVideo.content_id == video.content_id)\
        .values(is_processed = True))
    db.commit()
    db.close()


def save_video_frame(db: Session, video_content_id, image_content_id, image_path, ip_address = None):
    """save video frames to database"""
    video_frame = DbVideoFrames(
        video_content_id = video_content_id,
        image_content_id = image_content_id,
        image_path = image_path,
        ip_address = ip_address
    )
    db.add(video_frame)
    db.commit()
    db.close()


