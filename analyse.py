import os
import pandas as pd
import matplotlib.pyplot as plt

# === ПАРАМЕТРЫ ===
windows_folder = "split_windows"   # папка с разбитыми окнами
output_labels_file = "labels.csv"  # куда сохранять метки
available_labels = {
    0: "нет дефекта",
    1: "дефект подшипника",
    2: "дисбаланс",
    3: "расцентровка",
    4: "прочее"
}

# === ЧТЕНИЕ УЖЕ СОХРАНЕННЫХ МЕТОК ===
if os.path.exists(output_labels_file):
    labels_df = pd.read_csv(output_labels_file)
else:
    labels_df = pd.DataFrame(columns=["filename", "label"])

# === ПОЛУЧАЕМ СПИСОК ОКОН ===
window_files = sorted([f for f in os.listdir(windows_folder) if f.endswith('.csv')])
already_labeled = set(labels_df['filename'])

# === НАЧИНАЕМ РАЗМЕТКУ ===
for file in window_files:
    if file in already_labeled:
        continue  # уже размечено

    filepath = os.path.join(windows_folder, file)
    df = pd.read_csv(filepath)

    # Визуализация
    plt.figure(figsize=(12, 4))
    plt.plot(df['current_R'], label='Фаза R')
    plt.plot(df['current_S'], label='Фаза S')
    plt.plot(df['current_T'], label='Фаза T')
    plt.title(f"Окно: {file}")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Ручной ввод
    print("Выберите метку для этого окна:")
    for key, value in available_labels.items():
        print(f"{key} — {value}")
    
    while True:
        try:
            label = int(input("Введите номер метки: "))
            if label in available_labels:
                break
            else:
                print("Некорректная метка, попробуй снова.")
        except:
            print("Ошибка ввода, попробуй снова.")

    # Сохраняем метку
    labels_df = pd.concat([labels_df, pd.DataFrame([{"filename": file, "label": label}])], ignore_index=True)
    labels_df.to_csv(output_labels_file, index=False)
    print(f"✅ Метка сохранена: {available_labels[label]}")
    print("-" * 40)

print("🎉 Разметка завершена!")
