# image_detection

Detects relevant presence in an image set.

## detect_images.py

This script scans a directory (recursively) for images, runs YOLOv5 object detection and copies images containing persons, cars or animals to `var/detections/DATE`.

### Usage

```bash
python3 detect_images.py /path/to/images
```

The results will be stored in `var/detections/YYYY-MM-DD-hh-mm-ss`.

## usb_images_presence_detector.py

`usb_images_presence_detector.py` detecta personas, coches y animales en las
imágenes ubicadas en unidades externas conectadas a Windows. El script pide al
usuario seleccionar la unidad a analizar y la carpeta donde se almacenarán las
detecciones.

### Uso

```bash
python usb_images_presence_detector.py
```

Al finalizar se muestran estadísticas de las imágenes procesadas y las
detecciones encontradas.
