import cv2
import os

# Path video input dan output
video_path = "...."
output_path = "..."

# Membuat folder output jika belum ada
os.makedirs(output_path, exist_ok=True)

# Membuka video
vidcap = cv2.VideoCapture(video_path)

# Mendapatkan total frame
total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total Frames in Video: {total_frames}")

# Hitung interval frame
target_images = 100
frame_interval = total_frames / target_images
print(f"Frame Interval: {frame_interval:.2f}")

saved_count = 0
frame_index = 0

while saved_count < target_images and vidcap.isOpened():
    # Set posisi frame yang akan dibaca
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
    success, image = vidcap.read()

    if success:
        # Simpan gambar
        output_file = os.path.join(output_path, f"{saved_count}.png")
        cv2.imwrite(output_file, image)
        print(f"Saved Image {saved_count} at Frame {int(frame_index)}")
        saved_count += 1
        frame_index += frame_interval
    else:
        break

vidcap.release()
print(f"Proses selesai. Total {saved_count} frame disimpan di {output_path}")
