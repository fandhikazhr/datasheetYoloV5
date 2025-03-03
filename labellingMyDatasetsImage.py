import cv2
import os

# Inisialisasi variabel global
boxes = []
drawing = False
ix, iy = -1, -1
selected_class = 0
zoom_scale = 1.0  # Skala zoom awal
offset_x, offset_y = 0, 0  # Offset untuk zoom dan panning

# Daftar kelas (sesuaikan dengan kebutuhan)
class_list = ["logistik_besar", "logistik_kecil"]

def draw_rectangle(event, x, y, flags, param):
    global boxes, ix, iy, drawing, selected_class
    
    # Hitung posisi relatif terhadap zoom dan offset
    x = int((x - offset_x) / zoom_scale)
    y = int((y - offset_y) / zoom_scale)
    
    if event == cv2.EVENT_LBUTTONDOWN:  # Ketika klik mouse
        drawing = True
        ix, iy = x, y
    
    elif event == cv2.EVENT_MOUSEMOVE:  # Ketika mouse digerakkan
        if drawing:
            img_copy = img_display.copy()
            cv2.rectangle(img_copy, (int(ix * zoom_scale + offset_x), int(iy * zoom_scale + offset_y)),
                          (int(x * zoom_scale + offset_x), int(y * zoom_scale + offset_y)), (0, 255, 0), 2)
            cv2.putText(img_copy, class_list[selected_class], (int(ix * zoom_scale + offset_x), int(iy * zoom_scale + offset_y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            draw_crosshair(img_copy, x, y)
            cv2.imshow("Label Image", img_copy)
        else:
            img_copy = img_display.copy()
            draw_crosshair(img_copy, x, y)
            cv2.imshow("Label Image", img_copy)
    
    elif event == cv2.EVENT_LBUTTONUP:  # Ketika lepas klik mouse
        drawing = False
        x1 = int(ix)
        y1 = int(iy)
        x2 = int(x)
        y2 = int(y)
        boxes.append((x1, y1, x2, y2, selected_class))  # Simpan koordinat
        redraw_boxes()

def draw_crosshair(img, x, y):
    """Gambar crosshair di posisi kursor."""
    h, w, _ = img.shape
    x = int(x * zoom_scale + offset_x)
    y = int(y * zoom_scale + offset_y)
    color = (0, 255, 255)
    thickness = 1
    cv2.line(img, (x, 0), (x, h), color, thickness)
    cv2.line(img, (0, y), (w, y), color, thickness)

def redraw_boxes():
    """Gambar ulang semua bounding box."""
    global img_display
    img_display = cv2.resize(img, (int(img.shape[1] * zoom_scale), int(img.shape[0] * zoom_scale)))
    img_display = cv2.copyMakeBorder(img_display, offset_y, offset_y, offset_x, offset_x, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    for box in boxes:
        x1 = int(box[0] * zoom_scale + offset_x)
        y1 = int(box[1] * zoom_scale + offset_y)
        x2 = int(box[2] * zoom_scale + offset_x)
        y2 = int(box[3] * zoom_scale + offset_y)
        cv2.rectangle(img_display, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_display, class_list[box[4]], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("Label Image", img_display)

def change_class(key):
    global selected_class
    if key == ord('n'):  # Tombol 'n' untuk kelas berikutnya
        selected_class = (selected_class + 1) % len(class_list)
    elif key == ord('p'):  # Tombol 'p' untuk kelas sebelumnya
        selected_class = (selected_class - 1) % len(class_list)

def delete_last_box():
    """Hapus kotak bounding terakhir."""
    if boxes:
        boxes.pop()
        redraw_boxes()

def process_images_for_yolo(folder_path, output_path, class_list):
    images = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    
    # Simpan daftar kelas ke classes.txt
    classes_file = os.path.join(output_path, "classes.txt")
    with open(classes_file, "w") as f:
        f.write("\n".join(class_list))
    
    for img_name in images:
        global img, img_display, boxes, zoom_scale, offset_x, offset_y
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"Cannot read image {img_name}. Skipping.")
            continue
        
        # Reset variabel
        zoom_scale = 1.0
        offset_x, offset_y = 0, 0
        boxes = []
        redraw_boxes()

        print(f"Processing: {img_name}")
        cv2.imshow("Label Image", img_display)
        cv2.setMouseCallback("Label Image", draw_rectangle)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Tekan 'q' untuk selesai melabeli gambar
                break
            elif key == ord('n') or key == ord('p'):  # Tombol 'n' dan 'p' untuk mengganti kelas
                change_class(key)
            elif key == ord('d'):  # Tombol 'd' untuk menghapus bounding box terakhir
                delete_last_box()
            elif key == ord('+'):  # Tombol '+' untuk zoom in
                zoom_scale = min(zoom_scale + 0.1, 3.0)
                redraw_boxes()
            elif key == ord('-'):  # Tombol '-' untuk zoom out
                zoom_scale = max(zoom_scale - 0.1, 0.5)
                redraw_boxes()

        cv2.destroyAllWindows()
        
        # Simpan bounding box dalam format YOLO
        height, width = img.shape[:2]
        yolo_labels = []
        for box in boxes:
            x_center = ((box[0] + box[2]) / 2) / width
            y_center = ((box[1] + box[3]) / 2) / height
            w = abs(box[2] - box[0]) / width
            h = abs(box[3] - box[1]) / height
            yolo_labels.append(f"{box[4]} {x_center} {y_center} {w} {h}")
        
        # Simpan ke file .txt
        label_path = os.path.join(output_path, img_name.split('.')[0] + ".txt")
        with open(label_path, "w") as f:
            f.write("\n".join(yolo_labels))
        
        print(f"Saved labels for {img_name}")

# Contoh penggunaan
input_folder = "......"
output_folder = "....."
os.makedirs(output_folder, exist_ok=True)

process_images_for_yolo(input_folder, output_folder, class_list)
