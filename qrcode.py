# -*-coding=utf-8-*-
import os
import logging
from PIL import Image
import zxing
import random

logger = logging.getLogger(__name__)
if not logger.handlers: logging.basicConfig(level=logging.INFO)
DEBUG = (logging.getLevelName(logger.getEffectiveLevel()) == 'DEBUG')


def ocr_qrcode_zxing(filename):
    # 在当前目录生成临时文件，规避java的路径问题
    img = Image.open(filename)
    ran = int(random.random() * 100000)
    img.save('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))
    zx = zxing.BarCodeReader()
    data = ''
    zxdata = zx.decode('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))
    # 删除临时文件
    os.remove('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))
    if zxdata:
        logger.debug(u'zxing识别二维码:%s,内容: %s' % (filename, zxdata.parsed))
        data = zxdata.parsed
    else:
        logger.error(u'识别zxing二维码出错:%s' % (filename))
        img.save('%s-zxing.jpg' % filename)
    return data


if __name__ == '__main__':
    filename = r'/Users/demon/Desktop/11111.jpg'

    # zxing二维码识别
    # ltext = ocr_qrcode_zxing(filename)
    # logger.info(u'[%s]Zxing二维码识别:[%s]!!!' % (filename, ltext))
    # print(ltext)
    # p = "18302847823  https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + ltext
    rootdir = "/Users/demon/Desktop/images"
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        print(path)
