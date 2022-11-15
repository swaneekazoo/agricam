import os
from random import seed, random
from os import makedirs, listdir
from os.path import exists, isdir
import random
from shutil import copy
import argparse
import subprocess

import torch
from cv2 import imwrite

FRAMES_ONSCREEN = 227.3
FRAME_RATE = 25
FPS = 2
TIME_ONSCREEN = (FRAMES_ONSCREEN / FRAME_RATE) * FPS


def frames_to_dataset(frames_src: str, dest: str, test_split: float):
    cow_num = 0
    seed(0)
    frames = sorted((f for f in listdir(frames_src) if not f.startswith(".") and not isdir(f'{frames_src}/{f}')), key=str.lower)
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


# def frame_to_face(frame):
#     # Model
#     model = torch.hub.load(repo_or_dir='ultralytics/yolov5', model='custom', path='best.pt')
#     for f in os.listdir('/Users/adam/git/agricam/data/video/clean thermal/norm/frames'):
#         # Images
#         img = f'/Users/adam/git/agricam/data/video/clean thermal/norm/frames/{f}'

#         # Inference
#         results = model(img)

#         # Results
#         crops = results.crop()  # or .show(), .save(), .crop(), .pandas(), etc.
#         imgs = []
#         for c in crops:
#             imgs.append(c.im)