import cv2
import os

# Path dataset
input_folder = "...."
output_folder = "...."
os.makedirs(output_folder, exist_ok=True)

# Target size (640x640)
target_size = (640, 640)

# Loop semua gambar di folder
for filename in os.listdir(input_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Baca gambar
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        # Resize
        resized_img = cv2.resize(img, target_size)

        # Save hasil
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, resized_img)
        print(f"Processed and saved: {filename}")

