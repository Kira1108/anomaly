import logging

logging.basicConfig(level = logging.INFO)
from typing import List, Union

import numpy as np
from paddleocr import PaddleOCR
from pydantic import BaseModel

class BboxInfo(BaseModel):
    text: str
    confidence: float = None
    topleft: List = None
    topright: List = None
    bottomright: List = None
    bottomleft: List = None
    
class OcrResponse(BaseModel):
    result: List[BboxInfo]

class Ocr:
    """
    Usage: 
        img = np.array(img)
        ocr = Ocr()
        ocr.get_box(img)
    """
    def __init__(self, use_gpu=False):
        logging.info("Loading paddleocr model...")
        self.detector = PaddleOCR(use_angle_cls=False, use_gpu=use_gpu, lang = 'ch')

    def cvt_bbox(self, line):
        topleft, topright, bottomright, bottomleft \
            = np.array(line[0]).astype(np.int32).tolist()

        text, confidence = line[1]

        return BboxInfo(topleft=topleft,
                        topright=topright,
                        bottomright=bottomright,
                        bottomleft=bottomleft,
                        text=text,
                        confidence=confidence)

    def get_box(self, img:Union[np.ndarray, str]) -> OcrResponse:
        logging.info("Ocr processing...")
        result = self.detector.ocr(img)
        logging.info("Ocr done.")
        return OcrResponse(result = [self.cvt_bbox(line) for line in result])

    def get_texts(self, img:Union[np.ndarray, str]) -> List[str]:
        return [bbox.text for bbox in self.get_box(img)]