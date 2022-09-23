#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/20 11:12 
# @Author : hesgang
# @File : QRcode.py 

import sys

from typing import List
from Tea.core import TeaCore
import os
from alibabacloud_imm20170906.client import Client as imm20170906Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_imm20170906 import models as imm_20170906_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient
import configparser  # 读取配置文件的包
from PIL import Image, ImageGrab
import oss2
import cv2


def read_cfg():
    config = configparser.ConfigParser()
    try:
        # 读取私有配置
        path = os.path.join(os.getcwd(), 'my_cfg.ini')
        config.read(path, encoding="utf-8")
        _AK = config.get('AK', 'AK')
        _AS = config.get('AK', 'AS')
        return {'AK': _AK, 'AS': _AS}
    except BaseException:
        path = os.path.join(os.getcwd(), 'cfg.ini')
        config.read(path, encoding="utf-8")
        _AK = config.get('AK', 'AK')
        _AS = config.get('AK', 'AS')
        return {'AK': _AK, 'AS': _AS}


class QRcode:
    def __init__(self):
        pass

    @staticmethod
    def get_img():
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            im.save(img_path)
            QRcode.__upload_oss(AK['AK'], AK['AS'])
        else:
            print('ERROR:没有找到图片')
            exit(0)

    @staticmethod
    def __upload_oss(
            access_key_id: str,
            access_key_secret: str,
    ) -> None:
        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        auth = oss2.Auth(access_key_id, access_key_secret)
        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称。
        bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'bj-ocr')

        # 必须以二进制的方式打开文件。
        # 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
        with open(img_path, 'rb') as fileobj:
            # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
            bucket.put_object('QRcode/qrcode.png', fileobj)
            fileobj.close()

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> imm20170906Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        _config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id=access_key_id,
            # 您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        _config.endpoint = f'imm.cn-beijing.aliyuncs.com'
        return imm20170906Client(_config)

    @staticmethod
    def run_cloud(
        args: List,
    ):
        _client = QRcode.create_client(args[0]['AK'], args[0]['AS'])
        detect_image_qrcodes_request = imm_20170906_models.DetectImageQRCodesRequest(
            # ToDo 修改为自己的project和图片地址
            project='ocr',
            image_uri='oss://bj-ocr/QRcode/qrcode.png'
        )
        runtime = util_models.RuntimeOptions()
        resp = _client.detect_image_qrcodes_with_options(detect_image_qrcodes_request, runtime)
        # return UtilClient.to_jsonstring(TeaCore.to_map(resp))
        return TeaCore.to_map(resp)
        # ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))

    @staticmethod
    def run_local():
        QRcode.get_img()
        qrcode_image = cv2.imread(img_path)
        qrCodeDetector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(qrcode_image)
        return data


if __name__ == '__main__':
    os.chdir(r'D:\code\python\Auto Run')
    img_path = r'\cache\qrcode.png'
    AK = read_cfg()
    res = QRcode.run_local()
    if res:
        print(res)
    else:
        res = QRcode.run_cloud([AK])
        if res['body']['QRCodes']:
            print(res['body']['QRCodes'][0]['Content'])
        else:
            print('ERROR:请检查二维码是否正确')


