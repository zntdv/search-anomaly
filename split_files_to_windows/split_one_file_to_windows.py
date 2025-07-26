import pandas as pd
import numpy as np
import os

def split_csv_to_windows(
    csv_path="./datasets/current_5.csv",
    output_dir="./split_windows/5",
    window_size=256,
    step_size=256,
    normalize=True
):
    # Чтение исходного CSV
    df = pd.read_csv(csv_path)
    
    # Проверка, что в файле 3 колонки (например: current_R, current_S, current_T)
    if df.shape[1] != 3:
        raise ValueError("Ожидалось 3 колонки с токами по фазам.")
    
    # Нормализация (по умолчанию включена)
    if normalize:
        df = (df - df.mean()) / df.std()
    
    # Подготовка окон
    num_windows = (len(df) - window_size) // step_size + 1
    windows = []
    
    for i in range(num_windows):
        start = i * step_size
        end = start + window_size
        window = df.iloc[start:end].copy()
        windows.append(window)
    
    # Создание выходной папки
    os.makedirs(output_dir, exist_ok=True)
    
    # Сохраняем каждое окно в отдельный CSV
    for idx, win_df in enumerate(windows):
        win_df.to_csv(os.path.join(output_dir, f"window_{idx:03d}.csv"), index=False)

    print(f"✅ Успешно разбито: {len(windows)} окон.")
    print(f"📁 Сохранено в папку: {output_dir}")

split_csv_to_windows(
    csv_path="./raw_data/current_2.csv",
    output_dir="./split_windows_2048/2",
    window_size=2048,
    step_size=2048,
    normalize=True
)