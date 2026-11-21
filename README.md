# plate-scan

A small Cal AI-inspired Python CLI: local YOLOv8n detects objects on CPU,
filters the ten supported COCO food classes, estimates portions from bounding
box area, and prints calories/protein alongside an annotated photo. No API keys.

## Quickstart

Tested with Windows Python 3.13.1.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python plate_scan.py samples/bus.jpg
python plate_scan.py samples/zidane.jpg --min-conf 0.3
```

The first run downloads yolov8n.pt (internet required once); subsequent inference
is local. Outputs go to outputs/<image-stem>_annotated.jpg and overwrite that path
on repeat runs. Weights are gitignored. Annotations show all detected classes;
only supported food contributes to nutrition.

## Nutrition model

nutrition.json contains illustrative per-serving calories and protein for banana,
apple, orange, broccoli, carrot, pizza, donut, cake, sandwich, and hot dog.
Values are rounded demo assumptions, not a validated nutrition database.
One serving is arbitrarily 20% of image area; portions are box area divided by
that reference, clamped to 0.25-3.0. Confidence is a detection score, not nutrition
certainty. Perspective and cropping can change estimates for the same meal.

## Real output

Both commands above were actually run on CPU. Neither public sample contains
supported food, so the honest result is unknown, not a zero-calorie meal.

```text
$ python plate_scan.py samples/bus.jpg
PLATE SCAN | rough estimate, not a measurement
Item          Conf  Portions   kcal  Protein
No supported food detected; nutrition is unknown.
Annotated image: outputs/bus_annotated.jpg

$ python plate_scan.py samples/zidane.jpg
PLATE SCAN | rough estimate, not a measurement
Item          Conf  Portions   kcal  Protein
No supported food detected; nutrition is unknown.
Annotated image: outputs/zidane_annotated.jpg
```

These runs validate inference, filtering and annotation; they do not validate
food recognition or calorie accuracy. Try a local food photo to exercise the
nutrition rows. No personal photos were used.

## Production limitations

Cal AI's real problem needs volume estimation (depth, scale references or multiple
views), fine-grained food and ingredient classifiers, mixed-dish segmentation,
recipe and cooking-method understanding, and user correction. Box area is not
mass; hidden ingredients and oils are invisible. Missing detections can make a
partial total misleading. Serving assumptions need calibrated ground truth and
uncertainty ranges. This demo is not dietary or medical advice.

An iOS implementation needs Core ML conversion, quantization, device-specific
latency/memory/thermal testing, camera orientation and preprocessing parity,
privacy controls, and a responsive AVFoundation/SwiftUI capture pipeline.
Ultralytics licensing should be reviewed before product distribution.

Muhammad Abdulrehman ships SwiftUI/AVFoundation camera pipelines (Stitch
capture-to-share flow, user growth 800 to 1200) and trains YOLO/RF-DETR detectors
at Drexel's McDonald Lab - both halves of Cal AI's stack.

## Sample provenance

Public Ultralytics demo images, not personal photos:
- https://ultralytics.com/images/bus.jpg
- https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/zidane.jpg

Upstream model/code and sample licensing remains with its respective owners.
