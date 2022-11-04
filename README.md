# Agricam
Automatically read temperatures of individual livestock to provide early warning for illness. **monday.com** board at https://thermafy-group.monday.com/boards/3049767712

## Components

### 1. renamer
1. Read optical or thermal (depending on `--therm`) from `--in`
2. Perform OCR on the timestamps using Tesseract
3. Rename files accordingly

### 2. video_to_frames
1. Read videos from `--in`
2. Concatenate into a single video
3. Split into frames and write to `--out`
4. ~Sort frames by-cow, and by train and test according to `--test_split`~

### 3. frames_to_annotations
1. Read frames from `--in` (thermal images)
2. For each frame, perform Otsu thresholding and return the bounding boxes of the two biggest contours
3. Transform bounding boxes so they apply to the corresponding optical image
4. Write the resulting bounding boxes in YOLO annotation format to .txt files in `--out`

### 4. frames_to_faces
1. Read images from `--in`
2. For each image, run YOLO inference and write the cropped faces to `--out`. Sort faces by-cow, and by train and test according to `--test_split`.
