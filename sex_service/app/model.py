import logging

logger = logging.getLogger(__name__)

import os

os.environ['TFHUB_CACHE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/tfhub_modules")
from typing import Dict

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from pydantic import BaseModel


class SexInfo(BaseModel):
    sex_model_result:Dict[str,float]

def _preprocessing(img:np.ndarray):
    img = Image.fromarray(img)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img = img.resize((224, 224))
    img = np.array(img) / 255.
    return img

model_fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/nsfw_model.h5")

def _load_model(model_path=model_fp):
    
    if model_path is None or (not os.path.exists(model_path)):
        raise ValueError("Unable to load model from model path")

    print("Loading sex model")
    model = tf.keras.models.load_model(model_path, custom_objects={
                                    'KerasLayer': hub.KerasLayer})
    print("Loading sex model done.")

    return model
 
def _predict(model, nd_images):
    """ Classify given a model, image array (numpy)...."""

    model_preds = model.predict(nd_images)
    # preds = np.argsort(model_preds, axis = 1).tolist()

    categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

    probs = []
    for i, single_preds in enumerate(model_preds):
        single_probs = {}
        for j, pred in enumerate(single_preds):
            single_probs[categories[j]] = round(float(pred), 6) * 100
        probs.append(single_probs)
    return probs


class SexDetector():
    def __init__(self):
        self.model = _load_model()

    def predict(self, img):
        img = _preprocessing(img)
        img = np.array([img])
        return SexInfo(sex_model_result = _predict(self.model, img)[0])
