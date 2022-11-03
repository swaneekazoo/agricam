import os
import subprocess

import torch

# Train YOLOv5s on COCO128 for 3 epochs
subprocess.run(args=['python', 'yolov5/train.py', '--img', '640', '--batch', '128', '--epochs', '300', '--data', 'datasets/yolo/data.yaml', '--weights', 'yolov5s.pt'])

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
for f in os.listdir('/Users/adam/git/agricam/data/video/clean thermal/norm/frames'):
    # Images
    img = f'/Users/adam/git/agricam/data/video/clean thermal/norm/frames/{f}'

    # Inference
    results = model(img)

    # Results
    crops = results.crop()  # or .show(), .save(), .crop(), .pandas(), etc.
    imgs = []
    for c in crops:
        imgs.append(c.im)


