import argparse
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


path = 'data/pictures/05.08.22/therm/'
for f in os.listdir(path):
    if f[-4:] == '.jpg':
        print(path + f)
        text = get_text(filename=path + f, therm=True)
        text = text.replace(':', '')
        text = text.replace(' ', '_')
        text = text.strip()
        print(text)
        os.rename(path + f, path + text + '.jpg')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reads optical (`--therm 0`) or thermal (`--therm 1`) images from `--input`, performs Tesseract OCR on the timestamps, and renames files accordingly. \
                                                    Example: \n \
                                                    python renamer.py -i Images_Blutac/train -t 1 ')
    parser.add_argument('-i', '--input', help='the dataset ')
    parser.add_argument('dest')
    parser.add_argument('test_split')
    args = parser.parse_args()

    concat_video(args.src)
    video_to_frames(f'{args.src}/video.mp4', args.src)
    frames_to_dataset(f'{args.src}/frames', args.dest, float(args.test_split))
