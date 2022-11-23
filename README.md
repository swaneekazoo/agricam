# Agricam
Automatically read temperatures of individual livestock to provide early warning for illness. **monday.com** board at https://thermafy-group.monday.com/boards/3049767712

## Files

### best.pt
Weights for a YOLOv5l model trained on a sample of the `clean thermal` dataset

### `renamer.py`
1. Read optical or thermal images (depending on value of `--therm`) from `--in`
2. Perform OCR on the timestamps using Tesseract
3. Rename files in `--in` accordingly

### `video.py` and `frames.py`
Contain routines for video and still image data.

### `video_to_frames.py`
1. Read videos from `--in`
2. Concatenate into a single video
3. Split into frames and write to `--out`
4. ~~Sort frames by-cow, and by train and test according to `--test_split`~~

### `frames_to_labels.py`
1. Read frames from `--in` (thermal images)
2. For each frame, perform Otsu thresholding and return the bounding boxes of the two biggest contours
3. Transform bounding boxes so they apply to the corresponding optical image
4. Write the resulting bounding boxes in YOLO .txt annotation format to `--out`

### `video_to_demo.py`
Process recording of optical & thermal images side-by-side, superimposing bounding boxes obtained by Otsu thresholding (thermal) and YOLO inference (normal).
