import logging
logging.basicConfig(level=logging.INFO)
import requests
from PIL import Image
import io
import base64
import os
from schemas import (
    AbnWindowInfo, 
    OcrResponse, 
    TextInfo, 
    SexInfo
)
from pathlib import Path
import json
import shutil

from apscheduler.schedulers.background import BackgroundScheduler
import time


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
            
class BackendClient:
    
    def __init__(self):
        self.window = "http://localhost:8004/image/window"
        self.sex    = "http://localhost:8004/image/sex"
        self.ocr    = "http://localhost:8004/image/ocr"
        self.all    = "http://localhost:8004/image/all"
        self.dfa    = "http://localhost:8004/text/dfa" 
        self.video  = "http://localhost:8004/video/videofile"
        
    def predict_ocr(self, path:str, ip_address:str):
        img_b64 = read_b64(path)
        response = requests.post(self.ocr, json={"image": str(img_b64), 'ip_address': ip_address})
        return OcrResponse(**response.json())
    
    def predict_window(self, path:str, ip_address:str):
        img_b64 = read_b64(path)
        response = requests.post(self.window, json={"image": str(img_b64), 'ip_address': ip_address})
        return AbnWindowInfo(**response.json())
    
    
    def predict_sex(self, path:str, ip_address:str):
        img_b64 = read_b64(path)
        response = requests.post(self.sex, json={"image": str(img_b64), 'ip_address': ip_address})
        return SexInfo(**response.json())
        
    def predict_dfa(self, texts:list, ip_address:str):
        return TextInfo(**requests.post(self.dfa, json={"text": texts,"ip_address": ip_address}).json())
    
    def predict_all(self, path:str, ip_address:str):
        reponse = requests.post(self.all, json={"image": read_b64(path), 'ip_address': ip_address})
        return reponse.json()
    
    def predict_video(self, path:str, ip_address:str):
        with open(path, 'rb') as f:
            file_data = f.read()
            response = requests.post(self.video, files={'file': ("file", file_data)}, data = {'ip_address':ip_address})
        return response.json()

m = BackendClient()

def process_site(site_folder:str):

    site_folder = Path(site_folder)
    # 所有时间节点上的爬取记录
    scaper_temporal_folders = [x for x in site_folder.iterdir() if x.is_dir()]

    # 轮训一下所有文件夹(时间节点)
    for dir in scaper_temporal_folders:
        logging.info(f"Processing project: {dir}")
        meta_path = dir / "meta.json"
        
        # 打开meta.json文件
        with open(meta_path,'r') as f:
            meta = json.load(f)['urls']
            
        # 按照meta.json文件中的页面处理
        for page in meta:
            logging.info(f"Processing page: {page['name']}")
            url = page['url']
            
            # 页面文件夹
            page_folder = dir / page['name']
            
            # 图片文件夹
            image_folder = page_folder / "image"
            
            # 文本文件夹
            txt_folder = page_folder / "txt"
            
            # 轮图片
            
            for img in image_folder.glob("*.png"):
                logging.info(f"Processing image: {img}")
                img_path = str(img)
                res = m.predict_all(img_path, url)
            
            # 轮文本  
            for txt in txt_folder.glob("*.txt"):
                logging.info(f"Processing text: {txt}")
                txt_path = str(txt)
                with open(txt_path, 'r') as f:
                    for line in f:
                        res = m.predict_dfa([line], url)  
        shutil.rmtree(dir)          
        
        
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_site, 'interval', hours=1, args=["/Users/wanghuan/Projects/anomaly/hx_client/site1/data"])
    scheduler.add_job(process_site, 'interval', hours=1, args=["/Users/wanghuan/Projects/anomaly/hx_client/site2/data"])
    scheduler.start()

    # This is here to simulate application activity (which keeps the main thread alive).
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible
        
if __name__ == "__main__":
    start_scheduler()
