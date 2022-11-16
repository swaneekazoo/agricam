from os import listdir, makedirs
from os.path import isdir

import cv2
from cv2 import imread, imwrite

from frames import run_inference, frame_to_contours, draw_bounding_box
from video import video_to_frames, frames_to_video


# # split video into frames
# video_to_frames('data/video/demo/demo.mp4', 'data/video/demo/frames', 25)
#
#
# # split video down the middle
# makedirs('data/video/demo/frames/norm', exist_ok=True)
# makedirs('data/video/demo/frames/therm', exist_ok=True)
# frames = sorted((f for f in listdir('data/video/demo/frames') if not f.startswith(".") and not isdir(f'data/video/demo/frames/{f}')),
#                 key=str.lower)
# for f in frames:
#     img = imread(f'data/video/demo/frames/{f}', 0)
#     norm = img[0:768, 0:512]
#     therm = img[0:768, 512:1024]
#     imwrite(f'data/video/demo/frames/norm/{f}', norm)
#     imwrite(f'data/video/demo/frames/therm/{f}', therm)


# run inference on normal video
makedirs('data/video/demo/frames/norm/boxes', exist_ok=True)
frames = sorted((f for f in listdir('data/video/demo/frames/norm') if not f.startswith(".") and not isdir(f'data/video/demo/frames/norm/{f}')),
                key=str.lower)
for f in frames:
    run_inference(f'data/video/demo/frames/norm/{f}', f'data/video/demo/frames/norm/boxes')


# draw bounding boxes on thermal video
makedirs('data/video/demo/frames/therm/boxes', exist_ok=True)
frames = sorted((f for f in listdir('data/video/demo/frames/therm') if not f.startswith(".") and not isdir(f'data/video/demo/frames/therm/{f}')),
                key=str.lower)
for f in frames:
    cnts = frame_to_contours(f'data/video/demo/frames/therm/{f}')
    draw_bounding_box(f'data/video/demo/frames/therm/{f}', cnts, f'data/video/demo/frames/therm/boxes/{f}')


# reassemble frames
makedirs('data/video/demo/frames/concat', exist_ok=True)
norm_frames = sorted((f for f in listdir('data/video/demo/frames/norm/boxes') if not f.startswith(".") and not isdir(f'data/video/demo/frames/norm/boxes/{f}')),
                key=str.lower)
therm_frames = sorted((f for f in listdir('data/video/demo/frames/therm/boxes') if not f.startswith(".") and not isdir(f'data/video/demo/frames/therm/boxes/{f}')),
                key=str.lower)
for n, t in zip(norm_frames, therm_frames):
    frame_n = cv2.imread(f'data/video/demo/frames/norm/boxes/{n}')
    frame_t = cv2.imread(f'data/video/demo/frames/therm/boxes/{t}')
    frame = cv2.hconcat([frame_n, frame_t])
    imwrite(f'data/video/demo/frames/concat/{n}', frame)

# reassemble videos
# frames_to_video('/Users/adam/Git/agricam/data/video/demo/frames/concat', '/Users/adam/Git/agricam/data/video/demo', 60)