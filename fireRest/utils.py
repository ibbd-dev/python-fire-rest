# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2019年09月04日 星期三 09时31分18秒
import io
import cv2
import base64
import json
from PIL import Image
import numpy as np


def base64_cv2(pic):
    """将base64格式的图片转换为cv2格式"""
    tmp = pic.split(',')[0]
    pic = pic[len(tmp)+1:]
    pic = base64.b64decode(pic)
    pic = Image.open(io.BytesIO(pic))
    if 'png' in tmp:   # 先转化为jpg
        bg = Image.new("RGB", pic.size, (255, 255, 255))
        bg.paste(pic, pic)
        pic = bg

    return cv2.cvtColor(np.asarray(pic), cv2.COLOR_RGB2BGR)


def cv2_base64(img, format='JPEG'):
    """将cv2格式的图像转换为base64格式"""
    out_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    output_buffer = io.BytesIO()
    out_img.save(output_buffer, format='JPEG')
    binary_data = output_buffer.getvalue()
    return str(base64.b64encode(binary_data), encoding='utf8')


class RestEncoder(json.JSONEncoder):
    """
    使用：json.dumps(data, cls=RestEncoder)
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, np.bool_):
            return bool(obj)

        return json.JSONEncoder.default(self, obj)
