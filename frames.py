from os import listdir, makedirs
from os.path import isdir

import cv2
import numpy as np
import subprocess
import torch

import os
from random import seed, random
from os import makedirs, listdir
from os.path import exists, isdir
import random
from shutil import copy
import argparse
import subprocess

import torch
from cv2 import imwrite, imread

FRAMES_ONSCREEN = 227.3
FRAME_RATE = 25
FPS = 2
TIME_ONSCREEN = (FRAMES_ONSCREEN / FRAME_RATE) * FPS

NORM_W = 2688
NORM_H = 1520
THERM_W = 1280
THERM_H = 720
NORM_BOX_X = 650
NORM_BOX_Y = 131
THERM_BOX_X = 33
THERM_BOX_Y = 18
NORM_BOX_W = 1657
NORM_BOX_H = 1262
THERM_BOX_W = 1211
THERM_BOX_H = 688

SCALE_W = NORM_W / THERM_W
SCALE_H = NORM_H / THERM_H
NORM_CENTRE_X = NORM_W / 2
NORM_CENTRE_Y = NORM_H / 2
THERM_CENTRE_X = THERM_W / 2
THERM_CENTRE_Y = THERM_H / 2
NORM_BOX_CENTRE_X = NORM_BOX_W / 2 + NORM_BOX_X
NORM_BOX_CENTRE_Y = NORM_BOX_H / 2 + NORM_BOX_Y
THERM_BOX_CENTRE_X = THERM_BOX_W / 2 + THERM_BOX_X
THERM_BOX_CENTRE_Y = THERM_BOX_H / 2 + THERM_BOX_Y

THERM_BOX_SCALED_CENTRE_X = THERM_BOX_CENTRE_X * SCALE_W
THERM_BOX_SCALED_CENTRE_Y = THERM_BOX_CENTRE_Y * SCALE_H
BOX_CENTRE_OFFSET_X = NORM_BOX_CENTRE_X - THERM_BOX_SCALED_CENTRE_X
BOX_CENTRE_OFFSET_Y = NORM_BOX_CENTRE_Y - THERM_BOX_SCALED_CENTRE_Y
SCALE_BOX_W = NORM_BOX_W / (THERM_BOX_W * SCALE_W)
SCALE_BOX_H = NORM_BOX_H / (THERM_BOX_H * SCALE_H)

MODEL = torch.hub.load(repo_or_dir='ultralytics/yolov5', model='custom', path='best.pt')


def frame_to_contours(frame):
    img = cv2.imread(frame, 0)

    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Generate intermediate image; use morphological closing to keep parts of the cow together
    inter = cv2.morphologyEx(th, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

    # Find 2 largest contours in intermediate image
    cnts, _ = cv2.findContours(inter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=lambda c: cv2.contourArea(c), reverse=True)
    cnts = cnts[:2]

    return cnts


def draw_bounding_box(frame, cnts, dest):
    frame = imread(frame)
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
    print(f'Writing to {dest}')
    imwrite(dest, frame)


def frame_to_annotation(frame, dest):
    """
    Use `frame` (thermal) to generate YOLO-compliant label file for the corresponding normal frame, saving to `dest`.
    """

    makedirs(dest, exist_ok=True)
    cnts = frame_to_contours(frame)
    with open(f'{dest}/{frame.split(".")[0]}.txt', 'w') as text_file:
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            x, y, w, h = transform_bounding_rect(frame, x, y, w, h)
            # Convert to proportion of image size
            x /= NORM_W
            y /= NORM_H
            w /= NORM_W
            h /= NORM_H
            text_file.write(f'0 {x} {y} {w} {h}\n')


def run_inference(img, dest):
    results = MODEL(img)
    results.save(save_dir=dest)


def transform_bounding_rect(img, x, y, w, h):
    """
    Transform `x`, `y`, `w`, and `h` of bounding rectangle from a thermal image to match the corresponding optical image
    """

    frame = cv2.imread(f'/Users/adam/Git/agricam/data/video/clean thermal/norm/frames/{img}', 0)

    # x, y, w, h * 2.1
    x = round(x * SCALE_W)
    y = round(y * SCALE_H)
    w = round(w * SCALE_W)
    h = round(h * SCALE_H)

    # x, y - centre
    x -= NORM_CENTRE_X
    y -= NORM_CENTRE_Y

    # x,y,w,h * box scale
    x = round(x * SCALE_BOX_W)
    y = round(y * SCALE_BOX_H)
    w = round(w * SCALE_BOX_W)
    h = round(h * SCALE_BOX_H)

    # x, y - centre
    x = round(x + NORM_CENTRE_X)
    y = round(y + NORM_CENTRE_Y)

    # x, y + box centre offset
    x += round(BOX_CENTRE_OFFSET_X)
    y += round(BOX_CENTRE_OFFSET_Y)

    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 10)
    # cv2.imwrite(f'/Users/adam/git/agricam/data/video/clean thermal/norm/frames/2/{img}', frame)

    # x, y = box centre
    x += w / 2
    y += h / 2

    return x, y, w, h


def frames_to_dataset(frames_src: str, dest: str, test_split: float):
    cow_num = 0
    seed(0)
    frames = sorted((f for f in listdir(frames_src) if not f.startswith(".") and not isdir(f'{frames_src}/{f}')),
                    key=str.lower)
    model = torch.hub.load(repo_or_dir='ultralytics/yolov5', model='custom', path='best.pt')
    for i, frame in enumerate(frames):
        subset = random.random()
        imgs = []
        results = model(frame)
        crops = results.crop()
        for crop in crops:
            imgs.append(crop.im)
        if i % round(TIME_ONSCREEN) == 0:
            cow_num += 1
            print(f'Cow {cow_num}')
            makedirs(f'{dest}/train/cow{cow_num}', exist_ok=True)
            makedirs(f'{dest}/test/cow{cow_num}', exist_ok=True)
        if subset < 1 - test_split:
            # copy(f'{frames_src}/{frame}', f'{dest}/train/cow{cow_num}')  # Copy image to the appropriate directory
            for img in imgs:
                imwrite(f'{dest}/train/cow{cow_num}', img)  # Write cow face to the appropriate directory
        else:
            # copy(f'{frames_src}/{frame}', f'{dest}/test/cow{cow_num}')  # Copy image to the appropriate directory
            for img in imgs:
                imwrite(f'{dest}/test/cow{cow_num}', img)  # Write cow face to the appropriate directory
