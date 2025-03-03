# Skrip untuk memindahkan datasheet yang banyak ke folder train dan val otomaris
# Membaginya ke 2 bagian 80% train 20% val

import os
import shutil
import random

# Folder input
input_image_folder = "......" # lokasi folder images sebelum dipindah
input_label_folder = "....." # lokasi folder label sebelum dipindah

# Folder output untuk train dan val
output_image_train = "images/train"
output_image_val = "images/val"
output_label_train = "labels/train"
output_label_val = "labels/val"

# Membuat folder output jika belum ada
os.makedirs(output_image_train, exist_ok=True)
os.makedirs(output_image_val, exist_ok=True)
os.makedirs(output_label_train, exist_ok=True)
os.makedirs(output_label_val, exist_ok=True)

# Dapatkan semua gambar (nama file gambar tanpa ekstensi)
image_files = [f for f in os.listdir(input_image_folder) if f.endswith(('jpg', 'jpeg', 'png'))]

# Tentukan jumlah gambar untuk training dan validation (misalnya 80% untuk training)
train_size = int(0.8 * len(image_files))
train_images = random.sample(image_files, train_size)
val_images = [f for f in image_files if f not in train_images]

# Fungsi untuk memindahkan file dengan validasi pasangan
def move_file(image_folder, label_folder, image_name, image_dest, label_dest):
    label_name = image_name.split('.')[0] + '.txt'
    image_path = os.path.join(image_folder, image_name)
    label_path = os.path.join(label_folder, label_name)
    
    # Pastikan pasangan file ada sebelum memindahkan
    if os.path.exists(image_path) and os.path.exists(label_path):
        shutil.move(image_path, os.path.join(image_dest, image_name))
        shutil.move(label_path, os.path.join(label_dest, label_name))
    else:
        print(f"Pasangan file tidak ditemukan: {image_name} atau {label_name}")

# Pindahkan gambar dan label ke folder yang sesuai
for image_name in train_images:
    move_file(input_image_folder, input_label_folder, image_name, output_image_train, output_label_train)

for image_name in val_images:
    move_file(input_image_folder, input_label_folder, image_name, output_image_val, output_label_val)

print("Dataset telah dipisahkan ke dalam folder train dan val.")

