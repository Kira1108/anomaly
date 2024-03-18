import requests
from PIL import Image
import io
import base64
import os
from app.schemas import AbnWindowInfo, OcrResponse, TextInfo, SexInfo

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
            
class AnomalyClient:
    
    def __init__(self):
        self.window = f"http://{os.getenv('WINDOW_URL')}:8000/image/window"
        self.ocr    = f"http://{os.getenv('OCR_URL')}:8000/image/ocr"
        self.sex = f"http://{os.getenv('SEX_URL')}:8000/image/sex"
        self.dfa = f"http://{os.getenv('DFA_URL')}:8000/text/dfa"
        
    def predict_ocr(self, b64):
        response = requests.post(self.ocr, json={"content": str(b64)})
        return OcrResponse(**response.json())
    
    def predict_window(self, b64):
        response = requests.post(self.window, json={"content": str(b64)})
        return AbnWindowInfo(**response.json())
    
    def predict_sex(self, b64):
        response = requests.post(self.sex, json={"content": str(b64)})
        return SexInfo(**response.json())
        
    def predict_dfa(self, texts):
        return TextInfo(**requests.post(self.dfa, json={"texts": texts}).json())
         
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