import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from pydantic import BaseModel
import os

class AbnWindowInfo(BaseModel):
    confidence:float
    is_abnormal:bool

SHAPE = (224,224,3)

VGG_WEIGHTS_FP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/vgg16_weights_tf_dim_ordering_tf_kernels.h5")

class WindowModel(tf.keras.models.Model):
    def __init__(self):
        super().__init__()

        self.vgg = VGG16(weights = VGG_WEIGHTS_FP, include_top = True, input_shape = SHAPE)
        self.vgg = tf.keras.models.Model(self.vgg.input, self.vgg.layers[-3].output)
        self.vgg.trainable = False
        self.act = tf.keras.layers.Activation('relu')
        self.dense1 = tf.keras.layers.Dense(512, activation='relu')
        self.dense2 = tf.keras.layers.Dense(128, activation='relu')
        self.out_dense = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, inp, training = True):
        x = preprocess_input(inp)
        x = tf.keras.layers.GaussianNoise(0.1)(x)
        x = self.vgg(x)

        if training:

            noise = tf.zeros_like(x)
            noise = tf.keras.layers.GaussianNoise(0.1)(noise)

            concat = tf.concat([x, noise], axis=0)
            x = self.act(concat)

        x = self.dense1(x)
        x = self.dense2(x)
        return self.out_dense(x)

WEIGHTS_FP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/window_weights.h5")

if not os.path.exists(WEIGHTS_FP):
    raise FileNotFoundError(f"Could not find weights file at {WEIGHTS_FP}")

def load_model(weights = WEIGHTS_FP):
    newmodel = WindowModel()
    newmodel(np.random.random((1,224,224,3)))
    newmodel.load_weights(weights)
    return newmodel

def _preprocessing(img:np.ndarray):
    img = Image.fromarray(img)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img = img.resize((224, 224))
    return np.array(img)

class AbnormaWindowDetect():
    def __init__(self, *args, **kwargs):
        self.model = load_model()

    def predict(self, img):
        img = _preprocessing(img)
        result = self.model(np.array([img]), training = False)

        is_abnormal = np.argmax(result.numpy(),axis = -1)[0]
        confidence = np.max(result)

        return AbnWindowInfo(confidence=confidence, is_abnormal=is_abnormal)
