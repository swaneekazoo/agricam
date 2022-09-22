import cv2
import os
import numpy as np
from pytesseract import image_to_string


def get_text(filename: str, therm: bool):
    # Read image
    img: np.ndarray = cv2.imread(filename)
    # Crop
    img = img[20:100, 20:620] if therm else img[40:140, 40:820]
    # Threshold
    HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(HSV_img)
    v = cv2.GaussianBlur(v, (1,1), 0)
    thresh = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(1, 1))
    thresh = cv2.dilate(thresh, kernel)
    # Return text
    txt = image_to_string(thresh, config='-c page_separator=''')
    return txt


path = 'data/pictures/05.08.22/norm/'
for f in os.listdir(path):
    if f[-4:] == '.jpg':
        print(path + f)
        text = get_text(filename=path + f, therm=False)
        text = text.replace(':', '')
        text = text.replace(' ', '_')
        text = text.strip()
        print(text)
        os.rename(path + f, path + text + '.jpg')


# path = 'data/pictures/05.08.22/therm/'
# for f in os.listdir(path):
#     if f[-4:] == '.jpg':
#         print(f)
#         text = get_text(filename=path + f, therm=True)
#         print(text)
#         os.rename(path + f, path + text.replace(' ', '_') + '.jpg')
