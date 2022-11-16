import argparse
from video import concat_video, video_to_frames

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src')
    parser.add_argument('-d', '--dest')
    parser.add_argument('-t', '--test_split')
    args = parser.parse_args()

    concat_video(args.src)
    video_to_frames(f'{args.src}/video.mp4', f'{args.src}/frames', 2)