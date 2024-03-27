import logging
logging.basicConfig(level=logging.INFO)

import requests
from PIL import Image
import io
import base64
import os
from app.schemas import AbnWindowInfo, OcrResponse, TextInfo, SexInfo

from functools import lru_cache

from app.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD
)

import hashlib
import base64
import json
import redis

import logging

@lru_cache()
def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)


def dump_redis(key:str,d:dict):
    r = get_redis()
    r.set(key, json.dumps(d))
    return True

def load_redis(key:str):
    r = get_redis()
    content = r.get(key)
    if content is None:
        return None
    return json.loads(content.decode('utf-8'))

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

def b64_to_md5(b64_string):
    # Create an md5 hash object
    md5_hash = hashlib.md5()
    # Update the hash object with the decoded string
    md5_hash.update(b64_string.encode())
    # Get the hexadecimal representation of the hash
    md5_hex = md5_hash.hexdigest()
    return md5_hex
            
class AnomalyClient:
    
    def __init__(self):
        self.window = f"http://{os.getenv('WINDOW_URL')}:8000/image/window"
        self.ocr    = f"http://{os.getenv('OCR_URL')}:8000/image/ocr"
        self.sex = f"http://{os.getenv('SEX_URL')}:8000/image/sex"
        self.dfa = f"http://{os.getenv('DFA_URL')}:8000/text/dfa"
        
    def predict_ocr(self, b64):
        # convert b64 string into md5 hash
        md5 = "ocr" + b64_to_md5(b64)

        response = load_redis(md5)
        if response is not None:
            logging.info("Ocr response from cache")
            return OcrResponse(**response)
 
        response = requests.post(self.ocr, json={"content": str(b64)})
        dump_redis(md5, response.json())
        return OcrResponse(**response.json())
    
    def predict_window(self, b64):
        
        md5 = "window" + b64_to_md5(b64)
        response = load_redis(md5)
        if response is not None:
            logging.info("Window response from cache")
            return AbnWindowInfo(**response)
        response = requests.post(self.window, json={"content": str(b64)})
        dump_redis(md5, response.json())
        return AbnWindowInfo(**response.json())
    
    def predict_sex(self, b64):
        md5 = "sex" + b64_to_md5(b64)
        response = load_redis(md5)
        if response is not None:
            logging.info("Sex response from cache")
            return SexInfo(**response)
        response = requests.post(self.sex, json={"content": str(b64)})
        dump_redis(md5, response.json())
        return SexInfo(**response.json())
            
    def predict_dfa(self, texts):
        md5 = "dfa" + b64_to_md5(str(texts))
        response = load_redis(md5)
        if response is not None:
            logging.info("DFA response from cache")
            return TextInfo(**response)    
        response = requests.post(self.dfa, json={"texts": texts})
        dump_redis(md5, response.json())
        return TextInfo(**response.json())
    
    def predict_ocr_path(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.ocr, json={"content": str(img_b64)})
        return OcrResponse(**response.json())
    
    def predict_window_path(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.window, json={"content": str(img_b64)})
        return AbnWindowInfo(**response.json())
    
    def predict_sex_path(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.sex, json={"content": str(img_b64)})
        return SexInfo(**response.json())