#!/usr/bin/env python3
"""USB Images Presence Detector.

Scans external drives on Windows, runs object detection on all images and
copies those containing persons, cars or animals to a user defined
output directory.
"""

import argparse
import ctypes
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

DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3


def get_external_drives():
    """Return list of drive letters for external drives."""
    drives = []
    system_drive = os.getenv('SystemDrive', 'C:\\')
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for i in range(26):
        if bitmask & (1 << i):
            drive = f"{chr(65 + i)}:\\"
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(drive))
            if drive_type == DRIVE_REMOVABLE or (drive_type == DRIVE_FIXED and drive != system_drive):
                drives.append(drive)
    return drives


def choose_drive(drives):
    """Prompt the user to choose a drive from the list."""
    if not drives:
        raise SystemExit('No external drives found.')
    if len(drives) == 1:
        print(f'Using drive: {drives[0]}')
        return drives[0]
    print('Available drives:')
    for idx, d in enumerate(drives, start=1):
        print(f'{idx}) {d}')
    while True:
        choice = input('Select drive number to analyze: ')
        try:
            idx = int(choice)
            if 1 <= idx <= len(drives):
                return drives[idx - 1]
        except ValueError:
            pass
        print('Invalid selection.')


def ask_output_directory() -> Path:
    path = input('Enter output directory path: ').strip()
    out_dir = Path(path).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def is_image(filename: str) -> bool:
    return filename.lower().endswith(
        ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    )


def detect_images(root_dir: Path, out_dir: Path, conf: float):
    print('Loading model...')
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.conf = conf

    processed = 0
    skipped = 0
    car_detections = 0
    person_detections = 0
    animal_detections = 0

    for root, _, files in os.walk(root_dir):
        for file in files:
            if not is_image(file):
                continue
            img_path = Path(root) / file
            processed += 1
            try:
                results = model(str(img_path))
            except UnidentifiedImageError:
                print(f'Skipping {img_path}: cannot identify image')
                skipped += 1
                continue
            labels = results.pandas().xyxy[0]['name'].tolist()
            detected = False
            if any(l in PERSON_CLASSES for l in labels):
                person_detections += 1
                detected = True
            if any(l in CAR_CLASSES for l in labels):
                car_detections += 1
                detected = True
            if any(l in ANIMAL_CLASSES for l in labels):
                animal_detections += 1
                detected = True
            if detected:
                relative = img_path.relative_to(root_dir)
                destination = out_dir / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(img_path, destination)
                print(f'Copied {img_path} -> {destination}')

    print('\n----- Statistics -----')
    print(f'Images processed: {processed}')
    print(f'Images skipped : {skipped}')
    print(f'Images with persons: {person_detections}')
    print(f'Images with cars   : {car_detections}')
    print(f'Images with animals: {animal_detections}')
    print(f'Results stored in: {out_dir}')


def main():
    parser = argparse.ArgumentParser(description='USB Images Presence Detector')
    parser.add_argument(
        '--conf',
        type=float,
        default=0.5,
        help='Confidence threshold for detections'
    )
    args = parser.parse_args()
    drives = get_external_drives()
    drive = choose_drive(drives)
    out_dir = ask_output_directory()
    detect_images(Path(drive), out_dir, args.conf)


if __name__ == '__main__':
    main()
