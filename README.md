# image_detection

Detects relevant presence in an image set.

## detect_images.py

This script scans a directory (recursively) for images, runs YOLOv5 object detection and copies images containing persons, cars or animals to `/var/detection/DATE`.

### Usage

```bash
python3 detect_images.py /path/to/images
```

The results will be stored in `/var/detection/YYYY-MM-DD-hh-mm-ss`.
