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
            
class AnomalyClient:
    
    def __init__(self):
        self.window = "http://localhost:8043/image/window"
        self.ocr    = "http://localhost:8041/image/ocr"
        self.sex    = "http://localhost:8042/image/sex"
        self.dfa    = "http://localhost:8040/text/dfa"
        
    def predict_ocr(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.ocr, json={"content": str(img_b64)})
        return OcrResponse(**response.json())
    
    def predict_window(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.window, json={"content": str(img_b64)})
        return AbnWindowInfo(**response.json())
    
    
    def predict_sex(self, path):
        img_b64 = read_b64(path)
        response = requests.post(self.sex, json={"content": str(img_b64)})
        return SexInfo(**response.json())
        
    def predict_dfa(self, texts):
        return TextInfo(**requests.post(self.dfa, json={"texts": texts}).json())


if __name__ == "__main__":
    fps = [ "/Users/wanghuan/Projects/anomaly/client/tests/sex.png", "/Users/wanghuan/Projects/anomaly/client/tests/test.png",]#"./tests/sex.png",
    
    for fp in fps:

        print("Image: ", fp)
        m = AnomalyClient()
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
