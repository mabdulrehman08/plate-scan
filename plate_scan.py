"""CPU-only food detection with deliberately approximate nutrition."""
import argparse
import json
from pathlib import Path

from ultralytics import YOLO


def confidence(value):
    value = float(value)
    if not 0 <= value <= 1:
        raise argparse.ArgumentTypeError('confidence must be between 0 and 1')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('--min-conf', type=confidence, default=0.25)
    args = parser.parse_args()
    if not args.image.is_file():
        parser.error('image must be an existing local file')
    nutrition = json.loads(Path(__file__).with_name('nutrition.json').read_text())
    result = YOLO('yolov8n.pt').predict(str(args.image), device='cpu',
                                      conf=args.min_conf, verbose=False)[0]
    height, width = result.orig_shape
    print('PLATE SCAN | rough estimate, not a measurement')
    print('Item          Conf  Portions   kcal  Protein')
    calories = protein = 0.0
    count = 0
    for box in result.boxes:
        name = result.names[int(box.cls.item())]
        if name not in nutrition:
            continue
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        # Arbitrary demo reference: 20% of the image is one serving.
        portions = max(0.25, min(3.0, ((x2-x1)*(y2-y1)/(width*height))/0.20))
        row = nutrition[name]
        kcal, grams = row['calories']*portions, row['protein_g']*portions
        calories += kcal
        protein += grams
        count += 1
        print(f'{name:<13} {box.conf.item():.2f}  {portions:>7.2f} {kcal:>6.0f} {grams:>6.1f} g')
    if not count:
        print('No supported food detected; nutrition is unknown.')
    else:
        print(f'TOTAL                         {calories:>6.0f} {protein:>6.1f} g')
    output = Path('outputs') / (args.image.stem + '_annotated.jpg')
    output.parent.mkdir(exist_ok=True)
    result.save(filename=str(output))
    print(f'Annotated image: {output.as_posix()}')


if __name__ == '__main__':
    main()
