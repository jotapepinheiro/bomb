#!/usr/bin/python3
# coding: utf-8

import cv2
import pytesseract
import cv2
import numpy as np
import urllib
import requests
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
# TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR'
from PIL import Image, ImageOps, ImageEnhance

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

url='http://jeroen.github.io/images/testocr.png'

img = url_to_image(url)

# img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.medianBlur(img,5) 
retval, img = cv2.threshold(img,150,255, cv2.THRESH_BINARY)
txt = pytesseract.image_to_string(img, lang='eng')
print(txt)