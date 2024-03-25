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
        return TextInfo(**requests.post(self.dfa, json={"text": texts,"ip_adderss": ip_address}).json())
    
    def predict_all(self, path:str, ip_address:str):
        reponse = requests.post(self.all, json={"image": read_b64(path), 'ip_address': ip_address})
        return reponse.json()
    
    def predict_video(self, path:str, ip_address:str):
        with open(path, 'rb') as f:
            file_data = f.read()
            response = requests.post(self.video, files={'file': ("file", file_data)}, data = {'ip_address':ip_address})
        return response.json()




if __name__ == "__main__":
    
    
    
    fps = [ "/Users/wanghuan/Projects/anomaly/client/tests/sex.png", "/Users/wanghuan/Projects/anomaly/client/tests/test.png",]#"./tests/sex.png",
    
    m = BackendClient()
    
    for fp in fps:

        
        all_result = m.predict_all(fp, ip_address = "fuck, what is that")
        print(all_result)
        
        
        text_result = m.predict_dfa(texts = ['你妈逼，你是傻逼吧，卧槽，草泥马'], ip_address = 'www.pornlove.net')
        print(text_result)
    
    

    video_response = m.predict_video("/Users/wanghuan/Desktop/ anomaly material/file1.mp4", ip_address = "bbuuccddffss")
    print(video_response)