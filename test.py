#!/usr/bin/python3
# coding: utf-8

import pytesstrain
import pytesseract
import os
import argparse
from PIL import Image, ImageOps, ImageEnhance
from cv2 import cv2
import re

## TRIENAR FONTE
# https://www.youtube.com/watch?v=TpD76k2HYms
# http://www.fontsaddict.com/font/deluxefont-regular.html
# https://stackoverflow.com/questions/56362144/how-can-i-add-a-new-font-to-tesseract-4-0
# https://towardsdatascience.com/simple-ocr-with-tesseract-a4341e4564b6

# https://pretius.com/blog/ocr-tesseract-training-data/
# https://nanonets.com/blog/ocr-with-tesseract/

img_src = r'number.png'
img = Image.open(img_src)
text = pytesseract.image_to_string(img)
saldoApurado = re.sub("[^\d\.]", "", text)
print(text)

# print(pytesseract.image_to_boxes(img))

# img = cv2.imread('number.png')
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# print(pytesseract.image_to_string(img_rgb))
# # OR
# img_rgb = Image.frombytes('RGB', img.shape[:2], img, 'raw', 'BGR', 0, 0)
# print(pytesseract.image_to_string(img_rgb))


##
# https://gist.github.com/lobstrio/8010d0a21c48b8c807f0c3820467ee0c
# image = Image.open('number.png').convert('RGB')
# image = ImageOps.autocontrast(image)

# filename = "{}.png".format(os.getpid())
# image.save(filename)

# text = pytesseract.image_to_string(Image.open(filename))
# print(text)

###
# https://nanonets.com/blog/ocr-with-tesseract/

# img = cv2.imread('number.png')

# h, w, c = img.shape
# boxes = pytesseract.image_to_boxes(img) 
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# cv2.imshow('img', img)
# cv2.waitKey(0)

### 
# python3 -m pip install --upgrade Pillow

# python3 -m pip install pytesseract

# python3 -m pip install pytesstrain

# brew install pytesseract
# brew install tesseract
# brew install tesseract-lang
# brew install imagemagick --with-fontconfig

# https://stackoverflow.com/questions/58129505/tesseract-training-finetuning-characters
