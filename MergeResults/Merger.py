import json
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

markers = [
    ".",
    "o",
    "v",
    "^",
    "<",
    ">",
    "1",
    "2",
    "3",
    "4",
    "s",
    "p",
    "*",
    "h",
    "H",
    "+",
    "x",
    "D",
    "d",
]


def find_intersection_point(line1_point1, line1_point2, line2_point1, line2_point2):
    # Formulate the equations of the lines in the form Ax + By = C
    A1, B1, C1 = (
        line1_point2[1] - line1_point1[1],
        line1_point1[0] - line1_point2[0],
        line1_point1[0] * line1_point2[1] - line1_point2[0] * line1_point1[1],
    )
    A2, B2, C2 = (
        line2_point2[1] - line2_point1[1],
        line2_point1[0] - line2_point2[0],
        line2_point1[0] * line2_point2[1] - line2_point2[0] * line2_point1[1],
    )

    # Formulate the system of equations as a matrix
    matrix_coefficients = np.array([[A1, B1], [A2, B2]])
    constants = np.array([C1, C2])

    # Solve the system of equations
    intersection_point = np.linalg.solve(matrix_coefficients, constants)

    return intersection_point


## write directories for output data from models
donut_output = "../dataset/test/metadata.jsonl"
yolo_output = "../dataset/test/0000.txt"
image_input = "../dataset/test/0000.jpg"

## Open Donut data
with open(donut_output, "r") as file:
    donut_string = json.load(file)["ground_truth"]
donut_output = json.loads(donut_string)["gt_parse"]

title = donut_output["title"]
x_label = donut_output["x_label"]
y_label = donut_output["y_label"]
x_tick_values = donut_output["x_ticks"]
y_tick_values = donut_output["y_ticks"]

## Open Yolo data
with open(yolo_output, "r") as file:
    yolo_string = file.read().splitlines()

yolo_output = []
for line in yolo_string:
    newline = [float(x) for i, x in enumerate(line.split())]
    newline[0] = int(newline[0])
    if len(newline) == 5:
        newline.insert(1, 1.0)
    yolo_output.append(newline)
yolo_matrix = np.array(yolo_output)
yolo_matrix[:, 3] = (
    1 - yolo_matrix[:, 3]
)  # We need to go from yolo coordinates to graph coordinates. Move (0,0) from the top left to the bottom left.
## Open Image
img = Image.open(image_input)
pix_width = img.size[0]
pix_height = img.size[1]

# We get the coordinates of the tick marcks
x_ticks_coords = yolo_matrix[yolo_matrix[:, 0] == 0][:, 2:4]
y_ticks_coords = yolo_matrix[yolo_matrix[:, 0] == 1][:, 2:4]

# We get the coordinates of the scatterpoints
xy_coords = yolo_matrix[yolo_matrix[:, 0] > 1][:, 2:4]

marker_index = yolo_matrix[yolo_matrix[:, 0] > 1][0, 0]

# We compute the intersection point of the axis
axis_intersection = find_intersection_point(
    x_ticks_coords[0, :],
    x_ticks_coords[-1, :],
    y_ticks_coords[0, :],
    y_ticks_coords[-1, :],
)

# We compute the position of the scatterpoints with respect to the axiss intersextion
xy_on_axes = xy_coords - axis_intersection

# We compute the vectors of the axis. Ideally they should be ortonormal and only have one non-zero component
x_vector = x_ticks_coords[-1, :] - axis_intersection  # x_ticks_coords[0, :]
y_vector = y_ticks_coords[-1, :] - axis_intersection  # y_ticks_coords[0, :]
breakpoint()

# We compute the rotation matrix to correct for misalignments and shears
transformation_matrix = np.vstack(
    (x_vector / np.linalg.norm(x_vector), y_vector / np.linalg.norm(y_vector))
)
breakpoint()
# We transform the data so the result is ortonormal
xy_transformed = np.matmul(xy_on_axes, transformation_matrix)
axis_int_transformed = np.matmul(axis_intersection, transformation_matrix)
# We move the transformed dots to the data units space
xy_data = np.zeros(xy_transformed.shape)

xy_data[:, 0] = (xy_transformed[:, 0] + axis_int_transformed[0]) * (
    x_tick_values[-1] - x_tick_values[0]
)  # + x_tick_values[0]
xy_data[:, 1] = (xy_transformed[:, 1] + axis_int_transformed[1]) * (
    y_tick_values[-1] - y_tick_values[0]
)  # + y_tick_values[0]


fig, (ax1, ax2) = plt.subplots(1, 2, dpi=100, gridspec_kw={"width_ratios": [1, 1]})

ax1.imshow(img)

ax2.scatter(x=xy_data[:, 0], y=xy_data[:, 1], marker=markers[int(marker_index)])
ax2.set_xlabel(x_label)
ax2.set_ylabel(y_label)
ax2.set_title(title)
plt.show()

# x_scale = (x_tick_values[-1] - x_tick_values[0]) / np.linalg.norm(x_axis)
# y_scale = (x_tick_values[-1] - x_tick_values[0]) / np.linalg.norm(x_axis)


# min_confidence = 0.8
# x_tick_coords = np.zeros((0, 2))
# y_tick_coords = np.zeros((0, 2))
# for row in yolo_output:
#     if row[1] < min_confidence:
#         print(
#             f"Point skipped with confidence {row[1]}< Min conficence:{min_confidence}. Category {row[0]}  Coordinates {row[2:3]}"
#         )
#     else:
#         if row[0] == 0:
#             x_tick_coords = np.vstack((x_tick_coords, np.array(row[2:4])))
#         elif row[0] == 1:
#             y_tick_coords = np.vstack((y_tick_coords, np.array(row[2:4])))
#         else:
#             breakpoint()
