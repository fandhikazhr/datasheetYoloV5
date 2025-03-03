import os

# Path folder berisi file
folder_path = "........"

# Rentang nomor untuk penamaan
start_number = 625
end_number = 748

# Ambil semua file (hanya file biasa, bukan folder) dari folder
file_list = [f for f in sorted(os.listdir(folder_path)) if os.path.isfile(os.path.join(folder_path, f))]
file_extension = os.path.splitext(file_list[0])[1]  # Ambil ekstensi file pertama secara otomatis

# Pastikan jumlah file cocok dengan rentang
total_files_needed = end_number - start_number + 1

if len(file_list) != total_files_needed:
    print(f"Jumlah file ({len(file_list)}) tidak sesuai dengan rentang ({total_files_needed}).")
    print("Periksa apakah ekstensi file benar atau ada file yang hilang.")
else:
    # Ubah nama file
    for i, file_name in enumerate(file_list):
        new_name = f"{start_number + i}{file_extension}"
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_name)

        # Ubah nama file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed: {file_name} -> {new_name}")

    print("Semua file telah berhasil diubah namanya.")

