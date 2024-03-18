from app.crud import (
    get_next_video, 
    update_video_status,
    save_video_frame,
    save_sex_result,
    save_ocr_result,
    save_text_result,
    get_video_result)

from app.reader import extract_video
from app.config import VIDEO_EXTRACT_PATH, VIDEO_CALLBACK_URL, KPS
from app.database import SessionLocal
from app.utils import md5_id
from app.ai_client import AnomalyClient

import os
import time
import logging
import glob
# import requests
from sqlalchemy.orm import Session
logger = logging.getLogger('uvicorn')

from PIL import Image
import io
import base64

client = AnomalyClient()

def read_b64(path):
    # Open image
    img = Image.open(path)
    # Create a BytesIO object
    img_byte_arr = io.BytesIO()
    # Save image to the BytesIO object
    img.save(img_byte_arr, format='PNG')
    # Get the byte array of the image
    img_byte_arr = img_byte_arr.getvalue()
    # Convert the byte array to a base64 string
    img_b64 = base64.b64encode(img_byte_arr).decode('utf-8')
    return img_b64


def process_image(db:Session, image_path:str, content_id:str):
    
    img = read_b64(image_path)
    image_id = int(os.path.basename(image_path).split(".")[0].split("_")[-1])

    r_sex = client.predict_sex(img)
    save_sex_result(db, r_sex, content_id, image_id, image_path)

    r_ocr = client.predict_ocr(img)
    save_ocr_result(db, r_ocr.result, content_id, image_id, image_path)

    texts = [t.text for t in r_ocr.result]
    r_text = client.predict_dfa(texts)
    save_text_result(db, r_text, content_id)



def process_next_video():
    while True:
        video = get_next_video(SessionLocal())

        if video is None:
            logger.info("No video to process")
            time.sleep(5)
            continue
        else:
            extract_video(video.video_path, VIDEO_EXTRACT_PATH, kps = KPS)
            dest_path = os.path.join(VIDEO_EXTRACT_PATH, video.content_id)
            logger.info(f"Extracting video from {video.video_path} to {dest_path}")

            # save video frames to database
            image_files = glob.glob(os.path.join(dest_path, "*.jpg"))
            for im in image_files:
                image_content_id = md5_id()
                try:
                    logger.info(f"Processing image: {im}")
                    save_video_frame(SessionLocal(), video.content_id, image_content_id, im)
                    process_image(SessionLocal(), im, image_content_id)
                except Exception as e:
                    logger.error(f"Error processing image {im}")
                    logger.error(e)

            # update processing status
            update_video_status(SessionLocal(), video)
            import json
            json_content = json.dumps(get_video_result(video.content_id))
            with open("videojson.json",'w') as f:
                f.write(json_content)

        # if VIDEO_CALLBACK_URL != "":
        #     logger.info("Sending callback to: {VIDEO_CALLBACK_URL}, Video Content id: {video.content_id}")
        #     requests.post(VIDEO_CALLBACK_URL, json=get_video_result(video.content_id))
    
