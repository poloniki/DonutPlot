import numpy as np
import cv2
import os, os.path

colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 0, 0),  # Maroon
    (0, 128, 0),  # Green (dark)
    (0, 0, 128),  # Navy
    (128, 128, 0),  # Olive
    (128, 0, 128),  # Purple
    (0, 128, 128),  # Teal
    (255, 165, 0),  # Orange
    (128, 128, 128),  # Gray
    (255, 255, 255),  # White
    (0, 0, 0),  # Black
    (255, 192, 203),  # Pink
    (255, 140, 0),  # Dark Orange
    (0, 128, 128),  # Dark Teal
    (255, 20, 147),  # Deep Pink
    (0, 255, 0),  # Lime
    (173, 255, 47),  # Green Yellow
    (135, 206, 250),  # Sky Blue
    (128, 0, 0),  # Maroon (dark)
    (255, 215, 0),  # Gold
]


def draw_boxes_all(
    source_path: str = "ObjectRecognition/yolo/dataset/train/",
    save_path: str = "ObjectRecognition/yolo/dataset/train/boxed/",
):
    # Create list with JPG and TXT files and sort lists alphabetically
    jpg_file_list = [file for file in os.listdir(source_path) if file.endswith(".jpg")]
    txt_file_list = [file for file in os.listdir(source_path) if file.endswith(".txt")]

    jpg_file_list_sorted = sorted(jpg_file_list)
    txt_file_list_sorted = sorted(txt_file_list)

    # Loop through all JPG and TXT files and create boxed
    for i in range(len(jpg_file_list_sorted)):
        # Read TXT files and split the lines
        with open(source_path + txt_file_list_sorted[i], "r") as file:
            file_contents = file.read().splitlines()

        # Read JPG files and save contents and pixels
        img = cv2.imread(source_path + jpg_file_list_sorted[i])
        x_pix = img.shape[1]
        y_pix = img.shape[0]

        # Draw rectangles
        for rowraw in file_contents:
            row = np.array([float(x) for x in rowraw.split()])
            cat = int(row[0])
            x1 = int(row[1] * x_pix) - int(row[3] * x_pix * 0.5)
            y1 = int(row[2] * y_pix) - int(row[4] * y_pix * 0.5)
            x2 = x1 + int(row[3] * x_pix)
            y2 = y1 + int(row[4] * y_pix)
            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                color=colors[cat],
                thickness=1,
            )

        # Write output image
        cv2.imwrite(save_path + jpg_file_list_sorted[i], img)


# If name = main
if __name__ == "__main__":
    train_folder = "ObjectRecognition/yolo/dataset/train/"
    boxed_folder = train_folder + "boxed/"

    print("Creating boxed files")
    os.makedirs(boxed_folder, exist_ok=True) if not os.path.exists(
        boxed_folder
    ) else None

    draw_boxes_all(train_folder, boxed_folder)
