import cv2
import numpy as np
from typing import Tuple

from encoding import Packer, PackTraits

class JpegImage(PackTraits):
    TYPE_NAME   =   'cv::Mat'
    CODE        =   'JP'
    LENGTH      =   -1
    QUALITY     =   90
    @classmethod
    def pack(cls,value: list)->str:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), cls.QUALITY]
        result, buffer = cv2.imencode('.jpg', value, encode_param)
        temp = [
            Packer.pack(len(buffer)),
            buffer
        ]
        return b''.join(temp)
    @classmethod
    def unpack(cls,buffer:str,index:int)->Tuple[int,list]:
        try:
            index, lg = Packer.unpack(buffer,index)
            tmp = buffer[index:(index+lg)]
            mat = cv2.imdecode(np.asarray(tmp),cv2.IMREAD_COLOR)
            return index+lg, mat
        except Exception:
            raise
