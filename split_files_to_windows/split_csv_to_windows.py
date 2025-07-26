import os
import pandas as pd

def split_csv_to_windows(csv_path, output_dir, window_size=256, step_size=None):
    """
    Разбивает CSV-файл на окна фиксированной длины и сохраняет в отдельные файлы.
    Показывает прогресс выполнения.
    """
    if step_size is None:
        step_size = window_size

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ Файл не найден: {csv_path}")

    df = pd.read_csv(csv_path)

    if not {"current_R", "current_S", "current_T"}.issubset(df.columns):
        raise ValueError("❌ Файл должен содержать колонки: current_R, current_S, current_T")

    os.makedirs(output_dir, exist_ok=True)

    total = len(df)
    num_windows = (total - window_size) // step_size + 1

    print(f"📁 Файл: {csv_path}")
    print(f"🔪 Размер окна: {window_size}, шаг: {step_size}")
    print(f"📊 Всего будет создано окон: {num_windows}")
    print(f"📂 Сохранение в: {output_dir}")

    try:
        from tqdm import tqdm
        iterator = tqdm(range(num_windows), desc="📦 Обработка окон")
    except ImportError:
        iterator = range(num_windows)

    for i in iterator:
        start = i * step_size
        end = start + window_size
        window_df = df.iloc[start:end].reset_index(drop=True)

        output_file = os.path.join(output_dir, f"window_{i:03d}.csv")
        window_df.to_csv(output_file, index=False)

        if 'tqdm' not in globals():
            print(f"✅ Окно {i+1}/{num_windows} сохранено")

    print(f"\n✅ Готово: {num_windows} окон сохранено в {output_dir}")

# 🔧 Пример использования:
split_csv_to_windows("./raw_data/current_5.csv", "./split_windows_256/5", window_size=256)
