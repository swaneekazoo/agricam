import os
from random import seed, random
from os import makedirs, listdir
from os.path import exists, isdir
import random
from shutil import copy
import argparse
import subprocess


FRAMES_ONSCREEN = 227.3
FRAME_RATE = 25
FPS = 2

time_onscreen = (FRAMES_ONSCREEN / FRAME_RATE) * FPS


def concat_video(src: str):
    files = sorted((f for f in listdir(src) if not f.startswith(".") and f.endswith('.mp4')), key=str.lower)
    print(files)

    exists(f'{src}/video.mp4') and os.remove(f'{src}/video.mp4')
    exists(f'{src}/videos.txt') and os.remove(f'{src}/videos.txt')
    with open(f'{src}/videos.txt', 'w') as txt_file:
        for i, f in enumerate(files):
            txt_file.write(f"file '{src}/{f}'\n")
    subprocess.run(args=[f'ffmpeg', '-f', 'concat', '-safe', '0', '-i', f'{src}/videos.txt', '-c', 'copy', f'{src}/video.mp4'])


def video_to_frames(video_src: str, src: str):
    makedirs(f'{src}/frames', exist_ok=True)
    subprocess.run(args=['ffmpeg', '-i', f'{video_src}', '-vf', f'fps={FPS}', f'{src}/frames/%03d.png'])


def frames_to_dataset(frames_src: str, dest: str, test_split: float):
    cow_num = 0
    seed(0)
    frames = sorted((f for f in listdir(frames_src) if not f.startswith(".") and not isdir(f'{frames_src}/{f}')), key=str.lower)
    for i, frame in enumerate(frames):
        subset = random.random()
        if i % round(time_onscreen) == 0:
            cow_num += 1
            print(f'Cow {cow_num}')
            makedirs(f'{dest}/train/cow{cow_num}', exist_ok=True)
            makedirs(f'{dest}/test/cow{cow_num}', exist_ok=True)
        if subset < 1 - test_split:
            copy(f'{frames_src}/{frame}', f'{dest}/train/cow{cow_num}')
        else:
            copy(f'{frames_src}/{frame}', f'{dest}/test/cow{cow_num}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src')
    parser.add_argument('dest')
    parser.add_argument('test_split')
    args = parser.parse_args()

    concat_video(args.src)
    video_to_frames(f'{args.src}/video.mp4', args.src)
    frames_to_dataset(f'{args.src}/frames', args.dest, float(args.test_split))
