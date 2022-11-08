#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/20 11:12 
# @Author : hesgang
# @File : QRcode.py 

import sys

from typing import List
import os
import configparser  # 读取配置文件的包
from PIL import Image, ImageGrab
import cv2
from ocr import AipOcr


def read_cfg():
    config = configparser.ConfigParser()
    try:
        # 读取私有配置
        path = os.path.join(os.getcwd(), 'my_cfg.ini')
        config.read(path, encoding="utf-8")
        _appId = config.get('baidu', 'appId')
        _apiKey = config.get('baidu', 'apiKey')
        _secretKey = config.get('baidu', 'secretKey')
        return {'appId': _appId, 'apiKey': _apiKey, 'secretKey': _secretKey}
    except BaseException:
        path = os.path.join(os.getcwd(), 'cfg.ini')
        config.read(path, encoding="utf-8")
        _appId = config.get('baidu', 'appId')
        _apiKey = config.get('baidu', 'apiKey')
        _secretKey = config.get('baidu', 'secretKey')
        return {'appId': _appId, 'apiKey': _apiKey, 'secretKey': _secretKey}


def get_img():
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        im.save(img_path)
        with open(img_path, 'rb') as fp:
            return fp.read()
    else:
        print('ERROR:没有找到图片')
        exit(0)


def run_local():
    qrcode_image = cv2.imread(img_path)
    qrCodeDetector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(qrcode_image)
    return data


if __name__ == '__main__':
    img_path = r'\cache\qrcode.png'
    img = get_img()
    AK = read_cfg()
    QR = AipOcr(AK['appId'], AK['apiKey'], AK['secretKey'])
    res = run_local()
    if res:
        print(res)
    else:
        res = QR.qrcode(img)
        print(res['codes_result'])
        if res['codes_result']:
            print(res['codes_result'][0]['text'][0])
        else:
            print('ERROR:请检查二维码是否正确')


