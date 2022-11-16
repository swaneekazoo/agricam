import os
from os import makedirs, listdir
from os.path import exists
import argparse
import subprocess

def concat_video(src: str):
    files = sorted((f for f in listdir(src) if not f.startswith(".") and f.endswith('.mp4')), key=str.lower)
    print(files)
    exists(f'{src}/video.mp4') and os.remove(f'{src}/video.mp4')
    exists(f'{src}/videos.txt') and os.remove(f'{src}/videos.txt')
    with open(f'{src}/videos.txt', 'w') as txt_file:
        for i, f in enumerate(files):
            txt_file.write(f"file '{src}/{f}'\n")
    subprocess.run(args=[f'ffmpeg', '-f', 'concat', '-safe', '0', '-i', f'{src}/videos.txt', '-c', 'copy', f'{src}/video.mp4'])


def video_to_frames(src: str, dest: str, fps: int):
    makedirs(f'{dest}', exist_ok=True)
    subprocess.run(args=['ffmpeg', '-i', f'{src}', '-vf', f'fps={fps}', f'{dest}/%04d.png'])


def frames_to_video(src: str, dest: str, fps: int):
    subprocess.run(args=['ffmpeg', '-framerate', '60', '-i', f'{src}/%05d.jpg', dest])