import pytesseract
import cv2 as cv
import os

TESS_DAT = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

img = cv.imread("number.png")

gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
thr = cv.threshold(gry, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

# cv.imshow("Image", thr)
# cv.waitKey(0)

res = pytesseract.image_to_string(thr, lang="BombFont", config=f"--tessdata-dir {TESS_DAT} --psm 6 -c tessedit_char_whitelist=0123456789").split()[0]

print(res)