"""
Simply read an image from a path, use are going to use ImageReader directly
"""


import numpy as np
# import cv2
from PIL import Image
# import cairosvg
import io
from dataclasses import dataclass
import base64
import io
import numpy as np


@dataclass
class CommonImageFileReader:
    path: str

    def read(self):
        img = Image.open(self.path)
        img = img.convert('RGB')
        return np.array(img)


# @dataclass
# class SVGFileReader(Reader):
#     path: str

#     def read(self):
#         stream = io.BytesIO(cairosvg.svg2png(url=self.path, ))
#         img = Image.open(stream)

#         background = Image.new("RGB", img.size, (255, 255, 255))
#         background.paste(img, mask=img.split()[3])
#         return np.array(background)


def b64string2numpy(b64string):
    """Convert a base64 encoded string to numpy array
    Args:
        b64string (_type_): string of encoded bytes
        format (str, optional): string of byte
    Returns:
        _type_: np.array
    """
    
    # if isinstance(b64string, str):
    #     b64string = b64string.encode()
    
    buff = io.BytesIO(base64.b64decode(b64string))
    image = Image.open(buff)
    
    image = np.array(image)
    if image.shape[-1] == 4:
        image = image[:, :, :3]
    return image

@dataclass
class Base64Reader:
    content:str
    def read(self):
        return b64string2numpy(self.content)


PROCESSORS = {
    "base64": Base64Reader,
    # "svg": SVGFileReader,clear
    "jpg": CommonImageFileReader,
    "png": CommonImageFileReader,
    "jpeg": CommonImageFileReader,
    "default": CommonImageFileReader
}


@dataclass
class ImageReader:
    '''Pass a path if read a image file, if base64, pass a content'''
    path: str = None
    content: str = None

    def __post_init__(self):
        if self.content:
            filetype = 'base64'
            self.reader = PROCESSORS['base64'](self.content)
        else:
            filetype = self.path.split(".")[-1]
            self.reader = PROCESSORS.get(filetype, PROCESSORS['default'])(self.path)

    def read(self):
        return self.reader.read()
    
    
    
def file2b64(path:str, encode:bool = True):
    """Convert a image file to base64 string, encoded or not
    Args:
        path (_type_): string
        encode (bool, optional): _description_. Defaults to True.
    Raises:
        e: _description_
    Returns:
        b64 string
    """
    
    with open(path, "rb") as img_file:
            
        buffer = base64.b64encode(img_file.read())
        return buffer if encode else buffer.decode()
        
@dataclass
class File2b64Reader:
    path:str
    
    def read(self):
        try:
            return file2b64(self.path)
        except:
            return None
