import argparse
from os import listdir
from os.path import isdir

from frames import frame_to_annotation

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Frames to labels')
    parser.add_argument('-s', '--src', help='Input directory containing video frames (thermal)')
    parser.add_argument('-d', '--dest', help='Output directory for label files')
    args = parser.parse_args()

    frames = sorted((f for f in listdir(args.src) if not (f.startswith(".") or isdir(f'{args.src}/{f}'))),
                    key=str.lower)
    for f in frames:
        frame_to_annotation(f, args.dest)
