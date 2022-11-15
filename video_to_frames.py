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


def video_to_frames(video_src: str, src: str):
    makedirs(f'{src}', exist_ok=True)
    subprocess.run(args=['ffmpeg', '-i', f'{video_src}', '-vf', f'fps={FPS}', f'{src}/%04d.png'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src')
    parser.add_argument('-d', '--dest')
    parser.add_argument('-t', '--test_split')
    args = parser.parse_args()

    concat_video(args.src)
    video_to_frames(f'{args.src}/video.mp4', f'{args.src}/frames')
    # frames_to_dataset(f'{args.src}/frames', args.dest, float(args.test_split))
