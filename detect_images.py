#!/usr/bin/env python3
import argparse
import datetime
import os
import shutil
from pathlib import Path

import torch
from PIL import UnidentifiedImageError

ANIMAL_CLASSES = {
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
    'bear', 'zebra', 'giraffe'
}
PERSON_CLASSES = {'person'}
CAR_CLASSES = {'car'}


def parse_args():
    parser = argparse.ArgumentParser(
        description='Detect persons, cars and animals in images and copy them to var/detections/YYYY-MM-DD-hh-mm-ss inside the project directory.'
    )
    parser.add_argument('directory', help='Directory to search for images recursively')
    return parser.parse_args()


def is_image(filename: str) -> bool:
    return filename.lower().endswith((
        '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'
    ))


def main() -> None:
    args = parse_args()
    src_dir = Path(args.directory).resolve()
    if not src_dir.is_dir():
        raise SystemExit(f'{src_dir} is not a valid directory')

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir / 'var' / 'detections' / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    print('Loading model...')
    model = torch.hub.load(
        'ultralytics/yolov5:v7.0', 'yolov5s', pretrained=True
    )

    copied = 0
    for root, _, files in os.walk(src_dir):
        for file in files:
            if not is_image(file):
                continue
            img_path = Path(root) / file
            try:
                results = model(str(img_path))
            except UnidentifiedImageError:
                print(f'Skipping {img_path}: cannot identify image')
                continue
            detected_labels = results.pandas().xyxy[0]['name'].tolist()
            if any(
                label in PERSON_CLASSES
                or label in CAR_CLASSES
                or label in ANIMAL_CLASSES
                for label in detected_labels
            ):
                relative = img_path.relative_to(src_dir)
                destination = out_dir / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(img_path, destination)
                copied += 1
                print(f'Copied {img_path} -> {destination}')

    print(f'Total images copied: {copied}')
    print(f'Results stored in: {out_dir}')


if __name__ == '__main__':
    main()
