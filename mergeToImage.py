# Skrip parsing video to sequence image

import cv2
import os

# Path ke folder input dan output
input_folder = "......"
output_folder = "....."

# Membuat folder output jika belum ada
os.makedirs(output_folder, exist_ok=True)

# Mendapatkan semua file video dalam folder
video_extensions = ('.mp4', '.avi', '.mkv', '.mov')  # Tambahkan ekstensi sesuai kebutuhan
video_files = [f for f in os.listdir(input_folder) if f.endswith(video_extensions)]

print(f"File video ditemukan: {video_files}")

# Inisialisasi variabel untuk melanjutkan penomoran
last_saved_count = 0

# Proses setiap file video
for video_file in video_files:
    video_path = os.path.join(input_folder, video_file)
    video_name = os.path.splitext(video_file)[0]
    video_output_folder = os.path.join(output_folder, video_name)

    # Buat folder khusus untuk setiap video
    os.makedirs(video_output_folder, exist_ok=True)

    # Membuka video
    vidcap = cv2.VideoCapture(video_path)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Memproses {video_file} dengan total {total_frames} frame.")

    # Hitung interval untuk mendapatkan 100 gambar
    target_images = 10
    frame_interval = total_frames / target_images
    saved_count = last_saved_count
    frame_index = 0

    while saved_count < (last_saved_count + target_images) and vidcap.isOpened():
        # Set posisi frame
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
        success, image = vidcap.read()

        if success:
            # Simpan gambar
            output_file = os.path.join(video_output_folder, f"{saved_count}.png")
            cv2.imwrite(output_file, image)
            print(f"Saved Image {saved_count} for {video_file} at Frame {int(frame_index)}")
            saved_count += 1
            frame_index += frame_interval
        else:
            break

    vidcap.release()
    last_saved_count = saved_count  # Simpan angka terakhir yang digunakan
    print(f"Proses selesai untuk {video_file}. Total {saved_count - last_saved_count} frame disimpan di {video_output_folder}.")

print("Proses semua video selesai.")

