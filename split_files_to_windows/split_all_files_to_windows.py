import pandas as pd
import numpy as np
import os

def split_all_csv_in_folder(
    input_folder="./raw_data",
    output_base_folder="./split_windows",
    window_size=256,
    step_size=256,
    normalize=True
):
    csv_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".csv")])

    print(f"🔍 Найдено файлов для обработки: {len(csv_files)}")

    for idx, file_name in enumerate(csv_files, 1):
        csv_path = os.path.join(input_folder, file_name)
        dataset_num = file_name.split("_")[-1].split(".")[0]  # Извлечение N из current_N.csv
        output_dir = os.path.join(output_base_folder, dataset_num)

        print(f"\n📂 [{idx}/{len(csv_files)}] Обрабатывается файл: {file_name}")

        try:
            df = pd.read_csv(csv_path)

            if df.shape[1] != 3:
                print(f"⚠️ Пропуск файла — неверное количество колонок: {file_name}")
                continue

            if normalize:
                df = (df - df.mean()) / df.std()

            num_windows = (len(df) - window_size) // step_size + 1

            if num_windows <= 0:
                print(f"⚠️ Пропуск файла — недостаточно данных для окон: {file_name}")
                continue

            os.makedirs(output_dir, exist_ok=True)

            for win_idx in range(num_windows):
                start = win_idx * step_size
                end = start + window_size
                window_df = df.iloc[start:end].copy()
                window_df.to_csv(os.path.join(output_dir, f"window_{win_idx:03d}.csv"), index=False)

                if win_idx % 100 == 0 or win_idx == num_windows - 1:
                    print(f"   ✅ Сохранено {win_idx + 1}/{num_windows} окон", end="\r")

            print(f"✅ Файл обработан. Всего окон: {num_windows}")

        except Exception as e:
            print(f"❌ Ошибка при обработке {file_name}: {e}")

# Пример вызова:
split_all_csv_in_folder(
    input_folder="./raw_data",
    output_base_folder="./split_windows_256",
    window_size=256,
    step_size=256,
    normalize=True
)
