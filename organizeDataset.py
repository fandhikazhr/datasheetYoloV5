import os
import shutil
import random

# Folder input
input_image_folder = "......"
input_label_folder = "......"

# Folder output untuk train dan val
output_image_train = "............"
output_image_val = "......"
output_label_train = "......."
output_label_val = "......."

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

# Pindahkan gambar dan label ke folder yang sesuai
for image_name in train_images:
    label_name = image_name.split('.')[0] + '.txt'
    shutil.move(os.path.join(input_image_folder, image_name), os.path.join(output_image_train, image_name))
    shutil.move(os.path.join(input_label_folder, label_name), os.path.join(output_label_train, label_name))

for image_name in val_images:
    label_name = image_name.split('.')[0] + '.txt'
    shutil.move(os.path.join(input_image_folder, image_name), os.path.join(output_image_val, image_name))
    shutil.move(os.path.join(input_label_folder, label_name), os.path.join(output_label_val, label_name))

print("Dataset telah dipisahkan ke dalam folder train dan val.")

