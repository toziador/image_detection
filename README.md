# image_detection

Detects relevant presence in an image set.

## detect_images.py

This script scans a directory (recursively) for images, runs YOLOv5 object detection and copies images containing persons, cars or animals to `var/detections/DATE`.
All detected images from a run are placed directly inside that directory (the
input directory structure is not recreated).

### Installation

Install or upgrade the `ultralytics` package (which provides YOLOv5):

```bash
pip install -U ultralytics
```

The script expects a recent YOLOv5 release such as v7.0.

### Usage

```bash
python3 detect_images.py /path/to/images
```

The results will be stored in `var/detections/YYYY-MM-DD-hh-mm-ss` and all
copied images will be saved in that folder.
