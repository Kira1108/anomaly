import requests
from PIL import Image
import io
import base64
import os
from schemas import AbnWindowInfo, OcrResponse, TextInfo, SexInfo

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
        
    def predict_ocr(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.ocr, json={"image": str(img_b64), 'ip_address': "cctv-005-01"})
        return OcrResponse(**response.json())
    
    def predict_window(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.window, json={"image": str(img_b64), 'ip_address': "cctv-005-01"})
        return AbnWindowInfo(**response.json())
    
    
    def predict_sex(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.sex, json={"image": str(img_b64), 'ip_address': "cctv-005-01"})
        return SexInfo(**response.json())
        
    def predict_dfa(self, texts):
        response = requests.post(self.dfa, json={"texts": texts})
        print(response.json())
        return TextInfo(**requests.post(self.dfa, json={"text": texts}).json())
    
    def predict_all(self, path):
        reponse = requests.post(self.all, json={"image": read_b64(path), 'ip_address': "cctv-005-01"})
        return reponse.json()


if __name__ == "__main__":
    fps = [ "/Users/wanghuan/Projects/anomaly/client/tests/sex.png", "/Users/wanghuan/Projects/anomaly/client/tests/test.png",]#"./tests/sex.png",
    
    for fp in fps:

        print("Image: ", fp)
        m = BackendClient()
        res = m.predict_ocr(fp)
        print("OCR Result:")
        print(res)
        print("\n")

        print("Window Result:")
        res = m.predict_window(fp)
        print(res)
        print("\n")

        print("Sex Result:")
        res = m.predict_sex(fp)
        print(res)
        print("\n")

        
        all_result = m.predict_all(fp)
        print(all_result)