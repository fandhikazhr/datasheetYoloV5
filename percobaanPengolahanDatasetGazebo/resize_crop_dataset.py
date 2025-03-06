import cv2
import numpy as np

def resize_and_pad(image, target_size=(640, 640)):
    old_size = image.shape[:2]  # Dimensi asli gambar (height, width)
    ratio = min(target_size[0] / old_size[0], target_size[1] / old_size[1])
    new_size = (int(old_size[1] * ratio), int(old_size[0] * ratio))  # (width, height)
    
    # Resize gambar
    resized_img = cv2.resize(image, new_size)
    
    # Padding
    delta_w = target_size[1] - new_size[0]
    delta_h = target_size[0] - new_size[1]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    
    color = [0, 0, 0]  # Padding hitam
    padded_img = cv2.copyMakeBorder(resized_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    
    return padded_img

# Contoh penggunaan
image = cv2.imread("....")
processed_img = resize_and_pad(image)
cv2.imwrite(".....", processed_img)

