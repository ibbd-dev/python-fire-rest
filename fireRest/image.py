# -*- coding: utf-8 -*-
#
# 图像格式处理相关函数
# Author: alex
# Created Time: 2019年09月04日 星期三 09时31分18秒
import re
import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO


def base64_cv2(b64):
    """将base64格式的图片转换为cv2格式"""
    tmp = b64.split(',')[0]
    b64 = b64[len(tmp)+1:]
    b64 = base64.b64decode(b64)
    img = Image.open(BytesIO(b64))
    if 'png' in tmp:   # 先转化为jpg
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, img)
        img = bg

    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def cv2_base64(img, format='JPEG'):
    """将cv2格式的图像转换为base64格式"""
    out_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    output_buffer = BytesIO()
    out_img.save(output_buffer, format=format)
    binary_data = output_buffer.getvalue()
    return str(base64.b64encode(binary_data), encoding='utf8')


def base64_pil(b64):
    """将图片从base64格式转换为PIL格式"""
    base64_data = re.sub('^data:image/.+;base64,', '', b64)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    return Image.open(image_data)


def pil_base64(img, format='JPEG'):
    """将PIL图片转换为base64格式"""
    buf = BytesIO()
    img.save(buf, format=format)
    binary_data = buf.getvalue()
    return str(base64.b64encode(binary_data), encoding='utf8')


def cv2_pil(img):
    """将图片从cv2转换为PIL格式"""
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def pil_cv2(img):
    """将图片从PIL转换为cv2格式"""
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
