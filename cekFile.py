import os

# Path ke folder gambar dan folder label
image_folder = "....."  # Ganti dengan path folder gambar Anda
label_folder = "....."  # Ganti dengan path folder labelling Anda

# Ekstensi yang digunakan untuk file gambar
image_extensions = ['.jpg', '.jpeg', '.png']

# Dapatkan daftar nama file tanpa ekstensi
image_files = [os.path.splitext(f)[0] for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in image_extensions]
label_files = [os.path.splitext(f)[0] for f in os.listdir(label_folder) if f.endswith('.txt')]

# Cari label tanpa pasangan gambar
labels_without_images = [label for label in label_files if label not in image_files]

# Cari gambar tanpa pasangan label (opsional)
images_without_labels = [image for image in image_files if image not in label_files]

# Tampilkan hasil
if labels_without_images:
    print(f"Ada {len(labels_without_images)} file label yang tidak memiliki gambar:")
    for label in labels_without_images:
        print(f"- {label}.txt")
else:
    print("Semua file label memiliki pasangan gambar.")

if images_without_labels:
    print(f"Ada {len(images_without_labels)} file gambar yang tidak memiliki label:")
    for image in images_without_labels:
        print(f"- {image}.jpg/png")
else:
    print("Semua file gambar memiliki pasangan label.")

