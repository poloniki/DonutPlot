import json
from PIL import Image


## write directories for output data from models
donut_output = "path/to/your/file.json"
yolo_output = "path/to/your/file.txt"
image_input = "path/to/your/image.jpg"

## Open Donut data
with open(donut_output, "r") as file:
    DonutData = json.load(file)

## Open Yolo data
with open(yolo_output, "r") as file:
    YoloData = file.read()

## Open Image
img = Image.open(image_input)

## Get the x-ticks

xticks = []
yticks = []
min_confidence = 0.8
for row in YoloData:
    if row[1] < min_confidence:
        print(
            f"Point skipped with confidence {row[1]}< Min conficence:{min_confidence}. Category {row[0]}  Coordinates {row[2:3]}"
        )
    if row[0] == 0:
        xticks.append(row[2], row[3])
    if row[0] == 1:
        yticks.append(row[2], row[3])
