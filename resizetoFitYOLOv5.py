import cv2
import os

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

def process_folder(input_folder, output_folder, target_size=(640, 640)):
    # Membuat folder output jika belum ada
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterasi setiap file di folder input
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        
        # Cek apakah file adalah gambar
        if os.path.isfile(input_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Baca gambar
            image = cv2.imread(input_path)
            
            if image is not None:
                # Resize dan pad gambar
                processed_img = resize_and_pad(image, target_size)
                
                # Simpan hasilnya ke folder output
                output_path = os.path.join(output_folder, file_name)
                cv2.imwrite(output_path, processed_img)
                print(f"Processed and saved: {output_path}")
            else:
                print(f"Failed to read image: {input_path}")

# Contoh penggunaan
input_folder = "....."  # Ganti dengan path folder input
output_folder = "...."  # Ganti dengan path folder output

process_folder(input_folder, output_folder, target_size=(640, 640))

