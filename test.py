import os

BASE_FOLDER = "split_windows_2048"

all_window_files = []
for root, dirs, files in os.walk(BASE_FOLDER):
    if dirs != '31':
        for file in files:
            if file.endswith(".csv"):
                all_window_files.append(os.path.join(root, file))

print(len(all_window_files))